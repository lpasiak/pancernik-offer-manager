import smtplib
import config
from email.message import EmailMessage
from datetime import datetime
from utils.logger import get_outlet_logger, close_outlet_logger


class OutletEmailSender:
    def __init__(self,
                 created=0,
                 lacking=0,
                 discounted=0,
                 archived=0,
                 attributes=0,
                 category_attributes=0,
                 errors=0,
                 operation_logs=''):
        self.sender = config.GOOGLE_EMAIL_SENDER
        self.passwod = config.GOOGLE_EMAIL_PASSWORD
        self.receivers = config.OUTLET_MAIL_RECIPIENT_LIST
        self.created_products = created
        self.lacking_products = lacking
        self.discounted_products = discounted
        self.archived_products = archived
        self.attributes = attributes
        self.category_attributes = category_attributes
        self.errors = errors
        self.logs = operation_logs
        self.outlet_logger = get_outlet_logger().get_logger()

    def send_emails(self):

        for email in config.OUTLET_MAIL_RECIPIENT_LIST:

            try:
                print(f'ℹ️  Sending email to {email}...')
                self.outlet_logger.info(f'ℹ️ Sending email to {email}...')

                msg = EmailMessage()
                msg['Subject'] = f'Outlety {datetime.now().strftime("%d/%m/%Y, %H:%M")}'
                msg['From'] = config.GOOGLE_EMAIL_SENDER
                msg['To'] = email
                msg.set_content(f"Created {self.created_products} outlet offers")

                html_content = config.render_outlet_email_template(
                    created=self.created_products,
                    lacking=self.lacking_products,
                    discounted = self.discounted_products,
                    archived = self.archived_products,
                    attributes = self.attributes,
                    category_attributes = self.category_attributes,
                    errors = self.errors,
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
                print(f'❌ Email sender to {email} failed. {e}')
    