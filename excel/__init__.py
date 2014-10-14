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
        self.doc = xlrd.open_workbook(doc, on_demand=True)
        sheet = self.doc.sheet_by_index(0)
        number = self.get_value(sheet, 0, 1, u'№', u' от')

        self.number = number
        self.date = self.get_value(sheet, 0, 1, u'от', '')
        self.sklad = self.get_value(sheet, 0, 0, u': ', u'/')

        row_ = self.find_cell(sheet, u'Итого:')
        self.sum = self.get_value(sheet, 8, row_)
        self.sum_NDS = self.get_value(sheet, 7, row_)
        row_ = row_ + 4
        self.weight = float(self.get_value(sheet, 0, row_, u'Вес товара - ', u'кг.'))
        # self.products = self.get_products()

    def get_products(self):
        sheet = self.doc.sheet_by_index(0)
        count_row = sheet.nrows - 6
        result = []
        for rownum in range(count_row):
            if sheet.cell(rownum + 6, 0).value != '':
                arg = {}
                arg['name'] = sheet.cell(rownum + 6, 1).value
                arg['order'] = sheet.cell(rownum + 6, 2).value
                arg['count'] = sheet.cell(rownum + 6, 3).value
                arg['price_full'] = sheet.cell(rownum + 6, 4).value
                arg['price_without_NDS'] = sheet.cell(rownum + 6, 5).value
                arg['rate_NDS'] = sheet.cell(rownum + 6, 6).value
                arg['sum_NDS'] = sheet.cell(rownum + 6, 7).value
                arg['sum_with_NDS'] = sheet.cell(rownum + 6, 8).value
                ip = Product(**arg)
                if self.invoice.id is not None:
                    # if IncomingProduct.has_by_invoice(ip.name, self.invoice.id):
                    #     price_db = IncomingProduct.get_pricepay_by_name_invoice(
                    #         ip.name, self.invoice.id)
                    # else:
                    #     price_db = Product.get_pricepay_for_name(ip.norm_name())
                    if price_db:
                        ip.price_pay = price_db
                else:
                    price_db = Product.get_pricepay_for_name(ip.norm_name())
                ip.price_db = price_db
                result.append(ip)
            else:
                return result
        return result

    def find_cell(self, sheet, text):
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            if text in row:
                return rownum

    def get_value(self, sheet, col, row, mask_begin='_', mask_end='_'):
        cell = sheet.cell(row, col)
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