""" Main router for the application """
import requests

from flask import Flask, render_template, request, flash
from utils_package.py_utils.logger import logger

from application.functions.contact_form import contact_form

from application.base_configurations import VARS

app = Flask(__name__, template_folder='static')
app.secret_key = VARS['application.keys.secret_key']

# HTML Class Definitions
set_current = 'current'
set_error = 'display_error'
set_success = 'display_success'

# reCaptcha Variables
site_key = VARS['captcha.keys.site_key']
secret_key = VARS['captcha.keys.secret_key']

## TEST PORTION
# Test Page
@app.route('/test')
def test_page():
    return render_template('pages/zz_sample_output.html', site_key=site_key)


@app.route('/handle', methods=['POST'])
def lists():
    parameters = request.form

    recaptcha_passed = False
    recaptcha_response = parameters.get('g-recaptcha-response')
    try:
        # recaptcha_secret = os.environ.get('RECAPTCHA_SECRET')
        response = requests.post(f'https://www.google.com/recaptcha/api/siteverify?secret='
                                 f'{secret_key}&response={recaptcha_response}').json()
        recaptcha_passed = response.get('success')
        return render_template('pages/zz_test_data_output.html', result=response)
    except Exception as e:
        print(f"failed to get reCaptcha: {e}")


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
    return render_template('pages/contact_form.html', links_class=set_current, site_key=site_key, secret_key=secret_key)


# APPLICATION INTEGRATION
@app.route('/links/links_contact_send', methods=['POST'])
def contact_form_input():
    if request.method == 'POST':
        result = request.form
        captcha_response = result.get('g-recaptcha-response')
        try:
            response = requests.post(f'https://www.google.com/recaptcha/api/siteverify?secret='
                                     f'{secret_key}&response={captcha_response}').json()
            if response.get('success') is False:
                logger.error('reCaptcha failed...')
                flash('reCaptcha failed. If this is a mistake, contact me directly beringersolutions@gmail.com')
                return render_template('pages/contact_form.html', links_class=set_current,
                                       message_display_class=set_error)
        except Exception as e:
            logger.error(f'Failed to get reCaptcha: {e}')
        response = contact_form.contact_form_submission(result['name'], result['email'], result['message'])
        logger.info('Form submission status code: ' + str(response['status_code']))
        logger.info('Form submission display message: ' + response['display_message'])
        if response['status_code'] == 201:
            flash(response['display_message'])
            return render_template('pages/contact_form.html', links_class=set_current,
                                   message_display_class=set_success)
        else:
            flash(response['display_message'])
            return render_template('pages/contact_form.html', links_class=set_current, message_display_class=set_error)


if __name__ == '__main__':
    app.run(debug=True)
