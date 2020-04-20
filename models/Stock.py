from app import db
from datetime import datetime


class StocksModel(db.Model):
    __tablename__='new_stocks'
    id=db.Column(db.Integer,primary_key=True)
    invid=db.Column(db.Integer, db.ForeignKey('new_inventories.id'),nullable=False)
    stock=db.Column(db.Integer)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    def add_stock(self):
        db.session.add(self)
        db.session.commit()
        