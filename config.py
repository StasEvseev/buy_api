#coding: utf-8

import os

try:
    from config_local import USER
    from config_local import PASSWORD
except ImportError:
    USER = 'test'
    PASSWORD = 'test'

DATABASE_URI = 'postgresql://%s:%s@localhost:5432/buy_api' % (USER, PASSWORD)

try:
    from config_local import user_imap
    from config_local import user_pass
except ImportError:
    user_imap = ''
    user_pass = ''

imap_server = 'imap.gmail.com'
from_imap = "stasevseev@gmail.com"


DIR_PROJECT = os.path.dirname(__file__)
mail_folder = 'attachments'