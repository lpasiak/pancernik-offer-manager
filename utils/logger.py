import logging
import os
import config
from datetime import datetime

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

_outlet_log_manager = None

def get_outlet_logger():
    global _outlet_log_manager
    if _outlet_log_manager is None:
        _outlet_log_manager = Logger(
            name='Outlet Manager',
            log_filename=f'Outlet_Manager_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.html'
        )
    return _outlet_log_manager.get_logger()

def close_outlet_logger():
    if _outlet_log_manager is not None:
        _outlet_log_manager.close()