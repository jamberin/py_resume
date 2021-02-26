""" Main router for the application """
import requests

from flask import Flask, render_template, request, flash, make_response
from utils_package.py_utils.logger import logger

from application.functions.contact_form import contact_form
from application.application_security.captcha_validation import CaptchaValidation

from application.base_configurations import VARS

app = Flask(__name__, template_folder='static')
app.secret_key = VARS['application.keys.secret_key']

# HTML Class Definitions
set_current = 'current'
set_error = 'display_error'
set_success = 'display_success'

# reCaptcha Variables
captcha_site_key = VARS['captcha.keys.site_key']
# had to change name because setting as secret_key overwrites app.secret_key
captcha_secret_key = VARS['captcha.keys.secret_key']

# Application Imports
captcha_validation = CaptchaValidation(app.secret_key)


## TEST PORTION
# Test Page
# @app.route('/test')
# def test_page():
#     return render_template('pages/zz_sample_output.html', site_key=captcha_site_key)
#
#
# @app.route('/handle', methods=['POST'])
# def lists():
#     parameters = request.form
#     ipaddress = request.headers.get('X-Forwarded-For', request.remote_addr)
#     recaptcha_passed = False
#     recaptcha_response = parameters.get('g-recaptcha-response')
#     try:
#         # recaptcha_secret = os.environ.get('RECAPTCHA_SECRET')
#         response = requests.post(f'https://www.google.com/recaptcha/api/siteverify?secret='
#                                  f'{captcha_secret_key}&response={recaptcha_response}').json()
#         recaptcha_passed = response.get('success')
#         logger.debug(f'test ipaddress: {ipaddress}')
#         # response.append({'real_ipaddress': ipaddress})
#
#     except Exception as e:
#         print(f"failed to get reCaptcha: {e}")
#         response = {
#             'error': e
#         }
#     finally:
#         cookie_content = {
#             'variable1': 'value1',
#             'variable2': 'value2'
#         }
#         # only way to handle the cookie is to handle it as make response
#         # render template generates the template as a string to be passed to the client
#         payload = make_response(render_template('pages/zz_test_data_output.html', result=response))
#         payload.set_cookie('beringersolutions', str(cookie_content))
#         return payload


# Home Page - Main Index
@app.route('/')
def home_page():
    return render_template('pages/index.html', home_class=set_current)


# Landing Pages - Secondary Index
@app.route('/resume')
def resume_landing_page():
    return render_template('pages/resume.html', resume_class=set_current)


@app.route('/blog')
def blog_landing_page():
    return render_template('pages/blog.html', blog_class=set_current)


@app.route('/links')
def links_landing_page():
    return render_template('pages/links.html', links_class=set_current)


@app.route('/about')
def about_landing_page():
    return render_template('pages/about_me.html', about_class=set_current)


# Sub-Pages - Tertiary Index
# RESUME SUBPAGES
@app.route('/resume/download')
def resume_download_page():
    return render_template('pages/resume_download.html', resume_class=set_current)


@app.route('/resume/projects')
def projects_page():
    return render_template('pages/projects.html', resume_class=set_current)


@app.route('/resume/work')
def work_exp_page():
    return render_template('pages/work_exp.html', resume_class=set_current)


@app.route('/resume/tech')
def tech_exp_page():
    return render_template('pages/tech_exp.html', resume_class=set_current)


# LINKS SUBPAGES
@app.route('/links/contact')
def contact_form_page():
    return render_template('pages/contact_form.html', links_class=set_current, site_key=captcha_site_key, secret_key=captcha_secret_key)


# APPLICATION INTEGRATION
@app.route('/links/links_contact_send', methods=['POST'])
def contact_form_input():
    ipaddress = request.headers.get('X-Forwarded-For', request.remote_addr)
    message_allowed = True
    need_cookie = True
    cookie = None
    if request.method == 'POST':
        form_result = request.form
        if 'BS' in request.cookies:
            resp_code, resp_message = captcha_validation.captcha_cookie_validation(request.cookies.get('BS'))
            logger.info(f'Cookie validation response: {resp_code}: {resp_message}')
            if resp_code == 401:
                logger.warning('User previously was set with a score that is too low.')
                logger.warning('Setting flag for message ineligible')
                message_allowed = False
                need_cookie = False
            if resp_code == 200:
                logger.info('User with valid cookie')
                need_cookie = False
        captcha_result = form_result.get('g-recaptcha-response')
        if need_cookie:
            try:
                captcha_response = requests.post(f'https://www.google.com/recaptcha/api/siteverify?secret='
                                                 f'{captcha_secret_key}&response={captcha_result}').json()
                if captcha_response.get('success') is False:
                    logger.error('reCAPTCHA failed...')
                    message_allowed = False
                else:
                    logger.info('reCAPTCHA passed')
                cookie = captcha_validation.new_cookie_captcha(ipaddress, captcha_response.get('score'))
            except Exception as e:
                logger.error(f'Failed to get reCAPTCHA: {e}')
                flash('Totally our fault, seems like there was an error. '
                      'Please reach out to beringersolutions@gmail.com directly')
                return make_response(render_template('pages/contact_form.html', links_class=set_current,
                                                     message_display_class=set_error))
        if message_allowed:
            response = contact_form.contact_form_submission(form_result['name'], form_result['email'],
                                                            form_result['message'])
            logger.info(f"Form submission status code: {str(response['status_code'])}")
            logger.info(f"Form submission display message: {response['display_message']}")
            if response['status_code'] == 201:
                flash(response['display_message'])
                template = make_response(render_template('pages/contact_form.html', links_class=set_current,
                                                         message_display_class=set_success))
            else:
                flash(response['display_message'])
                template = make_response(render_template('pages/contact_form.html', links_class=set_current,
                                                         message_display_class=set_error))
        else:
            flash('reCAPTCHA failed. If this is a mistake, contact me directly beringersolutions@gmail.com')
            template = make_response(render_template('pages/contact_form.html', links_class=set_current,
                                                     message_display_class=set_error))
        if cookie is not None:
            template.set_cookie('BS', cookie)

        return template

# # Status Endpoint
# @app.route('/status')
# def status_page():
#     """ Endpoint to return the application status """
#

if __name__ == '__main__':
    app.run(debug=True)
