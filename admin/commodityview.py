#coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from models.commodity import Commodity


class CommodityView(ModelView):

    form_columns = ('name', 'thematic')
    can_delete = False

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CommodityView, self).__init__(Commodity, session, **kwargs)