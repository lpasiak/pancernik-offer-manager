import smtplib
import config
from email.message import EmailMessage
from datetime import datetime

class OutletEmailSender:
    def __init__(self, created_products, logs):
        self.sender = config.GOOGLE_EMAIL_SENDER
        self.passwod = config.GOOGLE_EMAIL_PASSWORD
        self.receivers = config.OUTLET_MAIL_RECIPIENT_LIST
        self.created_products = created_products
        self.logs = logs

    def send_emails(self):
        
        try:
            print(f'ℹ️  Sending email to {config.OUTLET_MAIL_RECIPIENT_LIST[0]}...')
            msg = EmailMessage()
            msg['Subject'] = f'Outlety {datetime.now().strftime("%d/%m/%Y, %H:%M")}'
            msg['From'] = config.GOOGLE_EMAIL_SENDER
            msg['To'] = config.OUTLET_MAIL_RECIPIENT_LIST[0]
            msg.set_content(f"Created {self.created_products} outlet offers")

            html_content = config.render_outlet_email_template(
                created=self.created_products,
                operation_logs=self.logs)
            
            msg.add_alternative(html_content, subtype='html')

            # Send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(config.GOOGLE_EMAIL_SENDER, config.GOOGLE_EMAIL_PASSWORD)
                smtp.send_message(msg)

        except Exception as e:
            print('❌ Email sender failed. {e}')
        