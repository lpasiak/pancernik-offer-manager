import smtplib
import config
from email.message import EmailMessage
from datetime import datetime
from utils.logger import get_outlet_logger, get_promo_logger


class OutletEmailSender:
    def __init__(self, **kwargs):
        self.sender = config.GOOGLE_EMAIL_SENDER
        self.password = config.GOOGLE_EMAIL_PASSWORD
        self.receivers = config.OUTLET_MAIL_RECIPIENT_LIST
        self.created_products = kwargs.get('created', 0)
        self.lacking_products = kwargs.get('lacking', 0)
        self.discounted_products = kwargs.get('discounted', 0)
        self.redirects_removed = kwargs.get('redirects_removed', 0)
        self.archived_products = kwargs.get('archived', 0)
        self.activated_products = kwargs.get('activated', 0)
        self.deactivated_products = kwargs.get('deactivated', 0)
        self.attributes = kwargs.get('attributes', 0)
        self.category_attributes = kwargs.get('category_attributes', 0)
        self.errors = kwargs.get('errors', 0)
        self.outlet_logger = get_outlet_logger().get_logger()


    def send_emails(self):

        for email in self.receivers:

            try:
                print(f'ℹ️  Sending email to {email}...')
                self.outlet_logger.info(f'ℹ️ Sending email to {email}...')

                msg = EmailMessage()
                msg['Subject'] = f'Outlety {datetime.now().strftime("%d/%m/%Y, %H:%M")}'
                msg['From'] = self.sender
                msg['To'] = email
                msg.set_content(f"Created {self.created_products} outlet offers")

                html_content = config.render_outlet_email_template(
                    created=self.created_products,
                    lacking=self.lacking_products,
                    discounted = self.discounted_products,
                    redirects_removed = self.redirects_removed,
                    archived = self.archived_products,
                    activated = self.activated_products,
                    deactivated = self.deactivated_products,
                    attributes = self.attributes,
                    category_attributes = self.category_attributes,
                    errors = self.errors)
                
                msg.add_alternative(html_content, subtype='html')

                try:
                    log_file_path = get_outlet_logger().log_path
                    log_filename = get_promo_logger().log_filename

                    with open(log_file_path, 'rb') as f:
                        file_data = f.read()

                    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=log_filename)

                except Exception as e:
                    print(f'❌ Failed to attach log file: {e}')

                # Send the email
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(self.sender, self.password)
                    smtp.send_message(msg)

            except Exception as e:
                print(f'❌ Email sender to {email} failed. {e}')
    

class PromoEmailSender:
    def __init__(self,
                 created_promo_allegro=0,
                 ommited_promo_allegro=0,
                 removed_promo_allegro=0,
                 ommited_promo_allegro_early=0,
                 discounts_failed=0,
                 errors=0,
                 operation_logs=''):
        
        self.sender = config.GOOGLE_EMAIL_SENDER
        self.password = config.GOOGLE_EMAIL_PASSWORD
        self.receivers = config.PROMO_MAIL_RECIPIENT_LIST
        self.created_promo_allegro = created_promo_allegro
        self.ommited_promo_allegro = ommited_promo_allegro
        self.removed_promo_allegro = removed_promo_allegro
        self.ommited_promo_allegro_early = ommited_promo_allegro_early
        self.discounts_failed = discounts_failed
        self.errors = errors
        self.logs = operation_logs
        self.promo_logger = get_promo_logger().get_logger()

    def send_emails(self):

        for email in self.receivers:

            try:
                print(f'ℹ️  Sending email to {email}...')
                self.promo_logger.info(f'ℹ️ Sending email to {email}...')

                msg = EmailMessage()
                msg['Subject'] = f'Promocje {datetime.now().strftime("%d/%m/%Y, %H:%M")}'
                msg['From'] = self.sender
                msg['To'] = email
                msg.set_content(f"Created {self.created_promo_allegro} promo offers.")

                html_content = config.render_promo_email_template(
                    created_promo_allegro=self.created_promo_allegro,
                    ommited_promo_allegro=self.ommited_promo_allegro,
                    removed_promo_allegro = self.removed_promo_allegro,
                    ommited_promo_allegro_early = self.ommited_promo_allegro_early,
                    discounts_failed = self.discounts_failed,
                    errors = self.errors)
                
                msg.add_alternative(html_content, subtype='html')

                try:
                    log_file_path = get_promo_logger().log_path
                    log_filename = get_promo_logger().log_filename

                    with open(log_file_path, 'rb') as f:
                        file_data = f.read()
                        
                    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=log_filename)

                except Exception as e:
                    print(f'❌ Failed to attach log file: {e}')
                
                # Send the email
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(self.sender, self.password)
                    smtp.send_message(msg)

            except Exception as e:
                print(f'❌ Email sender to {email} failed. {e}')
