from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
#import os


app = Flask(__name__)

#Email Configuration

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'teja.m.b15@outlook.com'
app.config['MAIL_PASSWORD'] = 'Crusader#15'#os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)

#Creating a route to show home page
@app.route('/')
def home():
    return render_template("home.html")


#Creating a route to send email
@app.route('/send_email', methods=['POST','GET'])
def send_email():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        msg = Message(sender= 'teja.m.b15@outlook.com',subject=subject,body=message_body,recipients=[recipient])
        #mail.send(msg)
        
        try:
            mail.send(msg)
            #return "Email has been sent successfully!!!"
            return render_template('emailsuccess.html')
        
        except Exception as e:
            return str(e), 500
    return render_template("email.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            #return "Logged in successfully!"
            return render_template('email.html')
        
        else:
            #return "Invalid username or password."
            return render_template('userinvalidcredentials.html')

    return render_template('login.html')

    #     if users.get(username) == password:
    #         # User authenticated, you can set a session here
    #         return redirect(url_for('home'))
    #     else:
    #         error_message = "Invalid username or password"
    #         return render_template('login.html', error=error_message)

    # return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')
    #return render_template('register.html')

@app.route('/signout', methods=['POST'])
def logout():
    #session.clear()
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)