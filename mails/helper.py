#coding:utf-8
import datetime
import os

def get_date(part):
    return datetime.datetime.strptime(
        part._headers[2][1][:-6], '%a, %d %b %Y %H:%M:%S')

def get_title(part):
    return part._headers[5][1]

def get_from(part):
    num_begin = part._headers[6][1].find('<') + 1
    num_end = part._headers[6][1].find('>')

    return part._headers[6][1][num_begin:num_end]

def get_to(part):
    num_begin = part._headers[7][1].find('<') + 1
    num_end = part._headers[7][1].find('>')

    return part._headers[7][1][num_begin:num_end]

def get_cont_type_file(part):
    num_end = part._headers[0][1].find(';')
    cont_t = part._headers[0][1][:num_end]

    return cont_t

def name_for_file(part, path):
    """
    Генерация имени для файла(без корреляции).
    """
    cont_t = get_cont_type_file(part)
    date_ = datetime.datetime.now()
    result = 'nakl_ot_%s' % date_.strftime('%d%m%Y')
    if cont_t == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        result = ''.join([result, '.xls'])
    if os.path.isfile(os.path.join(path, result)):
        result = ''.join(['(%s)' % id(path), result])

    return result