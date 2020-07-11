from flask import Flask, render_template, url_for, flash, request
from pack.forms import RegistrationForm, LoginForm, SearchForm, RegionForm, ContactForm ,FusionForm ,MethylForm
from pack import app, bcrypt
from flask_login import login_user, current_user, logout_user
from datetime import datetime
from pack.models import User,Feedback
from pack import db, bcrypt, app
from flask import redirect
from datetime import date
from flask import flash
# from flask import request
import happybase
import datetime
import os
connection = happybase.Connection('127.0.0.1')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    def calculateAge(birthDate):
        days_in_year = 365.2425
        age = int((date.today() - birthDate).days / days_in_year)
        return age

    if form.validate_on_submit():

        az = calculateAge(form.dob.data)
        print(form.username.data)
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user3 = User(username=form.username.data, password=hashed_pwd, email=form.email.data, phone=form.phone_no.data,
                     age=az)
        db.session.add(user3)
        db.session.commit()
        flash("User is created.Now user can login",'success')
        print("registered")
        return render_template("login.html",form=LoginForm() , title='Login')
        # return redirect(url_for('login-page'))
    else:
        print("Form me galti hai")
        flash("Check the details and register", 'danger')

    return render_template('register.html', form=form, title='register')


@app.route('/', methods=['GET', 'POST'])
@app.route('/homepage')
def homepage():
    return render_template('homepage.html', title='Home')


@app.route('/about')
def about():
    return render_template('about_us.html', title='About')


@app.route('/graph')
def graph():
    return render_template('graph.html', title='Graph')


@app.route('/analysis')
def analysis():
    return render_template('analysis.html', title='Analysis')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("user_logged in")
            print(user.is_authenticated)
            login_user(user)
            # return redirect(url_for('account'))
            #flash("login successful", "success")
            return render_template('homepage.html', title='Admin')

        else:
            #flash("Login error", 'danger')
            print("galti hau")
    return render_template('login.html', form=form, title='login')

@app.route('/download')
def download():
    x=os.getcwd()
    return render_template('download.html', os=os,x=x)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route('/first')
# def first():
#

@app.route('/first')
def first():
    return render_template('first.html')


@app.route('/variant', methods=['GET', 'POST'])
def variant():
    form = SearchForm()
    print("asdgvj")
    if request.method == 'POST':
        table = connection.table('fusionasa3')
        print('Table Connected')
        chrno = str(form.chr.data)
        st = int(form.start.data)
        en = int(form.end.data)
        vtype = str(form.var_type.data)
        res = ""
        l = list()
        s = set()
        count=0
        for key, data in table.scan():

            if int(data['variants_info:start']) >= en:
                print('end')
            cn = data['variants_info:chr']
            if cn != chrno:
                continue
            print('inside')
            if int(data['variants_info:start']) in range(st, en) and int(data['variants_info:end']) in range(st, en):
                try:
                    z = data['variants_info:variant_subtype']
                except:
                    # print('Some exception :KEy not found')
                    continue

                if z == vtype:
                    count = count + 1
                    # print(data['variants_info:variant_subtype'])
                    # print(data)
                    # print(key)
                    line = str(data)
                    res = res + str(data) + "\n"
                    words = line[1:len(line) - 2]
                    words = words.split(',')
                    d = dict()
                    for word in words:
                        word = word.strip()
                        k, v = word.split("':")
                        k = k.strip()
                        k = k[1:len(k)]
                        v = v.strip()
                        v = v[1:len(v)]
                        v = v.split("'")
                        d[k] = v[0]
                        s.add(k)
                    l.append(d)
        s = list(s)
        if len(res) < 1:
            res = "No match found"
            form.output.data=res
            print('No result found')
        else:
            return render_template('result.html', l=l, s=s)

    else:
        print("Something fishy in search form")

    return render_template('variant.html', form=form, title='Variant wise search')


