from datetime import datetime
from app import db

# instantiates db
class Run(db.Model):
    #header
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    operator_1 = db.Column(db.String(30), nullable=False)
    operator_2 = db.Column(db.String(30))
    date_begin = db.Column(db.Date(), nullable=False)
    date_end = db.Column(db.Date())
    final_dis = db.Column(db.String(4), nullable=False)
    
    lot_nc = db.Column(db.String(25))
    e_dat_nc = db.Column(db.Date())

    lot_vii = db.Column(db.String(20), nullable=False)
    e_dat_vii = db.Column(db.Date())

    #equipment
    bsc_id = db.Column(db.String(25))
    bsc_cdd = db.Column(db.String(7))

    pip_id = db.Column(db.String(25))
    pip_cdd = db.Column(db.String(7))

    #instrument errors
    is_ie = db.Column(db.String(5))
    errors = db.relationship('Error', backref='run_entry', lazy='dynamic')
    panels = db.relationship('Panel', backref='run_entry', lazy='dynamic')

    def __repr__(self):
        return '<Run {}>'.format(self.timestamp)

class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.String(12))
    error_type = db.Column(db.String(25))
    vii_lot = db.Column(db.String(20))
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))

class Panel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    panel_type = db.Column(db.Integer)
    panel_lot = db.Column(db.String(25))
    panel_e_dat = db.Column(db.Date())
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))