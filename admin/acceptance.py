#coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext import login
from flask.ext.admin.form import Select2Field
from sqlalchemy import not_, or_
from wtforms import SelectField
from models.acceptance import Acceptance
from models import db
# from models.invoice import Invoice
from models.invoice import Invoice


class AcceptanceView(ModelView):
    form_columns = ('invoice', 'date')
    column_labels = dict(invoice=u'Накладная', date=u'Дата')
    can_delete = False

    def is_accessible(self):
        return login.current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(AcceptanceView, self).__init__(Acceptance, session, **kwargs)

    def create_form(self, obj=None):

        form = super(AcceptanceView, self).create_form(obj)

        form.invoice.query_factory = Invoice.query.outerjoin(
            Invoice.acceptance
        ).filter(
            Acceptance.invoice_id == None
        ).all

        return form

    def edit_form(self, obj=None):

        form = super(AcceptanceView, self).edit_form(obj)

        form.invoice.query_factory = Invoice.query.outerjoin(
            Invoice.acceptance
        ).filter(
            or_(
                Acceptance.invoice_id == None,
                Invoice.id == obj.invoice_id
            )

        ).all

        return form