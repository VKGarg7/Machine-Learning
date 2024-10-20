from flask import Flask, render_template, request, redirect, url_for
from image_downloader import download_images
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        num_images = int(request.form["num_images"])
        email = request.form["email"]
        output_folder = './static/images'

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        download_images(query, num_images, output_folder)

        send_confirmation_email(email, query, num_images)

        return redirect(url_for("gallery"))
    return render_template("index.html")

@app.route("/gallery")
def gallery():
    image_folder = './static/images'
    images = os.listdir(image_folder)
    return render_template("gallery.html", images=images)

def send_confirmation_email(to_email, query, num_images):
    """Function to send a confirmation email"""
    msg = Message(
        "Image Download Completed",
        sender="your_email@gmail.com",
        recipients=[to_email]
    )
    msg.body = f"The download for {num_images} images related to '{query}' has been completed successfully."
    mail.send(msg)

if __name__ == "__main__":
    app.run(debug=True)
