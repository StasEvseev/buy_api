#coding:utf-8

import xlrd
import datetime
from collections import namedtuple

Product = namedtuple("Product", [
    'full_name', 'name', 'number_local', 'number_global', 'count_order', 'count_postorder', 'count',
    'price_without_NDS', 'price_with_NDS', 'sum_without_NDS', 'sum_NDS', 'rate_NDS', 'sum_with_NDS', 'thematic',
    'count_whole_pack', 'placer'], verbose=False)


class InvoiceModel(object):
    """
    Класс для работы с файлом приходной накладной.
    """
    def __init__(self, doc):

        self.count = 0
        self.start_row = 0

        self.doc = xlrd.open_workbook(doc, on_demand=True, encoding_override="cp1251")
        # self.doc.verbosity = 2
        sheet = self.doc.sheet_by_index(0)

        self.number = self.get_value(sheet, 3, 0, u'№ ', u' от')
        self.date = self.get_value(sheet, 3, 0, u'от', ' (')

        self.date = datetime.datetime.strptime(self.date, '%d.%m.%y').date()
        self.start_row = self.find_cell(sheet, u"Название издания") + 1
        row_ = self.find_cell(sheet, u'Итого:')
        self.count = row_ - self.start_row
        self.sum_without_NDS = self.get_value(sheet, row_, 7)
        self.sum_with_NDS = self.get_value(sheet, row_, 10)
        self.sum_NDS = self.get_value(sheet, row_, 9)

        row_ = row_ + 4
        self.weight = float(self.get_value(sheet, row_, 0, u'Вес товара - ', u'кг.'))

        row_ += 2
        self.responsible = self.get_value(sheet, row_, 0, u" /", u"/ ")

        assert self.number and self.date and self.sum_without_NDS and self.sum_with_NDS and self.sum_NDS and self.weight and self.responsible

    def get_products(self):
        """
        Получим все позиции приходной накладной в виде списка объектов заглушек.
        """
        sheet = self.doc.sheet_by_index(0)
        result = []
        for rownum in range(self.start_row, self.start_row + self.count):
            if sheet.cell(rownum, 0).value != '':
                full_n = sheet.cell(rownum, 1).value
                arg = {}
                arg['full_name'] = full_n
                arg['name'], arg['number_local'], arg['number_global'] = self.get_name_number(full_n)
                arg['count_order'] = int(sheet.cell(rownum, 2).value)
                arg['count_postorder'] = int(sheet.cell(rownum, 3).value)
                arg['count'] = int(sheet.cell(rownum, 4).value)
                arg['price_without_NDS'] = sheet.cell(rownum, 5).value
                arg['price_with_NDS'] = sheet.cell(rownum, 6).value
                arg['sum_without_NDS'] = sheet.cell(rownum, 7).value
                arg['rate_NDS'] = sheet.cell(rownum, 8).value.replace(' %', '')
                arg['sum_NDS'] = sheet.cell(rownum, 9).value
                arg['sum_with_NDS'] = sheet.cell(rownum, 10).value
                arg['thematic'] = sheet.cell(rownum, 11).value

                count_whole_pack = sheet.cell(rownum, 12).value
                if count_whole_pack in ['   ', '  ', ' ', ''] :
                    count_whole_pack = 0
                else:
                    count_whole_pack = int(count_whole_pack)
                arg['count_whole_pack'] = count_whole_pack
                placer = sheet.cell(rownum, 13).value
                if placer in ['']:

                    arg['placer'] = 0
                else:
                    arg['placer'] = int(placer)

                ip = Product(**arg)
                result.append(ip)
            else:
                return result
        return result

    def get_name_number(self, full_name):
        """
        Извлечь чистое имя, локальный и глобальный номера.
        """
        wt_nb = full_name.find(u"б/н")

        if wt_nb != -1:
            return full_name[:wt_nb].strip(), None, None

        st = full_name.split(u"№")
        name = st[0].strip()
        number_local = st[1].split(u"(")[0]
        number_global = self.substring(st[1], "(", ")")
        return name, number_local, number_global

    def find_cell(self, sheet, text):
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            if text in row:
                return rownum

    def get_value(self, sheet, col, row, mask_begin='_', mask_end='_'):
        cell = sheet.cell(col, row)
        value = cell.value
        if isinstance(value, float):
            return value
        result = self.substring(value, mask_begin, mask_end)
        return result

    def substring(self, string, mask_begin, mask_end):
        ind_begin = string.find(mask_begin) + len(mask_begin)
        ind_end = string.find(mask_end)
        if not ind_end:
            result = string[ind_begin:]
        else:
            result = string[ind_begin:ind_end].strip()
        return result