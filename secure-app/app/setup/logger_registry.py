from app.logger import *

def register_loggers(app):
    app.security_logger = SecurityLogger(app, log_file='app/logs/security.log', max_bytes=1024*1024, backup_count=5)
    app.entity_logger = EntityLogger(app, log_file='app/logs/entity.log', max_bytes=1024*1024, backup_count=5)