from datetime import datetime
from flask import render_template, redirect, url_for, flash, request 
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin.contrib.sqla import ModelView
from autoservisas.models import Automobilis, Gedimai, Vartotojas, Irasas
from autoservisas import forms
from autoservisas import app, db, admin


class AutoservisoAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


admin.add_view(AutoservisoAdminView(Vartotojas, db.session))
admin.add_view(AutoservisoAdminView(Automobilis, db.session))
bcrypt = Bcrypt(app)


@app.route("/admin")
@login_required
def admin():
    return redirect(url_for(admin))


@app.route('/')
def home():
    flash('Sveiki atvykę, žinutės praeina', 'info')
    return render_template('base.html', current_user=current_user)


@app.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if current_user.is_authenticated:
        flash('Atsijunkite, kad priregistruoti naują vartotoją.')
        return redirect(url_for('home'))
    form = forms.RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        is_admin = not Vartotojas.query.first()
        naujas_vartotojas = Vartotojas(
            vardas = form.vardas.data,
            el_pastas = form.el_pastas.data,
            slaptazodis = koduotas_slaptazodis,
            is_admin = is_admin
        )
        db.session.add(naujas_vartotojas)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        return redirect(url_for('home'))
    return render_template('registracija.html', form=form, current_user=current_user)


@app.route('/prisijungimas', methods=['GET', 'POST'])
def prisijungimas():
    next_page = request.args.get('next')
    if current_user.is_authenticated:
        flash('Vartotojas jau prisijungęs. Atisjunkite ir bandykite iš naujo.')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
        flash('Prisijungti nepavyko, neteisingas el.paštas arba slaptažodis.', 'danger')
    return render_template('prisijungimas.html', form=form, current_user=current_user)

@app.route('/atsijungimas')
def atsijungimas():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))


@app.route('/profilis', methods=['GET', 'POST'])
@login_required
def profilis():
    form = forms.ProfilioForma()
    if form.validate_on_submit():
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        db.session.commit()
        flash('Profilis atnaujintas!', 'success')
        return redirect(url_for('profilis'))
    elif request.method == "GET":
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas     
    return render_template('profilis.html', current_user=current_user, form=form)


@app.route('/naujas_automobilis', methods=['GET', 'POST'])
@login_required
def naujas_automobilis():
    form = forms.NaujoAutomobilioForma()
    if form.validate_on_submit():
        print(current_user.id)
        naujas_automobilis = Automobilis(
            # id = form.id.data,
            marke = form.marke.data,
            modelis = form.modelis.data,
            pagaminimo_metai = form.pagaminimo_metai.data,
            variklis = form.variklis.data,
            valstybinis_numeris = form.valstybinis_numeris.data,
            vin_kodas = form.vin_kodas.data,
            vartotojo_id = current_user.id
            )
        db.session.add(naujas_automobilis)
        db.session.commit()
        print('registracija pavyko')
        flash('Automobilis užregistruotas', 'success')
        return redirect(url_for('home'))
    return render_template('naujas_automobilis.html', current_user=current_user, form=form)


@app.route('/gedimas', methods=['GET', 'POST'])
@login_required
def gedimas():
    form = forms.NaujoGedimoForma()
    if form.validate_on_submit():
        print(current_user.id)
        naujas_gedimas = Gedimai(
        id = form.id.data,
        gedimas = form.gedimas.data,
        kaina = form.kaina.data,
        statusas = form.statusas.data
        )
        db.session.add(naujas_gedimas)
        db.session.commit()
        flash('Gedimas užregistruotas', 'success')
        return redirect(url_for('gedimas'))  
    return render_template('gedimas.html', current_user=current_user, form=form)


@app.route('/irasai')
@login_required
def records():
    page = request.args.get('page', 1, type=int)
    visi_irasai = Irasas.query.filter_by(vartotojas_id=current_user.id).order_by(Irasas.sukurta.desc()).paginate(page=page, per_page=5)
    return render_template("irasai.html", visi_irasai=visi_irasai, datetime=datetime)

