import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from dotenv import load_dotenv

load_dotenv()


def send_email(to_email: str, subject: str, message: str):
    # todo remake this email and password so they will be setting from .env file
    # from_email = "boss.igroteka@mail.ru"  # Replace with your email address
    # password = "9T225JimsA5HQaMp05ZV"  # Replace with your email password
    # from_email = "pavlina.sokolova.94@list.ru"  # Replace with your email address
    # password = "12{me3Ibj3"  # Replace with your email password
    from_email = os.getenv("FROM_EMAIL")  # Replace with your email address
    password = os.getenv("PASSWORD")  # Replace with your email password
    print(from_email)
    print(password)
    try:
        server = smtplib.SMTP("smtp.mail.ru", 587)
        server.starttls()
        server.login(from_email, password)

        # Create the email message
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = formataddr(("Риелтор бот", from_email))
        msg['To'] = to_email

        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}


# res = send_email(to_email="boss.igroteka@mail.ru", subject='Пришла заявка на продажу', message=f'Данные пользователя: asd')
# print(res)
