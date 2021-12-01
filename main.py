#!/usr/bin/env python

import json 
import random
import smtplib

from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
    with open("people.json", "r") as rf:
        decoded_data = json.load(rf)

    people = [*decoded_data]

    people_shuffled = random.sample(people, len(people))

    for i in range(len(people)): 
        is_self = False
        if people[i] in people_shuffled:
            is_self = True
            people_shuffled.remove(people[i])
        secret_santa = random.choice(people_shuffled) 
        if secret_santa in people_shuffled:
            people_shuffled.remove(secret_santa)
        
        content_html = f"""
            <html>
            <body>
                <h2>Hello, {people[i]}</h2>
                <h3>You got {secret_santa} for your Secret Santa Gift Exchange</h3>
                <h3>Gift Price Range: $20 - $25</h3>
                <h3>Secret Santa & Friendsgiving:</h3>
                <p>
                    Location: KP's place(10317 Wood Rd, Fairfax, VA 22030) <br>
                    Time: 3 pm - 9 pm
                    Food: It's a potluck so you better bring at least ONE food item(not just snacks)
                    Alcohol: On me
                </p>
            </body>
            </html>
        """
        send_email(decoded_data[people[i]]["email"], "SECRET SANTA GIFT EXCHANGE", content_html)
        if is_self:
            people_shuffled.append(people[i])

def send_email(to_email, subject, content_html):
    from_email = config("SENDER")

    message = MIMEMultipart("mixed")
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email

    # write the HTML part
    part = MIMEText(content_html, "html")
    message.attach(part)

    with smtplib.SMTP(config("SMTP_SERVER"), config("SMTP_PORT")) as server:
        if config("SMTP_TLS"):
            print("SMTP server initiating a secure connection with TLS")
            server.starttls()
        print("SMTP server {0}:{1} started".format(config("SMTP_SERVER"), config("SMTP_PORT")))
        server.login(config("SMTP_USERNAME"), config("SMTP_PASSWORD"))
        print("SMTP server logged in with user {0}".format(config("SMTP_USERNAME")))
        server.sendmail(from_email, to_email, message.as_bytes())
        print("SMTP server sent email message")

if __name__ == "__main__":
    main()