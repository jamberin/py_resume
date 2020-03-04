""" Main router for the application """
from flask import Flask, render_template, request
from application.functions.contact_form import contact_form

app = Flask(__name__, template_folder='static')
set_current = 'current'


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
    return render_template('pages/contact_form.html', links_class=set_current)


# APPLICATION INTEGRATION
@app.route('/links/links_contact_send', methods=['POST'])
def contact_form_input():
    if request.method == 'POST':
        result = request.form
        response = contact_form.contact_form_submission(result['name'], result['email'], result['message'])
        # TODO generate method to display error messaging
        return render_template('pages/zz_sample_output.html', result=response)


if __name__ == '__main__':
    app.run(debug=True)
