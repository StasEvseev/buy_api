#coding:utf-8

import imaplib
import email as email_module
import os
from collections import namedtuple

from mails.helper import (get_title, get_date, get_from, get_to, name_for_file)
from config import (mail_folder, user_imap, user_pass, imap_server,
                    from_imap, DIR_PROJECT)

detach_dir = '.'

DIR_ATTACH = os.path.join(DIR_PROJECT, mail_folder)


class ProjectException(Exception):
    pass


class NotConnect(ProjectException):
    pass


class NotMails(ProjectException):
    pass


MailObject = namedtuple('MailObject', ['title', 'date_', 'from_', 'to_', 'file_'])

def get_mail(mail, search_str):
    mail.list()
    mail.select('inbox')
    result, data = mail.search(None, *search_str)
    return result, data

def get_count_mails(email):
    """
    функция получения количества новых писем
    """
    m, l_ids = get_ids_mails(email)
    return len(l_ids) # get the latest

def get_ids_mails(email):
    """
    Получение идентификаторов непрочитанных писем от некоего отправителя
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(user_imap, user_pass)
    except Exception as err:
        raise NotConnect(u'Нет соединения с сервером. Проверьте подключение.')
    else:
        search_str = ['UnSeen', ]
        if from_imap:
            from_str = '(FROM "%s")' % email
            search_str.append(from_str)
        result, data = get_mail(mail, search_str)

        ids = data[0] # data is a list.
        id_list = ids.split()

    return mail, id_list

def get_mails(emails):
    """
    Получение всех непрочитанных писем от некоего отправителя
    """

    results = {}

    if not os.path.exists(DIR_ATTACH):
        os.makedirs(DIR_ATTACH)

    mail = None
    try:
        for email in emails:
            results[email] = []
            mail, ids = get_ids_mails(email)
            for id in ids:
                result, data = mail.fetch(id, "(RFC822)")
                if data[0] is not None:
                    raw_email = data[0][1]

                    pmail = email_module.message_from_string(raw_email)
                    try:
                        mail_item = file_imap(pmail)
                    except Exception:
                        raise
                    # finally:
                    #     mail.close()
                    #     mail.logout()
                    results[email].append(mail_item)
    finally:
        if mail:
            mail.close()
            mail.logout()

    return ids, results

def mark_as_unseen(ids):
    """
    Помечаем письма с ids как непросмотренные
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(user_imap, user_pass)
    except Exception as err:
        raise NotConnect(u'Нет соединения с сервером. Проверьте подключение.')
    else:
        mail.select('inbox')
        for id in ids:
            mail.store(id, '-FLAGS', '\Seen')
        mail.close()
        mail.logout()

def file_imap(pmail):
    """
    Получение объекта письма.
    """
    title = get_title(pmail)
    date_ = get_date(pmail)
    from_ = get_from(pmail)
    to_ = get_to(pmail)

    for part in pmail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        print "FIND FILE - ", part.get_filename()
        fileName = part.get_filename()
        if bool(fileName):

            # filePath = os.path.join(detach_dir, mail_folder)
            fileName = name_for_file(part, DIR_ATTACH)
            filePath = os.path.join(DIR_ATTACH, fileName)
            #filePath = os.path.join(detach_dir, mail_folder, fileName)
            if not os.path.isfile(filePath):
                print fileName
            fp = open(filePath, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

            m = MailObject(title=title, date_=date_, from_=from_, to_=to_, file_=filePath)

            return m