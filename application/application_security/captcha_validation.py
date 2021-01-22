""" Validation rules for captcha """
from utils_package.data_controller.scripts.captcha_cookie.site_captcha_results_queries import SiteCaptchaResultsWriter
from utils_package.py_utils.logger import logger
from datetime import datetime, timedelta
from cryptography.fernet import Fernet


class CaptchaValidation:

    def __init__(self, encryption_key=None):
        """ Initialize class variables """
        self.captcha_writer = SiteCaptchaResultsWriter()
        self.encryption = Fernet(encryption_key)

    def new_cookie_captcha(self, ipaddress, score):
        """
        Generate a new captcha record for captcha results
        Args:
            ipaddress: ipaddress of the client machine
            score: decimal scale of the captcha score

        Returns:
            dictionary of cookie data to be sent to the client
        """
        # Set up content to be stored
        expiration_date = datetime.now() + timedelta(days=1)
        human_prob = float(score)  # Eventually this will be reworked to be based on IP hit frequency

        # Build the cookie to be returned
        cookie = {
            'expiration_date': str(expiration_date.timestamp()),
            'ipaddress': ipaddress,
            'score': str(score),
            'human_prob': str(human_prob)
        }

        # Build insert dictionary
        record_dict = {
            'ipaddress': ipaddress,
            'score': str(score),
            'cookie_content': str(cookie)
        }

        # Insert new record to database
        response = self.captcha_writer.insert_new_record(record_dict)
        if response[0] == 1:
            logger.info('Record updated successfully')
        else:
            logger.error('Issue updating record in database')

        # Encrypt the cookie
        cookie = self.encryption.encrypt(bytes(str(cookie), 'utf-8'))

        # Return cookie
        return cookie

    def captcha_cookie_validation(self, cookie_data):
        """
        Decrypt and validate a cookie's content is valid before letting them send a message
        Args:
            cookie_data: bytes of encrypted data with appropriate content

        Returns:
            dict containing boolean of success or failure, along with error code and message
        """
        # Decrypt the cookie
        cookie_data = dict(self.encryption.decrypt(cookie_data))

        # Validate the datetime
        if cookie_data['expiration_date'] < str(datetime.now().timestamp()):
            logger.info('Cookie expired, create new one')
            return 407, 'New cookie required'

        # Validate the captcha score
        if float(cookie_data['score']) <= 0.3:
            logger.info('reCAPTCHA score is too low')
            return 401, 'Failed reCAPTCHA score'

        # Return response
        return 200, 'Cookie is valid'
