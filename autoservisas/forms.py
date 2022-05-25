from flask_wtf import FlaskForm 
from wtforms import SubmitField, BooleanField, StringField, PasswordField, IntegerField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from autoservisas import models
# from wtforms_sqlalchemy.fields import SelectField 

MESSAGE_BAD_EMAIL = 'Neteisingas el.pašto adresas.'


class RegistracijosForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El.paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    patvirtinimas = PasswordField('Pakartokite slaptažodį', [EqualTo('slaptazodis', "Slaptažodis turi sutapti.")])
    submit = SubmitField('Prisiregistruoti')

    def tikrinti_varda(self, vardas):
        vartotojas = models.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja.Pasirinkite kitą vardą. ')
    
    def tikrinti_pasta(self, el_pastas):
        vartotojas = models.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas jūsų nurodytu el paštu jau egzistuoja. ')
        
        
class PrisijungimoForma(FlaskForm):  
    el_pastas = StringField('El.paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    prisiminti = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')
     

class ProfilioForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])  
    el_pastas = StringField('El.paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    submit = SubmitField('Atnaujinti')
    
     
    def tikrinti_varda(self, vardas):
        vartotojas = models.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja. Pasirinkite kitą vardą. ')
        
    def tikrinti_pasta(self, el_pastas):
        vartotojas = models.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistoja. ')    
        
        
class NaujoAutomobilioForma(FlaskForm):
    id = IntegerField('Automobilio id', [DataRequired()])
    marke = StringField('Markė', [DataRequired()])    
    modelis = StringField('Modelis', [DataRequired()])
    pagaminimo_metai = IntegerField('Pagaminimo metai', [DataRequired()])
    variklis = StringField('Variklis', [DataRequired()])
    valstybinis_numeris = StringField('Valstybinis numeris', [DataRequired()])
    vin_kodas = StringField('VIN kodas', [DataRequired()])
    submit = SubmitField('Išsaugoti')
    
    
class NaujoGedimoForma(FlaskForm):
    id = IntegerField('Gedimo id', [DataRequired()])
    gedimas = StringField('Gedimo pavadinimas', [DataRequired()])
    kaina = DecimalField('Kaina', [DataRequired()])
    statusas = StringField('Remonto statusas', [DataRequired()])
    submit = SubmitField('Išsaugoti')