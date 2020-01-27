from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField


class KnihaForm(FlaskForm):
    jmeno = StringField()
    hlavni_tema = StringField()
    casoprostor = StringField()
    zanr = StringField()
    kompozice = TextAreaField()
    jazyk = TextAreaField()
    dej = TextAreaField()
    maturita = BooleanField()
    typ = SelectField(choices=[('Fikce', 'Fikce'), ('Fakt', 'Fakt'), ('Těžké', 'Těžké')])
    hodnoceni = SelectField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    datum_precteni = DateField(format='%d. %m. %Y')
    autor = StringField()

    tema = StringField()
    motiv = StringField()
    kompozicni_vystavba = StringField()
    literarni_druh = StringField()
    literarni_zanr = StringField()
    vypravec = StringField()
    vypraveci_zpusoby = StringField()
    typy_promluv = StringField()
    versova_vystavba = StringField()
    kontext_autorovy_tvorby = StringField()
    literarni_kontext = StringField()

    postava1 = StringField()
    postava1p = TextAreaField()
    postava2 = StringField()
    postava2p = TextAreaField()
    postava3 = StringField()
    postava3p = TextAreaField()
    postava4 = StringField()
    postava4p = TextAreaField()
    postava5 = StringField()
    postava5p = TextAreaField()
    postava6 = StringField()
    postava6p = TextAreaField()
    postava7 = StringField()
    postava7p = TextAreaField()
    obrazek = StringField()
    submit = SubmitField('Uložit')


class KnihaTRForm(FlaskForm):
    jmeno = StringField()
    typ = RadioField(choices=[('Fikce', 'Fikce'), ('Fakt', 'Fakt'), ('Těžké', 'Těžké')])
    obrazek = StringField()
    submit = SubmitField()


class SlovickoForm(FlaskForm):
    anglicky = StringField()
    submit = SubmitField()
