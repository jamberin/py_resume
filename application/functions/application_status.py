""" Class to handle the status page data compilation
> Get DB health check
> > Ensure that both readers/writers are able to hit the database
> Get Project Git Information
> > Pull project level information
> > Parse for release/tag information
> Generate Page Response
> > Build appropriate content
"""
from utils_package.py_utils.logger import logger
from utils_package.data_controller.scripts.health_check import HealthCheck
from git import Repo


def git_info():
    my_repo = Repo(search_parent_directories=True)
    branch = my_repo.active_branch
    head = my_repo.head
    return branch.name, head.commit


class ApplicationStatus(object):

    def __init__(self):
        self.db_health_check = HealthCheck()

    def application_db_health_check(self):
        """
        Validate the database users are able to hit appropriately
        Returns:
            dict of users and statuses
        """
        response = {
            'reader': self.db_health_check.validate_reader_up(),
            'writer': self.db_health_check.validate_writer_up()
        }
        return response

    def generate_status_response(self):
        """
        Generate the default JSON payload for the status page
        Returns:
            dict of the content to be displayed on the page
        """
        # Relevant git information
        branch_name, commit = git_info()

        # DB status info
        db_status = self.application_db_health_check()

        # Build the dictionary
        response = {
            'branch_info': branch_name,
            'commit': commit.name,
            'db_info': db_status
        }

        # Return the response
        return response
