#coding: utf-8

import os

try:
    from config_local import USER
    from config_local import PASSWORD
except ImportError:
    USER = 'test'
    PASSWORD = 'test'

DB = "buy_api"

COMMON_URL = 'postgresql://%s:%s@localhost:5432/%s'

DATABASE_URI = COMMON_URL % (USER, PASSWORD, DB)

try:
    from config_local import SECRET_KEY
except ImportError:
    SECRET_KEY = 'test'

try:
    from config_local import user_imap
    from config_local import user_pass
except ImportError:
    user_imap = ''
    user_pass = ''

try:
    from config_local import admin_imap
    from config_local import admin_pass
except ImportError:
    admin_imap = ""
    admin_pass = ""

try:
    from config_local import ADMINS
except ImportError:
    ADMIN = "stasevseev@gmail.com"
    ADMINS = [ADMIN]

imap_server = 'imap.gmail.com'


DIR_PROJECT = os.path.dirname(__file__)
mail_folder = 'attachments'

PATH_TO_GENERATE_INVOICE = os.path.join(DIR_PROJECT, 'static', 'files')