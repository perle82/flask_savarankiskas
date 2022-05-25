from datetime import datetime
from sqlalchemy import DateTime
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from autoservisas import db


class Vartotojas(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column('Vartotojo vardas', db.String(200), unique=True, nullable=False)
    el_pastas = db.Column('El paštas', db.String(200), nullable=False)
    slaptazodis = db.Column('Slaptažodis', db.String(200), nullable=False)
    is_admin = db.Column('Administratorius', db.Boolean(), default=False)
    darbuotojas = db.Column('Darbuotojas', db.Boolean(), default=False)
    
    def __repr__(self):
        return self.vardas
            
            
class Automobilis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marke = db.Column('Automobilio markė', db.String(40), nullable=False)
    modelis = db.Column('Automobilio modelis', db.String(150), nullable=False)
    pagaminimo_metai = db.Column('Pagaminimo metai', db.String(50), nullable=False)
    variklis = db.Column('Variklis', db.String, nullable=False)
    valstybinis_numeris = db.Column('Valstybinis numeris', db.String(8), unique=True, nullable=False)
    vin_kodas = db.Column('VIN kodas', db.String(30), nullable=False)
    vartotojo_id = db.Column(db.Integer, db.ForeignKey('vartotojas.id'))
    vartotojas = db.relationship("Vartotojas", lazy=True)
    
    def __repr__(self):
       return self.marke
    
        
class LimitedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_accessible and current_user.is_admin
    
    
class Gedimai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gedimas = db.Column('Gedimo pavadinimas', db.String(80), nullable=False)
    kaina = db.Column('Remonto_kaina', db.Integer, nullable=False)
    statusas = db.Column('Remonto statusas', db.String(60), nullable=False)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey('vartotojas.id'))
    vartotojas = db.relationship("Vartotojas", lazy=True)
    automobilis_id = db.Column(db.Integer, db.ForeignKey('automobilis.id'))
    automobilis = db.relationship('Automobilis', lazy=True)
    
    def __repr__(self):
        return f'{self.gedimas}: {self:kaina} - {self:vartotojas}: {self:automobilis}'
    
    
class Irasas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sukurta = db.Column('Sukurta', DateTime, default=datetime.utcnow())
    suma = db.Column('Suma', db.Numeric(16,2), default=0)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey('vartotojas.id'))
    vartotojas = db.relationship("Vartotojas", lazy=True)

    def __repr__(self):
        return f'{self.suma}: {self.sukurta} @ {self.vartotojas}'