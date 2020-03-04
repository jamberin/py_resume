""" Class to handle the contact form tasks
> Send contact form entry
> > Will validate the user is eligible to send
> > Returns the appropriate status code
> Send response email
> > If the user doesn't have a violation, will send response
> > If the user does have a violation, will not reach this step
"""
from email_controller.contact_handler import ContactHandler
from email_controller.response_handler import ResponseHandler
from utils_package.py_utils.logger import logger
from application.application_security.field_validation import GeneralRegexValidations


class ContactForm(object):
    """ Handles all contact form interactions """

    def __init__(self):
        """ Initialize Class Variables """
        self.contact_handler = ContactHandler()
        self.response_handler = ResponseHandler()
        self.regex = GeneralRegexValidations()

    def contact_form_submission(self, name, email, message):
        """
        Handle the form for a contact form submission
        :param name: Name of the person making the contact
        :param email: Email address of the person making the contact
        :param message: Message being sent
        :return: Status Code, Display Message, and Validation
        """
        logger.info('New contact form submission')
        validations = self.regex_validations(name, email, message)
        if len(validations) > 0:
            code = 400
            display = 'Looks like there was an issue with your request. Make sure the fields are correct.'
            response = {
                'violation_code': [400],
                'violation_reasons': validations,
                'display_message': 'Looks like there was an issue with your request. Make sure the fields are correct.'
            }
            return code, display, response
        code, display, response = self.contact_handler.contact_form_entry(name, email, message)
        logger.info('Contact submission transmitted ')
        if code == 201:
            logger.info('Sending response')
            chk = self.response_handler.send_response_email(email)
            assert chk is True, 'There was an issue sending the response email'
        else:
            logger.error('There was an issue sending the contact form entry')
            logger.error('Code: %s | Display Message: %s | Full Validation: %s' % (code, display, response))
        return code, display, response

    def regex_validations(self, name, email, message):
        """
        Validate that all fields pass the regex validations
        :param name: Name of the person making the contact
        :param email: Email address of the person making the contact
        :param message: Message being sent
        :return: Error Validation Response
        """
        logger.info('Validating form values')
        validation_rejections = []
        name_chk = self.regex.name_validation(name)
        email_chk = self.regex.email_validation(email)
        message_chk = self.regex.message_validation(message)

        if name_chk is False:
            logger.error('Name not accepted: %s' % name)
            validation_rejections.append('Name')
        elif email_chk is False:
            logger.error('Email not accepted: %s' % email)
            validation_rejections.append('Email')
        elif message_chk is False:
            logger.error('Message not accepted: %s' % message)
            validation_rejections.append('Message')
        return validation_rejections


contact_form = ContactForm()
