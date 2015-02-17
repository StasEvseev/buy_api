#coding: utf-8
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import ADMINS, admin_imap, admin_pass

LOG_FILE_NAME_ERROR = "logs/error.log"
LOG_FILE_NAME_WARNING = "logs/warning.log"
LOG_FILE_NAME_DEBUG = "logs/debug.log"

def init_logging(application):
    if admin_imap and admin_pass:
        mail_handler = SMTPHandler('smtp.gmail.com',
                                   'server-error@example.com',
                                   ADMINS, 'BuyApi Failed', credentials=(admin_imap, admin_pass), secure=())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter('''
            Message type:       %(levelname)s
            Time:               %(asctime)s
            Message:
            %(message)s
        '''))
        application.logger.addHandler(mail_handler)
    rotate_handler1 = RotatingFileHandler(LOG_FILE_NAME_ERROR, maxBytes=1048576, backupCount=5)
    rotate_handler1.setLevel(logging.ERROR)
    rotate_handler1.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        # '[in %(pathname)s:%(lineno)d]'
    ))
    application.logger.addHandler(rotate_handler1)

    rotate_handler2 = RotatingFileHandler(LOG_FILE_NAME_WARNING, maxBytes=1048576, backupCount=5)
    rotate_handler2.setLevel(logging.WARNING)
    rotate_handler2.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        # '[in %(pathname)s:%(lineno)d]'
    ))
    application.logger.addHandler(rotate_handler2)

    rotate_handler3 = RotatingFileHandler(LOG_FILE_NAME_DEBUG, maxBytes=1048576, backupCount=5)
    rotate_handler3.setLevel(logging.DEBUG)
    rotate_handler3.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        # '[in %(pathname)s:%(lineno)d]'
    ))
    application.logger.addHandler(rotate_handler3)
    application.logger.setLevel(logging.DEBUG)

    # app = application

def mess(message):
    if type(message) == unicode:
        return message.encode("utf-8")
    else:
        return message

def prep_arg(*args):
    res = []
    for ar in args:
        res.append(mess(ar))
    return tuple(res)


def debug(message, *args):
    from app import app
    app.logger.debug(mess(message), *prep_arg(*args))

def warning(message, *args):
    from app import app
    app.logger.warn(mess(message), *prep_arg(*args))

def error(message, *args):
    from app import app
    import traceback
    trace = traceback.format_exc()
    app.logger.error(mess(message)+"\n"+trace , *prep_arg(*args))