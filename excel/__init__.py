#coding:utf-8

import xlrd
from collections import namedtuple

# from applications.product.models import Invoice, IncomingProduct, Product

Product = namedtuple("Product", [
    'full_name', 'name', 'number', 'count_order', 'count_postorder', 'count', 'price_without_NDS',
    'price_with_NDS', 'sum_without_NDS', 'sum_NDS', 'rate_NDS', 'sum_with_NDS', 'thematic',
    'count_whole_pack', 'placer'], verbose=False)


class InvoiceModel(object):

    def __init__(self, doc):

        self.count = 0
        self.start_row = 0

        self.doc = xlrd.open_workbook(doc, on_demand=True)
        sheet = self.doc.sheet_by_index(0)

        self.number = self.get_value(sheet, 3, 0, u'№ ', u' от')
        self.date = self.get_value(sheet, 3, 0, u'от', ' (')
        #self.provider = ''
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
        sheet = self.doc.sheet_by_index(0)
        count_row = self.count
        result = []
        for rownum in range(self.start_row, self.start_row + self.count):
            if sheet.cell(rownum, 0).value != '':
                full_n = sheet.cell(rownum, 1).value
                # st = full_n.split(u" №")
                arg = {}
                arg['full_name'] = full_n
                arg['name'], arg['number'] = self.get_name_number(full_n)
                # arg['number'] = st[1].split(u"(")[0]
                arg['count_order'] = sheet.cell(rownum, 2).value
                arg['count_postorder'] = sheet.cell(rownum, 3).value
                arg['count'] = sheet.cell(rownum, 4).value
                arg['price_without_NDS'] = sheet.cell(rownum, 5).value
                arg['price_with_NDS'] = sheet.cell(rownum, 6).value
                arg['sum_without_NDS'] = sheet.cell(rownum, 7).value
                arg['sum_NDS'] = sheet.cell(rownum, 8).value
                arg['rate_NDS'] = sheet.cell(rownum, 9).value
                arg['sum_with_NDS'] = sheet.cell(rownum, 10).value
                arg['thematic'] = sheet.cell(rownum, 11).value
                arg['count_whole_pack'] = sheet.cell(rownum, 12).value
                arg['placer'] = sheet.cell(rownum, 13).value

                ip = Product(**arg)
                result.append(ip)
            else:
                return result
        return result

    def get_name_number(self, full_name):
        st = full_name.split(u" №")
        return st[0], st[1].split(u"(")[0]

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
        ind_begin = value.find(mask_begin) + len(mask_begin)
        ind_end = value.find(mask_end)
        if not ind_end:
            result = value[ind_begin:]
        else:
            result = value[ind_begin:ind_end].strip()
        return result

    # def create(self):
    #     inv = Invoice.get_by_number(number=self.invoice.number)
    #     if inv is None:
    #         self.invoice.create()
    #         inv = self.invoice
    #     for pr in self.products:
    #         pr.invoice_id = inv.id
    #         pr.create()