@app.route('/region', methods=['GET', 'POST']) #disease
def region():
    form = SearchForm()
    print("asdgvj")
    if request.method == 'POST':
        table = connection.table('fusionasa3')
        print('table connected')
        chrno = str(form.chr.data)
        st = int(form.start.data)
        en = int(form.end.data)
        disease = form.var_type.data
        res = ""
        l = list()
        s = set()
        count = 0
        for key, data in table.scan():
            cn = data['variants_info:chr']
            k=key
            k=k.split(':')

            if (cn != chrno):
                continue
            if int(data['variants_info:start']) in range(st, en) and int(data['variants_info:end']) in range(st, en):
                try:
                    z = data['genes_info:disease']
                except:
                    # print('Some exception :KEy not found')
                    continue

                if z == disease:
                    print(key)
                    count = count + 1
                    print(data['genes_info:disease'])
                    line = str(data)
                    res = res + str(data) + "\n"
                    words = line[1:len(line) - 2]
                    words = words.split(',')
                    d = dict()
                    for word in words:
                        word = word.strip()
                        k, v = word.split("':")
                        k = k.strip()
                        k = k[1:len(k)]
                        v = v.strip()
                        v = v[1:len(v)]
                        v = v.split("'")
                        d[k] = v[0]
                        s.add(k)
                    l.append(d)
                s = list(s)
        if len(res) < 1:
            res = "No match found"
            form.output.data = res
            print('No result found')
        else:
            return render_template('result.html', l=l, s=s)
    else:
        print("Something fishy in search form")

    return render_template('region.html', form=form, title='Region wise search')


@app.route('/category', methods=['GET', 'POST'])
def gene():
    form = SearchForm()
    print("asdgvj")
    if request.method == 'POST':
        table = connection.table('fusionasa3')
        print('table connected')
        chrno = str(form.chr.data)
        st = int(form.start.data)
        en = int(form.end.data)
        vtype = str(form.var_type.data)
        res = ""
        l = list()
        s = set()
        for key, data in table.scan():
            cn = data['variants_info:chr']
            if (cn > chrno):
                break
            if (cn != chrno):
                continue
            print('inside')
            if int(data['variants_info:start']) in range(st, en) and int(data['variants_info:end']) in range(st, en):
                z = data['genes_info:gene_name']
                if z == vtype:
                    print(data['genes_info:gene_'])
                    count = count + 1
                    line = str(data)
                    res = res + str(data) + "\n"
                    words = line[1:len(line) - 2]
                    words = words.split(',')
                    d = dict()
                    for word in words:
                        word = word.strip()
                        k, v = word.split("':")
                        k = k.strip()
                        k = k[1:len(k)]
                        v = v.strip()
                        v = v[1:len(v)]
                        v = v.split("'")
                        d[k] = v[0]
                        s.add(k)
                    l.append(d)
                s = list(s)
                if len(res) < 1:
                    res = "No match found"
                    form.output.data = res
                    print('No result found')
                else:
                    return render_template('result.html', l=l, s=s)
    else:
        print("Something fishy in search form")

    return render_template('category.html', form=form, title='Category wise search')


@app.route('/gene', methods=['GET', 'POST'])
def category():
    form = SearchForm()
    print("asdgvj")
    if request.method == 'POST':
        dt_started = datetime.datetime.utcnow()
        table = connection.table('fusionasa3')
        print("Table connected")
        count=0
        chrno = str(form.chr.data)
        st = int(form.start.data)
        en = int(form.end.data)
        vtype = str(form.var_type.data)
        res = ""
        z=''
        l = list()
        s = set()
        # test = key.split(':')
        for key, data in table.scan():
            if count==10:
                break
            if (int(data['variants_info:start']) >= en):
                continue
            cn = data['variants_info:chr']
            if (cn > chrno):
                break
            if (cn != chrno):
                continue
            if int(data['variants_info:start']) in range(st, en) and int(data['variants_info:end']) in range(st, en):
                try:
                    z = data['genes_info:genes_symbol']
                except:
                    print 'Key Error:Key not in record'
                    continue
                if z == vtype:
                    print(data['genes_info:gene_type'])
                    print(vtype)
                    count=count+1
                    line = str(data)
                    # res = res + str(data) + "\n"
                    words = line[1:len(line) - 2]
                    words = words.split(',')
                    d = dict()
                    for word in words:
                        word = word.strip()
                        k, v = word.split("':")
                        k = k.strip()
                        k = k[1:len(k)]
                        v = v.strip()
                        v = v[1:len(v)]
                        v = v.split("'")
                        d[k] = v[0]
                        s.add(k)
                    l.append(d)
        s = list(s)
        if count== 0:
            res = "No match found"
            form.output.data=res
        else:
            return render_template('result.html', l=l, s=s,count=count,dt_started = dt_started)

                    # res = res + str(data) + "\n"
        # form.output.data = res

    else:
        print("Something fishy in search form")

    return render_template('gene.html', form=form, title='Gene-Symbol search')


