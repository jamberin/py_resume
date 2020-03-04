""" Different validation rules that are eligible to test against fields """
import re
from utils_package.data_controller.json_config import JSONConfig


class GeneralRegexValidations:
    """ Validations against different regex rules """

    def __init__(self):
        """ Initialize class variables """
        self.regex_configs = JSONConfig().get_email_controller_config('regex')

    def email_validation(self, email_string):
        """
        Validate a string is a valid email address
        :param email_string: Input string to be evaluated as an email address
        :return: Validation boolean
        """
        return self.__regex_validate(self.regex_configs['email'], email_string)

    def name_validation(self, name_string):
        """
        Validate a string is a valid name string
        :param name_string: Input string to be evaluated as a name
        :return: Validation boolean
        """
        return self.__regex_validate(self.regex_configs['names'], name_string)

    def message_validation(self, message_string):
        """
        Validate a message string input is valid
        :param message_string: Input string to be evaluated as a paragragh message
        :return: Validation boolean
        """
        return self.__regex_validate(self.regex_configs['special_char_exclusion'], message_string)

    @staticmethod
    def __regex_validate(regex, input_string):
        """
        Validate that the given text is an email address using regex
        :param input_string: Email address to be evaluated
        :return: Return resposne status
        """
        validation = re.match(regex, input_string)
        if validation:
            return True
        else:
            return False
