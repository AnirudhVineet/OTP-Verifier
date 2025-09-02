import smtplib
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
S_email = "anirudhnoreply@gmail.com"
app.secret_key = "1n9ru48"  # required for sessions and flash

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        R_email = request.form["email"]

        # Generate OTP
        otp = random.randint(100000, 999999)
        session["otp"] = str(otp)
        session["R_email"] = R_email  # store recipient email too

        subject = "OTP Tester"
        message = f"Subject: {subject}\n\nYour OTP is {otp}"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(S_email, "nrfb gtaa ratb pbeg")  # Gmail app password
            server.sendmail(S_email, R_email, message)
            server.quit()

            flash(f"OTP sent to {R_email} successfully!")
            return redirect(url_for("verify"))
        except Exception as e:
            flash(f"Error sending email: {e}")

    return render_template("SendEmail.html")


@app.route("/VerifyOTP", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        num = request.form["number"]
        otp = session.get("otp")

        if otp and num == otp:
            flash("✅ The OTP you entered is correct!")
            session.pop("otp", None)  # clear OTP after success
            return redirect(url_for("home"))
        else:
            flash("❌ The OTP you entered is incorrect!, OTP has been resent")
            

    return render_template("VerifyOTP.html")


if __name__ == "__main__":
    app.run(debug=True)