@app.route('/contact', methods=['GET','POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        user4 = Feedback(fname=form.fname.data, lname = form.lname.data,  country=form.country.data ,
                         email=form.email.data,message=form.message.data)
        db.session.add(user4)
        db.session.commit()
        # flash(f"User is created.Now user can login",'success')
        print("Message sent successfully")
        return render_template("homepage.html", title='Homepage')
        # return redirect(url_for('login-page'))
    else:
        print("Cannot sent feedback")
        flash("Check the details and message again", 'danger')
    return render_template('contact.html', form=form,title='Contact')





@app.route('/epigen_methyl', methods=['GET', 'POST'])
def epigen_methyl():
    form = MethylForm()
    print("asdgvj")
    if request.method == 'POST':
        table = connection.table('epigdb')
        print('table connected')
        st = int(form.start.data)
        en = int(form.end.data)
        l = list()
        s = set()
        res=""
        count = 0
        for key, data in table.scan():
            print(key)
            print(data);
            if int(data['cf1:start']) in range(st, en) and int(data['cf1:end']) in range(st, en):
                print(key)
                count = count + 1
                print(data)
                print(key)
                line = str(data)
                res = res + str(data) + "\n"
                words = line[1:len(line) - 2]
                words = words.split(',')
                d = dict()
                for word in words:
                    word = word.strip()
                    k, v = word.split("':")
                    k = k.strip()
                    k = k[1:len(k)]
                    v = v.strip()
                    v = v[1:len(v)]
                    v = v.split("'")
                    d[k] = v[0]
                    s=set(s)
                    s.add(k)
                l.append(d)
                s = list(s)
        if len(res) < 1:
            res = "No match found"
            form.output.data = res
            print('No result found')
        else:
            return render_template('result.html', l=l, s=s)
    else:
        print("Something fishy in search form")

    return render_template('methyl.html', form=form, title='Methyl wise search')



@app.route('/epigen_fusion', methods=['GET', 'POST'])
def epigen_fusion():
    form = FusionForm()
    print("asdgvj")
    if request.method == 'POST':
        table = connection.table('fusiopedia')
        print('table connected')
        hgene = form.h_gene.data
        l = list()
        s = set()
        res=""
        count = 0
        for key, data in table.scan():
            if data['genes_info:h_gene'] == hgene :
                print(key)
                count = count + 1
                print(data)
                print(key)
                line = str(data)
                res = res + str(data) + "\n"
                words = line[1:len(line) - 2]
                words = words.split(',')
                d = dict()
                for word in words:
                    word = word.strip()
                    k, v = word.split("':")
                    k = k.strip()
                    k = k[1:len(k)]
                    v = v.strip()
                    v = v[1:len(v)]
                    v = v.split("'")
                    d[k] = v[0]
                    s = set(s)
                    s.add(k)
                l.append(d)
        s=list(s)
        r =s[1],s[8],s[6],s[13],s[10]
        r=list(r)
        if len(res) < 1:
            res = "No match found"
            form.output.data = res
            print('No result found')
        else:
            return render_template('result.html', l=l, s=r)
    else:
        print("Something fishy in search form")

    return render_template('fusion.html', form=form, title='Fusiongene wise search')


@app.route('/epigenomic', methods=['GET', 'POST'])
def epigenomic():
    return render_template(('epigenomic.html'));
