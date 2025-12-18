import os
from flask import Flask
from flask import render_template,redirect,url_for
from forms import EmailForm
from mailjet_rest import Client
from dotenv import load_dotenv


app = Flask(__name__)

ENV_PATH = '.env'
load_dotenv(ENV_PATH)

app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-key")

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

        MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
        MAILJET_SECRET_KEY = os.getenv('MAILJET_SECRET_KEY')
        SENDER_EMAIL = os.getenv('SENDER_EMAIL')
        RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
        subject="User Enquiry"

        try:
            mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')
            data = {
            'Messages': [
                            {
                                "From": {
                                        "Email": SENDER_EMAIL,
                                        "Name": "Portfolio website"
                                },
                                "To": [
                                        {
                                                "Email": RECEIVER_EMAIL,
                                                "Name": "Receiver Email"
                                        }
                                ],
                                "Subject": subject,
                                "TextPart": f"This email is from {email}. {messages}",
                                "HTMLPart": f"""<h1>This email is from {email}</h1><br/><h3>{messages}</h3>"""
                            }
                    ]
            }
            result = mailjet.send.create(data=data)
            print(result.status_code)
            print(result.json())
        except Exception as e:
            print(str(e))
        return redirect(url_for('contact_me'))
    return render_template('contact_me.html',form=form)

if __name__=="__main__":
    app.run(debug=True)