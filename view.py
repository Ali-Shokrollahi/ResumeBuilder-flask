from . import app
from . import db
from . import login_manager
from flask import render_template, request, flash, redirect, url_for, abort, jsonify
from . import forms
from . import model
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from time import sleep
import os

path = os.getcwd()
UPLOAD_FOLDER = path = os.path.join(path, "static", "users")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@login_manager.user_loader
def load_user(user_id):
    return model.User.query.get(int(user_id))


@app.route('/')
def index():  # put application's code here
    user = None
    if current_user.is_authenticated:
        user = current_user

    return render_template('index.html', user=user)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = model.User(name=form.name.data, lastname=form.lastname.data, email=form.email.data,
                              password=form.password.data)

            db.session.add(user)
            db.session.commit()
            sleep(1)

            flash("شما با موفقیت ثبت نام شدید! جهت استفاده از خدمات به سایت وارد شوید.", "تمام")
        else:
            flash("مشکلی پیش آمده، لطفا مجددا تلاش نمیایید.", "خطا")

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():

            user = model.User.query.filter_by(email=form.email.data).first()
            if user:
                if user.password != form.password.data:
                    flash("رمز عبور اشتباه است.", "pass")
                else:
                    login_user(user, remember=form.checkauth.data)
                    if current_user.point < current_user.maxpoint:
                        current_user.resumeproccess += 10
                        current_user.point += 10
                    db.session.commit()
                    return redirect(url_for('index'))
            else:

                flash("کاربری با این ایمیل یافت نشد.", "email")

    return render_template('login.html', form=form)


@app.route('/dashboard/')
def dashboard():
    return redirect('/dashboard/profile')


@app.route('/dashboard/profile', methods=["GET", "POST"])
@login_required
def profile():
    user = current_user
    form = forms.Profile()
    picform = forms.ProfilePic()

    if request.method == "POST":
        if form.validate_on_submit():
            user.name = form.name.data
            user.lastname = form.lastname.data
            user.email = form.email.data
            user.number = form.phone.data
            user.age = form.age.data
            user.job = form.job.data
            user.description = form.description.data
            user.gender = form.gender.data
            user.username = form.username.data
            if current_user.point < current_user.maxpoint:
                current_user.resumeproccess += 10
                current_user.point += 10
            db.session.commit()

    form.name.data = user.name
    form.lastname.data = user.lastname
    form.email.data = user.email
    form.phone.data = user.number
    form.age.data = user.age
    form.job.data = user.job
    form.description.data = user.description
    form.gender.data = user.gender
    form.username.data = user.username
    page = f"dashboard_forms/profile.html"

    return render_template('dashboard.html', page=page, form=form, user=user, picform=picform)


@app.route('/dashboard/experience', methods=["GET", "POST"])
@login_required
def experience():
    data = None
    user = current_user
    form1 = forms.WorkData()
    form2 = forms.Experience()
    if user.workdata:
        data = user.workdata[0]
    experiences = user.experience
    if data is not None:
        form1.time.data = data.experience
        form1.projects.data = data.projects_number
        form1.customers.data = data.customer_number

    page = f"dashboard_forms/experience.html"

    return render_template('dashboard.html', page=page, form1=form1, form2=form2, user=user, experiences=experiences)


@app.route('/dashboard/education', methods=["GET", "POST"])
@login_required
def education():
    user = current_user
    form = forms.Education()
    educations = user.education
    if request.method == "POST":
        if form.validate_on_submit():
            ed = model.Education(title=form.title.data, school=form.school.data, description=form.description.data,
                                 duration=form.duration.data,
                                 userId=current_user.id)
            db.session.add(ed)
            db.session.commit()
            massage = "با موفقیت اضافه شد"

            ed = model.Education.query.filter_by(userId=current_user.id).first()

            if ed.point < ed.maxpoint:
                current_user.resumeproccess += 5
                ed.point += 5
                db.session.commit()



        else:
            massage = "خطا در ثبت"

        return jsonify({'flash': {"text": massage}})

    page = f"dashboard_forms/education.html"
    return render_template('dashboard.html', page=page, form=form, educations=educations, user=user)


@app.route('/updateWorkData', methods=['POST'])
@login_required
def updateWorkData():
    form = forms.WorkData()
    if form.validate_on_submit():
        wk = model.WorkData.query.filter_by(userId=current_user.id).first()
        if wk:
            wk.experience = form.time.data
            wk.projects_number = form.projects.data
            wk.customer_number = form.customers.data
            db.session.commit()
        else:
            wk = model.WorkData(experience=form.time.data, projects_number=form.projects.data,
                                customer_number=form.customers.data, userId=current_user.id)
            db.session.add(wk)
            db.session.commit()
        wk = model.WorkData.query.filter_by(userId=current_user.id).first()
        if wk.point < wk.maxpoint:
            current_user.resumeproccess += 10
            wk.point += 10
            db.session.commit()

    return redirect(url_for('experience'))


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


