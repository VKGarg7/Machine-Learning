from flask import Flask, render_template, request, send_file
import zipfile
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    singer_name = request.form['singer_name']
    num_videos = int(request.form['num_videos'])
    duration = request.form['duration']
    email = request.form['email']

    # Create a zip file with the provided information (simulated)
    zip_filename = 'videos.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for i in range(num_videos):
            zip_file.writestr(f'video_{i+1}.txt', f'Singer: {singer_name}, Duration: {duration}')

    # Send the zip file via email (you need to provide your email and password)
    send_email(email, zip_filename)

    return f"Submission received! A zip file has been sent to {email}."

def send_email(to_email, zip_filename):
    from_email = "your_email@gmail.com"  # Replace with your email
    from_password = "your_password"       # Replace with your email password

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Your Video Files"

    body = "Attached is the zip file with your requested videos."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the zip file
    with open(zip_filename, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(zip_filename))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_filename)}"'
        msg.attach(part)

    # Set up the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
