""" Handle all configurations for repository """
from utils_package.api_controller.configman import ConfigmanController

VARS = ConfigmanController().get_application_configs('resume_site', 'vars')
DIRS = ConfigmanController().get_application_configs('resume_site', 'dirs')
