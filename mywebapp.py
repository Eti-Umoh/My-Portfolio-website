import os
from flask import Flask
from flask import render_template,request,redirect,url_for
from forms import EmailForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv


app = Flask(__name__)

ENV_PATH = '.env'
load_dotenv(ENV_PATH)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    print(os.getenv('SECRET_KEY'))
    return render_template('index.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

@app.route('/certificates&projects')
def certificates():
    return render_template('certificates&projects.html')

@app.route('/contact_me',methods=['GET','POST'])
def contact_me():
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        messages = form.messages.data

        SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
        SMTP_HOST_SENDER ='simeoneumoh@gmail.com'

        message = Mail(
        from_email=SMTP_HOST_SENDER,
        to_emails="etiumoh04@gmail.com",
        subject="User Enquiry",
        html_content=f"<p>This email is from {email}</p><p>{messages}</p>")
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
        return redirect(url_for('contact_me'))
    return render_template('contact_me.html',form=form)

if __name__=="__main__":
    app.run(debug=True)