from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import os
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(to_address, filename):
    from_address = "your-email@example.com"
    password = "your-email-password"

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "TOPSIS Result File"

    body = "Please find the attached TOPSIS result file."
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()

def topsis(data, weights, impacts):
    weights = np.array(weights)
    impacts = np.array(impacts)

    norm_data = data / np.sqrt((data ** 2).sum())

    weighted_data = norm_data * weights

    ideal_best = np.max(weighted_data, axis=0) * impacts + np.min(weighted_data, axis=0) * (1 - impacts)
    ideal_worst = np.min(weighted_data, axis=0) * impacts + np.max(weighted_data, axis=0) * (1 - impacts)

    dist_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    performance_score = dist_worst / (dist_best + dist_worst)
    return performance_score

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            weights = list(map(float, request.form['weights'].split(',')))
            impacts = list(map(lambda x: 1 if x == '+' else 0, request.form['impacts'].split(',')))
            email_id = request.form['email']

            try:
                v = validate_email(email_id)
                email_id = v["email"]
            except EmailNotValidError as e:
                return str(e)

            data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if len(weights) != len(impacts) or len(weights) != data.shape[1] - 1:
                return "Number of weights must be equal to number of impacts and must match the number of criteria in the file."

            scores = topsis(data.iloc[:, 1:], weights, impacts)
            data['Topsis Score'] = scores
            data['Rank'] = scores.rank(ascending=False)

            result_filename = "result_" + filename
            data.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], result_filename), index=False)

            send_email(email_id, os.path.join(app.config['UPLOAD_FOLDER'], result_filename))
            return "Result file sent to your email!"

    return '''
    <!doctype html>
    <title>TOPSIS Web Service</title>
    <h1>Upload CSV File for TOPSIS</h1>
    <form method=post enctype=multipart/form-data>
      <label for="file">File Name</label>
      <input type="file" name="file"><br><br>
      <label for="weights">Weights</label>
      <input type="text" name="weights"><br><br>
      <label for="impacts">Impacts</label>
      <input type="text" name="impacts"><br><br>
      <label for="email">Email Id</label>
      <input type="text" name="email"><br><br>
      <input type="submit" value="Submit">
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