@app.route('/addExperience', methods=['POST'])
@login_required
def addExperience():
    form = forms.Experience()
    if form.validate_on_submit():
        ex = model.Experience(title=form.title.data, company=form.company.data,
                              description=form.description.data, duration=form.duration.data, userId=current_user.id)
        db.session.add(ex)
        db.session.commit()
        massage = "با موفقیت اضافه شد"

        ex = model.Experience.query.filter_by(userId=current_user.id).order_by(model.Experience.id.desc()).first()

        if ex.point < ex.maxpoint:
            current_user.resumeproccess += 5
            ex.point += 5
            db.session.commit()
        ex = row2dict(ex)

        return jsonify({'flash': {"text": massage}, 'obj': ex})
    else:
        massage = "خطا در ثبت"

    return jsonify({'flash': {"text": massage}})


@app.route("/order", methods=["GET", "POST"])
def order():
    user = current_user
    if request.method == "POST":
        pizaa = request.form["type"]
        bread = request.form["bread"]
        size = request.form["size"]
        spices = request.form["spices"]

        order = model.order(type=pizaa, bread=bread,
                          size=size, spices=spices,user_id=current_user.id)

        db.session.add(order)
        db.session.commit()

    pizaaList=model.pizaa.query.filter_by(category="pizaa")

    return render_template("order.html",pizaaList=pizaaList)





@app.route('/dashboard/social', methods=["GET", "POST"])
@login_required
def social():
    user = current_user
    form = forms.Social()
    so = model.Social.query.filter_by(userId=user.id).first()

    if request.method == "POST":

        if form.validate_on_submit():

            if so:
                so.instagram = form.instagram.data
                so.telegram = form.telegram.data
                so.linkedin = form.linkedin.data
                so.github = form.github.data
                so.pinterest = form.pinterest.data
                db.session.commit()
            else:
                so = model.Social(instagram=form.instagram.data, telegram=form.telegram.data,
                                  linkedin=form.linkedin.data, github=form.github.data,
                                  pinterest=form.pinterest.data, userId=current_user.id)
                db.session.add(so)
                db.session.commit()

            so = model.Social.query.filter_by(userId=user.id).first()

            if so.point < so.maxpoint:
                current_user.resumeproccess += 10
                so.point += 10
                db.session.commit()

            return redirect(url_for('social'))
    if so:
        socials = user.social[0]
        form.instagram.data = socials.instagram
        form.telegram.data = socials.telegram
        form.linkedin.data = socials.linkedin
        form.github.data = socials.github
        form.pinterest.data = socials.pinterest
    page = f"dashboard_forms/social.html"
    return render_template('dashboard.html', page=page, form=form, user=current_user)


@app.route('/dashboard/skill', methods=["GET", "POST"])
@login_required
def skill():
    user = current_user
    form = forms.Skill()
    skills = user.skill
    if request.method == "POST":
        if form.validate_on_submit():
            sk = model.Skill(name=form.name.data, percent=form.percent.data,
                             userId=current_user.id)

            db.session.add(sk)
            db.session.commit()

            sk = model.Skill.query.filter_by(userId=user.id).first()

            if sk.point < sk.maxpoint:
                current_user.resumeproccess += 5
                sk.point += 5
                db.session.commit()

            return redirect(url_for('skill'))

    page = f"dashboard_forms/skill.html"
    return render_template('dashboard.html', page=page, form=form, skills=skills, user=user)


@app.route('/<username>')
def resume(username):
    user = model.User.query.filter_by(username=username).first()
    if (user is None) or (user.isallowed is False):
        abort(404)
    user.iscreated = True

    profile = user
    workdata = user.workdata[0]
    social = user.social[0]
    experience = user.experience
    education = user.education
    skill = user.skill

    return render_template('resume.html', profile=profile, workdata=workdata, social=social, experiences=experience,
                           educations=education, skills=skill)


@app.route('/dashboard/build', methods=["GET", "POST"])
@login_required
def buildResume():
    if request.method == "POST":
        print("hi")
        if current_user.iscreated == True:
            return redirect(url_for("resume", username=current_user.username))

        if current_user.resumeproccess >= 60:
            if len(current_user.username) > 3:
                current_user.isallowed = True
                db.session.commit()
                return redirect(url_for("resume", username=current_user.username))

            else:
                flash("هنوز نام کاربری ثبت نکردی!")
                return redirect(url_for("buildResume"))
        else:
            flash("امتیاز کافی نداری. می تونی با پر کردن رزومه امتیاز جمع کنی")
            return redirect(url_for("buildResume"))

    page = f"dashboard_forms/build.html"
    return render_template('dashboard.html', page=page, user=current_user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/changepic', methods=["POST"])
@login_required
def changepic():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file')
            return redirect(url_for("profile"))
        file = request.files['file']
        if file.filename == '':
            print('No file part')
            return redirect(url_for("profile"))

        if file and allowed_file(file.filename):
            ext = file.filename.split(".")
            ext = ext[len(ext) - 1]
            print(ext)
            file.filename = str(current_user.id) + f".{ext}"
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.photo = filename
            db.session.commit()
            return redirect(url_for("profile"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def E404(e):
    return "Not Found", 404
