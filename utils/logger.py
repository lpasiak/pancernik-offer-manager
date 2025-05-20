import logging
import os
import config
from datetime import datetime
import io

class HTMLFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        return f'<p>{msg}</p>'

class Logger:
    def __init__(self, name='app_logger', log_dir=config.LOGGING_DIR, log_filename='App_Logger'):
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.log_stream = io.StringIO()
        self.memory_handler = logging.StreamHandler(self.log_stream)
        self.memory_handler.setFormatter(HTMLFormatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.memory_handler)

        os.makedirs(log_dir, exist_ok=True)

        self.log_path = os.path.join(config.LOGGING_DIR, log_filename)

        self._setup_handler()

    def _setup_handler(self):
        with open(self.log_path, 'w', encoding='utf-8') as f:
            f.write(
                "<html><head><style>"
                "body { font-family: monospace; background: #f9f9f9; padding: 20px; } "
                "p { padding: 5px; margin: 0; }"
                "</style></head><body>\n"
                f"<h2>{self.name}</h2>\n"
            )

        file_handler = logging.FileHandler(self.log_path, mode='a', encoding='utf-8')  # 'a' to append
        formatter = HTMLFormatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def close(self):
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write("</body></html>")

    def get_logger(self):
        return self.logger

    def get_log_as_string(self) -> str:
        return self.log_stream.getvalue()

outlet_log_manager = None

def get_outlet_logger():
    global outlet_log_manager
    if outlet_log_manager is None:
        outlet_log_manager = Logger(
            name='Outlet Manager',
            log_filename=f'Outlet_Manager_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.html'
        )
    return outlet_log_manager

def close_outlet_logger():
    global outlet_log_manager
    if outlet_log_manager is not None:
        outlet_log_manager.close()

promo_log_manager = None

def get_promo_logger():
    global promo_log_manager
    if promo_log_manager is None:
        promo_log_manager = Logger(
            name='Promo Manager',
            log_filename=f'Promo_Manager_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.html'
        )
    return promo_log_manager

def close_promo_logger():
    global promo_log_manager
    if promo_log_manager is not None:
        promo_log_manager.close()