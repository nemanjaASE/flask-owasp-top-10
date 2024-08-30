import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from flask import request

class EntityLogger:
    def __init__(self, app=None, log_file='entity.log', max_bytes=1024*1024, backup_count=5):
        self.logger = logging.getLogger('entity')
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            self.log_file, maxBytes=self.max_bytes, backupCount=self.backup_count
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)

    def log_entity_not_found(self, msg):
        self.logger.warning(
            f"Entity not found: {msg} at {datetime.now().isoformat()}. "
            f"IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}. "
            f"URL: {request.url}. Endpoint: {request.endpoint}"
        )