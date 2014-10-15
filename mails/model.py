#coding:utf-8

from models import db


class Mail(db.Model):
    __tablename__ = 'mails'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    date = db.Column(db.DateTime)
    from_ = db.Column(db.String)
    to = db.Column(db.String)
    file = db.Column(db.String)
    is_handling = db.Column(db.BOOLEAN)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship('Invoice', backref=db.backref('mails', lazy='dynamic'))

    def __init__(self, title, date, from_, to, file=None, is_handling=False):
        self.title = title
        self.date = date
        self.from_ = from_
        self.to = to
        self.file = file
        self.is_handling = is_handling

    def __repr__(self):
        return "<Mail ('%s', '%s')>" % (self.title, self.date)

    # def create(self):
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     session.add(self)
    #     session.commit()

    # @classmethod
    # def all(cls):
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     res = session.query(cls).all()
    #     return res

    # @classmethod
    # def get_by_id(cls, id):
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     res = session.query(cls).get(id)
    #     return res
#
# Mail.metadata.create_all(engine)