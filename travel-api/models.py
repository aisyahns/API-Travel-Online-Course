from app import db

class User( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pesanan = db.relationship('Pesanan', backref='buyer', lazy ='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    asal = db.Column(db.String(120))
    tujuan = db.Column(db.String(120))
    tanggal_berangkat = db.Column(db.DateTime)
    jumlah_kursi = db.Column(db.Integer)
    kursis = db.relationship('Kursi', backref='travel', lazy ='dynamic')
    
    def __repr__(self):
        return '<Travel {}>'.format(self.name)    

class Pesanan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_penumpang = db.Column(db.String(64), index=True)
    no_identitas = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'))
    kursi = db.Column(db.Integer, db.ForeignKey('kursi.id'))

    def __repr__(self):
        return '<Pesanan {}>'.format(self.name)  

class Kursi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    pesanan = db.relationship('Pesanan', backref='kursi', lazy ='dynamic')
    travels = db.Column(db.Integer, db.ForeignKey('travel.id'))

    def __repr__(self):
        return '<Kursi {}>'.format(self.id)

