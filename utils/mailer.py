import smtplib
import config


class OutletEmailSender:
    def __init__(self, created_products):
        self.sender = config.GOOGLE_EMAIL_SENDER
        self.passwod = config.GOOGLE_EMAIL_PASSWORD
        self.receivers = config.OUTLET_MAIL_RECIPIENT_LIST
        self.created_products = created_products

    def send_emails(self):
        pass
