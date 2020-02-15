from flask import Flask, url_for, redirect, render_template, request, send_filefrom time import gmtime, strftime, sleep, timefrom flask_sqlalchemy import SQLAlchemyfrom flask_admin import Adminfrom flask_admin.contrib.sqla import ModelViewfrom datetime import datetime, timedelta, time, dateimport requestsimport bs4from flask_script import Managerimport jsonfrom flask_migrate import Migrateapp = Flask(__name__)app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'app.config['SECRET_KEY'] = 'f874123aa5dsf84af'db = SQLAlchemy(app)migrate = Migrate(app, db)class Kniha(db.Model):    id = db.Column(db.Integer, primary_key=True)    jmeno = db.Column(db.String(100))    hlavni_tema = db.Column(db.String(100))    casoprostor = db.Column(db.String(100))    databaze_knih = db.Column(db.String(500))    kpbo = db.Column(db.String(500))    knihy_dobrovsky = db.Column(db.String(500))    kompozice = db.Column(db.String(5000))    jazyk = db.Column(db.String(5000))    dej = db.Column(db.String(50000))    typ = db.Column(db.String(20))    maturita = db.Column(db.Boolean)    hodnoceni = db.Column(db.String(10))    datum_precteni = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)    obrazek = db.Column(db.String(2000))    dzebing = db.Column(db.String(20))    tema = db.Column(db.String(200))    motiv = db.Column(db.String(200))    kompozicni_vystavba = db.Column(db.String(200))    literarni_druh = db.Column(db.String(200))    literarni_zanr = db.Column(db.String(200))    vypravec = db.Column(db.String(200))    vypraveci_zpusoby = db.Column(db.String(200))    typy_promluv = db.Column(db.String(200))    versova_vystavba = db.Column(db.String(200))    kontext_autorovy_tvorby = db.Column(db.String(200))    literarni_kontext = db.Column(db.String(200))    autor = db.Column(db.Integer, db.ForeignKey('autor.id'))    zanr = db.Column(db.Integer, db.ForeignKey('zanr.id'))    postavy = db.relationship('Postava', backref='kniha_id', lazy=True)    def __repr__(self):        return f"('{self.jmeno}')"class Autor(db.Model):    id = db.Column(db.Integer, primary_key=True)    jmeno = db.Column(db.String(100))    kniha = db.relationship('Kniha', backref='author', lazy=True)    def __repr__(self):        return f"('{self.jmeno}')"class Postava(db.Model):    id = db.Column(db.Integer, primary_key=True)    jmeno = db.Column(db.String(100))    popis = db.Column(db.String(5000))    kniha = db.Column(db.Integer, db.ForeignKey('kniha.id'))    def __repr__(self):        return f"('{self.jmeno}')"class KnihaTR(db.Model):    id = db.Column(db.Integer, primary_key=True)    jmeno = db.Column(db.String(100))    typ = db.Column(db.String(50))    obrazek = db.Column(db.String(5000))    databaze_knih = db.Column(db.String(500))    kpbo = db.Column(db.String(500))    knihy_dobrovsky = db.Column(db.String(500))    def __repr__(self):        return f"('{self.jmeno}')"class Zanr(db.Model):    id = db.Column(db.Integer, primary_key=True)    zanr = db.Column(db.String(100))    knihy = db.relationship('Kniha', backref='zanr_id', lazy=True)    def __repr__(self):        return f"('{self.zanr}')"class Slovicko(db.Model):    id = db.Column(db.Integer, primary_key=True)    cesky = db.Column(db.String(500))    anglicky = db.Column(db.String(500))from forms import KnihaForm, KnihaTRForm, SlovickoFormadmin = Admin(app)admin.add_view(ModelView(Kniha, db.session))admin.add_view(ModelView(Autor, db.session))admin.add_view(ModelView(Postava, db.session))admin.add_view(ModelView(KnihaTR, db.session))admin.add_view(ModelView(Zanr, db.session))admin.add_view(ModelView(Slovicko, db.session))obdobi = {'Prázdniny 2019': ('2019-06-28', '2019-08-31'), 'Nižší gympl': ('2014-01-09', '2018-06-31'), 'První pololetí 5.A': ('2018-09-01', '2019-01-31'), 'Druhé polotetí 5.A': ('2019-01-31', '2019-06-28')}@app.route("/<int:typ>/<string:text>")@app.route("/<int:typ>", defaults={'text': ''})@app.route("/", defaults={'typ': 0, 'text': ''})def knihy(typ, text):    knihy = Kniha.query.order_by(Kniha.datum_precteni.desc())    if typ == 1:        knihy = Kniha.query.filter_by(hodnoceni="1").order_by(Kniha.datum_precteni.desc())    elif typ == 2:        knihy = Kniha.query.filter_by(hodnoceni="2").order_by(Kniha.datum_precteni.desc())    elif typ == 3:        knihy = Kniha.query.filter_by(hodnoceni="3").order_by(Kniha.datum_precteni.desc())    elif typ == 4:        knihy = Kniha.query.filter_by(hodnoceni="4").order_by(Kniha.datum_precteni.desc())    elif typ == 5:        knihy = Kniha.query.filter_by(hodnoceni="5").order_by(Kniha.datum_precteni.desc())    elif typ == 6:        knihy = Kniha.query.filter_by(typ="Fikce").order_by(Kniha.datum_precteni.desc())    elif typ == 7:        knihy = Kniha.query.filter_by(typ="Fakt").order_by(Kniha.datum_precteni.desc())    elif typ == 8:        knihy = Kniha.query.filter_by(typ="Těžké").order_by(Kniha.datum_precteni.desc())    elif typ == 9:        knihy = Kniha.query.filter_by(maturita=True).order_by(Kniha.datum_precteni.desc())    elif typ == 10:        knihy = Kniha.query.filter_by(maturita=False).order_by(Kniha.datum_precteni.desc())    elif typ == 11:        knihy = Kniha.query.filter_by(autor=int(text)).order_by(Kniha.datum_precteni.desc())    elif typ == 12:        knihy = Kniha.query.filter_by(zanr=int(text)).order_by(Kniha.datum_precteni.desc())    elif typ == 13:        for i in range(len(obdobi.keys())):            if text == list(obdobi.keys())[i]:                knihy = Kniha.query.filter(Kniha.datum_precteni >= list(obdobi.values())[i][0],                                           Kniha.datum_precteni <= list(obdobi.values())[i][1])                break    autors = Autor.query.all()    zanry = Zanr.query.all()    return render_template('knihy.html', link='knihy', knihy=knihy, autors=autors, zanry=zanry, obdobis=obdobi.keys())@app.route("/kniha/<int:kniha_id>")def kniha(kniha_id):    kniha = Kniha.query.filter_by(id=kniha_id).first_or_404()    postavy = Postava.query.filter_by(kniha_id=kniha)    return render_template('kniha.html', link='kniha', kniha=kniha, postavy=postavy)@app.route("/autor/<int:autor_id>")def autor(autor_id):    knihy = Kniha.query.filter_by(autor=autor_id)    return render_template('knihy.html', link='knihy', knihy=knihy)@app.route("/nova_kniha", methods=['GET', 'POST'])def nova_kniha():    form = KnihaForm()    if form.validate_on_submit():        autor = Autor.query.filter_by(jmeno=form.autor.data).first()        if not autor:            autor = Autor(jmeno=form.autor.data)            db.session.add(autor)        obrazek = form.obrazek.data        if not obrazek:            url = form.jmeno.data.replace(" ", "+")            url = 'https://www.databazeknih.cz/search?q=' + url            url = requests.get(url)            soup = bs4.BeautifulSoup(url.text)            el = 'https://www.databazeknih.cz/' + soup.select('.new_search a')[1]['href']            url = requests.get(el)            soup = bs4.BeautifulSoup(url.text)            el = soup.select('#icover_mid img')[0]['src']            obrazek = el        zanr = Zanr.query.filter_by(zanr=form.zanr.data).first()        if not zanr:            zanr = Zanr(zanr=form.zanr.data)            db.session.add(zanr)        databaze_knih = 'https://www.databazeknih.cz/search?q=' + form.jmeno.data.replace(' ', '+')        kpbo = 'https://www.okpb.cz/Opava/cs/results?q=' + form.jmeno.data.replace(' ', '+')        knihy_dobrovsky = 'https://www.knihydobrovsky.cz/vyhledavani?search=' + form.jmeno.data.replace(' ', '+')        kniha = Kniha(jmeno=form.jmeno.data, hlavni_tema=form.hlavni_tema.data, casoprostor=form.casoprostor.data,                      zanr_id=zanr, kompozice=form.kompozice.data,                      jazyk=form.jazyk.data, dej=form.dej.data, maturita=form.maturita.data, typ=form.typ.data,                      hodnoceni=form.hodnoceni.data,                      datum_precteni=form.datum_precteni.data, author=autor, obrazek=obrazek,                      databaze_knih=databaze_knih, kpbo=kpbo, knihy_dobrovsky=knihy_dobrovsky,                      tema=form.hlavni_tema.data, motiv=form.motiv.data, kompozicni_vystavba=form.kompozicni_vystavba.data, literarni_druh=form.literarni_druh.data,                      literarni_zanr=form.literarni_zanr.data, vypravec=form.vypravec.data, vypraveci_zpusoby=form.vypraveci_zpusoby.data,                      typy_promluv=form.typy_promluv.data, versova_vystavba=form.versova_vystavba.data,                      kontext_autorovy_tvorby=form.kontext_autorovy_tvorby.data, literarni_kontext=form.literarni_kontext.data                    )        if form.postava1.data:            postava = Postava(jmeno=form.postava1.data, popis=form.postava1p.data, kniha_id=kniha)            db.session.add(postava)        if form.postava2.data:            postava = Postava(jmeno=form.postava2.data, popis=form.postava2p.data, kniha_id=kniha)            db.session.add(postava)        if form.postava3.data:            postava = Postava(jmeno=form.postava3.data, popis=form.postava3p.data, kniha_id=kniha)            db.session.add(postava)        if form.postava4.data:            postava = Postava(jmeno=form.postava4.data, popis=form.postava4p.data, kniha_id=kniha)            db.session.add(postava)        if form.postava5.data:            postava = Postava(jmeno=form.postava5.data, popis=form.postava5p.data, kniha_id=kniha)            db.session.add(postava)        if form.postava6.data:            postava = Postava(jmeno=form.postava6.data, popis=form.postava6p.data, kniha_id=kniha)            db.session.add(postava)        if form.postava7.data:            postava = Postava(jmeno=form.postava7.data, popis=form.postava7p.data, kniha_id=kniha)            db.session.add(postava)        db.session.add(kniha)        delete_knihatr = KnihaTR.query.filter_by(jmeno=form.jmeno.data).first()        if delete_knihatr:            db.session.delete(delete_knihatr)        db.session.commit()        return redirect(url_for('knihy'))    now = datetime.now()    date = now.strftime("%d. %m. %Y")    obrazek = ""    jmeno = ""    if request.args.get('jmeno') is not None:        jmeno = request.args.get('jmeno')        obrazek = request.args.get('obrazek')    return render_template('nova_kniha.html', link='nova_kniha', form=form, date=date, jmeno=jmeno, obrazek=obrazek)@app.route("/knihytr")def knihytr():    fikce = KnihaTR.query.filter_by(typ='Fikce')    fakt = KnihaTR.query.filter_by(typ='Fakt')    tezke = KnihaTR.query.filter_by(typ='Těžké')    return render_template('knihytr.html', link='knihytr', fikce=fikce, fakt=fakt, tezke=tezke)@app.route("/nova_knihatr", methods=['GET', 'POST'])def nova_knihatr():    form = KnihaTRForm()    if form.validate_on_submit():        obrazek = form.obrazek.data        if not obrazek:            url = form.jmeno.data.replace(" ", "+")            url = 'https://www.databazeknih.cz/search?q=' + url            url = requests.get(url)            soup = bs4.BeautifulSoup(url.text)            el = 'https://www.databazeknih.cz/' + soup.select('.new_search a')[1]['href']            url = requests.get(el)            soup = bs4.BeautifulSoup(url.text)            el = soup.select('#icover_mid img')[0]['src']            obrazek = el        databaze_knih = 'https://www.databazeknih.cz/search?q=' + form.jmeno.data.replace(' ', '+')        kpbo = 'https://www.okpb.cz/Opava/cs/results?q=' + form.jmeno.data.replace(' ', '+')        knihy_dobrovsky = 'https://www.knihydobrovsky.cz/vyhledavani?search=' + form.jmeno.data.replace(' ', '+')        kniha = KnihaTR(jmeno=form.jmeno.data, typ=form.typ.data, obrazek=obrazek, databaze_knih=databaze_knih, kpbo=kpbo, knihy_dobrovsky=knihy_dobrovsky)        db.session.add(kniha)        db.session.commit()        return redirect(url_for('knihytr'))    return render_template('nova_knihatr.html', link='nova_knihatr', form=form)@app.route("/statistiky")def statistiky():    zanry = Zanr.query.all()    autori = Autor.query.all()    return render_template('statistiky.html', Kniha=Kniha, KnihaTR=KnihaTR, zanry=zanry, autori=autori, obdobis=obdobi, link="")@app.route("/slovicka", methods=['POST', 'GET'])def slovicka():    form = SlovickoForm()    if form.validate_on_submit():        anglicky = form.anglicky.data        url = 'https://api.mymemory.translated.net/get?q=' + anglicky + '&langpair=en|cs'        url = requests.get(url)        data = json.loads(url.text)        cesky = data['responseData']['translatedText']        slovicko = Slovicko(cesky=cesky, anglicky=anglicky)        db.session.add(slovicko)        db.session.commit()        return redirect(url_for('slovicka'))    slovicka = Slovicko.query.order_by(Slovicko.id.desc())    return render_template('slovicka.html', slovicka=slovicka, link="slovicka", form=form)@app.route("/pdf")def pdf():    book_id = request.args.get('book_id')    book = Kniha.query.filter_by(id=book_id).first_or_404()    create_pdf(book)    pdf_file = "\\" + book.jmeno.replace(" ", "_") + ".pdf"    # Download    import pathlib    path_abs = pathlib.Path().absolute()    path = str(path_abs) + str(pdf_file)    return send_file(path, as_attachment=True, cache_timeout=0)def create_pdf(book):    from reportlab.pdfgen import canvas    from reportlab.pdfbase.ttfonts import TTFont  # Font    from reportlab.pdfbase import pdfmetrics  # Font    def wrap_text(text, maximal_length):        letter_counter = 0        result = []        curr_sentence = ""        for i in text.split(" "):  # i is every word split by space in text            if curr_sentence != "":                curr_sentence += " "  # Add spaces between words            word_letters_counter = 0            for j in i:  # For each letter in word i                word_letters_counter += 1                curr_sentence += j  # Add letter to sentence on current row                letter_counter += 1  # Letter counter for line break                if letter_counter >= maximal_length and len(i) >= 6 and (                        word_letters_counter >= 4 and (len(i) - word_letters_counter) >= 4) and j not in [".", "-",                                                                                                          ","]:  # If words have reached the end of row and word is longer than 6 letters                    curr_sentence += "-"  # Add hyphen for unfinished word                    result.append(str(curr_sentence))  # Add the whole sentence to the result                    curr_sentence = ""  # Reset current sentence                    letter_counter = 0  # Reset letter count            if letter_counter >= maximal_length:  # If we reached end of row                result.append(str(curr_sentence))  # Add the whole sentence to the result                curr_sentence = ""  # Reset current sentence                letter_counter = 0  # Reset letter count        if not result:            result.append(str(curr_sentence))        elif result[-1] != curr_sentence:            result.append(str(curr_sentence))        return result    # Init PDF    pdf = canvas.Canvas(book.jmeno.replace(" ", "_") + '.pdf')    # Register fonts    pdfmetrics.registerFont(        TTFont('Ubuntu_B', 'Ubuntu-Bold.ttf'),    )    pdfmetrics.registerFont(        TTFont('Ubuntu_M', 'Ubuntu-Medium.ttf')    )    pdfmetrics.registerFont(        TTFont('Ubuntu_R', 'Ubuntu-Regular.ttf')    )    # Write title    pdf.setTitle(book.jmeno.replace(" ", "_"))    # Title    pdf.setFont('Ubuntu_B', 38)    pdf.setFillColorRGB(0.85098039215, 0.11764705882, 0.21176470588)    pdf.drawCentredString(295, 780, book.jmeno)    # Author    pdf.setFont('Ubuntu_B', 18)    pdf.setFillColorRGB(0.3294117647, 0.3294117647, 0.3294117647)    pdf.drawCentredString(295, 755, book.author.jmeno)    # Most important info    # Names    def text(text, x, y, color, font='Ubuntu_B', font_size=15):        pdf.setFont(font, font_size)        if color == 1: # Red            r = 0.85098039215            g = 0.11764705882            b = 0.21176470588        elif color == 2: # Grey            r = g = b = 0.3294117647        pdf.setFillColorRGB(r, g, b)        pdf.drawString(x, y, text)    texts = ['Téma:', 'Motivy:', 'Časoprostor:', 'Datum dočtení:', 'Literární druh:', 'Literární žánr:', 'Hlavní postavy:', 'Vypravěč:', 'Vyprávěcí způs.:', 'Typy promluv.']    for i in range(len(texts)):        text(texts[i], 30, 710-i*35, 1)    # Values    postavy = ""    postava_counter = 0    for i in book.postavy:        postavy += i.jmeno + ", "        postava_counter += 1        if postava_counter == 4:            break    postavy = postavy[:-2]    texts = [book.hlavni_tema, book.motiv, book.casoprostor, str(book.datum_precteni.strftime('%d. %m. %Y')), book.typ, book.zanr_id.zanr, postavy, book.vypravec, book.vypraveci_zpusoby, book.typy_promluv]    for i in range(len(texts)):        text(texts[i], 155, 710-i*35, 2, font="Ubuntu_M")    # Long string    def long_text(fill_text, x, y, font='Ubuntu_M', font_size=15, text_wrap=45):        pdf.setFont(font, font_size)        r = g = b = 0.3294117647        pdf.setFillColorRGB(r, g, b)        text = pdf.beginText(x, y)        res = wrap_text(fill_text, text_wrap)        lines_count = 0        for line in res:            lines_count += 1            text.textLine(line)        pdf.drawText(text)        print(lines_count)        return lines_count-2    text("Kompozice:", 30, 360, 1)    kompozice = book.kompozicni_vystavba    if not kompozice:        kompozice = book.kompozice    lines_count = long_text(kompozice, 155, 360)    text("Kontext Au. Tv.:", 30, 325-35*lines_count, 1)    lines_count += long_text(book.kontext_autorovy_tvorby, 155, 325-35*lines_count)    text("Lit. Kontext:", 30, 290-35*lines_count, 1)    long_text(book.literarni_kontext, 155, 290-35*lines_count)    # long_text(book.dej, 40, 680)    # pdf.showPage() # New page    r = 0.85098039215    g = 0.11764705882    b = 0.21176470588    pdf.setFillColorRGB(r, g, b)    pdf.rect(0, 0, 800, 28, fill=True, stroke=False)    pdf.setFillColorRGB(1, 1, 1)    pdf.drawString(10, 9, book.jmeno)    x_pos = pdf.stringWidth(book.author.jmeno, 'Ubuntu_M', 15)    pdf.drawString(580-x_pos, 9, book.author.jmeno)    pdf.save()