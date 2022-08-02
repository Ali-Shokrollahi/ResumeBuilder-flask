from . import app
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField, \
    DateField, IntegerField, TextAreaField, FileField

from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Optional, Regexp
from .model import User


class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={"placeholder": "نام"})
    lastname = StringField(validators=[DataRequired()], render_kw={"placeholder": "نام خانوادگی"})
    email = EmailField(validators=[DataRequired()], render_kw={"placeholder": "ایمیل"})
    password = PasswordField(
        validators=[DataRequired()],

        render_kw={"placeholder": "رمز عبور"})

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("رمز عبور باید بیشتر از 8 کارکتر باشد.")

    repassword = PasswordField(validators=[DataRequired(), EqualTo('password', message="رمز عبور مطابقت ندارند.")],
                               render_kw={"placeholder": "تکرار رمز عبور"})
    submit = SubmitField("ثبت نام", render_kw={"class": "submit"})

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("این ایمیل قبلا ثبت نام کرده است.")
        else:
            pass


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired()], render_kw={"placeholder": "ایمیل"})

    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "رمز عبور"})
    checkauth = BooleanField(render_kw={"class": "checkbox"})
    submit = SubmitField("ورود", render_kw={"class": "submit  b-blue"})


class Profile(FlaskForm):
    name = StringField(validators=[DataRequired()])
    lastname = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    gender = SelectField(choices=["مرد", "زن"])
    phone = StringField(validators=[Optional(), Length(min=11)])
    job = StringField(validators=[Optional()])
    age = StringField(validators=[Optional()],
                      render_kw={"autocomplete": "off", "class": "date-picker", "id": "date-picker"})
    description = TextAreaField(validators=[Optional(), Length(min=20)],
                                render_kw={

                                    "class": "w-100",
                                    "placeholder": "توضیحاتی در رابطه ما علاقه مندی ها، شرایط همکاری، اهداف و ...",
                                })
    username = StringField(validators=[Optional()], render_kw={})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            if user.username != username.data:
                raise ValidationError("این نام کاربری وجود دارد.")
        elif username.data.isalnum() == False:
            raise ValidationError("نام کاربری تنها می تواند شامل حروف و اعداد انگلیسی باشد.")

    submit = SubmitField("بروزرسانی")


class WorkData(FlaskForm):
    time = IntegerField(validators=[DataRequired()], render_kw={"readonly": "true", "ondblclick": "dis(this)"})
    projects = IntegerField(validators=[DataRequired()], render_kw={"readonly": "true", "ondblclick": "dis(this)"})
    customers = IntegerField(validators=[DataRequired()], render_kw={"readonly": "true", "ondblclick": "dis(this)"})
    submit = SubmitField("بروزرسانی")


class Experience(FlaskForm):
    title = StringField(validators=[DataRequired(), Length(min=3)],
                        )
    company = StringField(validators=[DataRequired(), Length(min=3)],
                          )

    duration = IntegerField(validators=[DataRequired(), NumberRange(1, 40)])

    description = TextAreaField(validators=[DataRequired(), Length(min=20)],
                                render_kw={

                                    "class": "w-100", "placeholder": "تجربه کار، نوع فعالیت، علت خروج و ...",
                                })
    submit = SubmitField("بروزرسانی")


class Education(FlaskForm):
    title = StringField(validators=[DataRequired(), Length(min=3)],
                        )
    school = StringField(validators=[DataRequired(), Length(min=3)],
                         )
    description = TextAreaField(validators=[DataRequired(), Length(min=20)],
                                render_kw={

                                    "class": "w-100", "placeholder": "فعالیت های زمان تحصیل و ...",
                                })
    duration = IntegerField(validators=[DataRequired(), NumberRange(1, 12)])
    submit = SubmitField("بروزرسانی")


class Social(FlaskForm):
    instagram = StringField(validators=[Optional()], render_kw={})

    def validate_instagram(self, instagram):
        link = "https://www.instagram.com/"
        if link not in instagram.data:
            instagram.render_kw["class"] = "invalid"
            raise ValidationError("لینک نامعتبر است")
        else:
            instagram.render_kw["class"] = ""

    telegram = StringField(validators=[Optional()], render_kw={})

    def validate_telegram(self, telegram):
        link = "https://t.me/"
        if link not in telegram.data:
            telegram.render_kw["class"] = "invalid"
            raise ValidationError("لینک نامعتبر است")
        else:
            telegram.render_kw["class"] = ""

    linkedin = StringField(validators=[Optional()], render_kw={})

    def validate_linkedin(self, linkedin):
        link = "https://www.linkedin.com/in"
        if link not in linkedin.data:
            linkedin.render_kw["class"] = "invalid"
            raise ValidationError("لینک نامعتبر است")
        else:
            linkedin.render_kw["class"] = ""

    github = StringField(validators=[Optional()], render_kw={})

    def validate_github(self, github):
        if "https://github.com/" not in github.data:
            github.render_kw["class"] = "invalid"
            raise ValidationError("لینک نامعتبر است")
        else:
            github.render_kw["class"] = ""

    pinterest = StringField(validators=[Optional()], render_kw={})

    def validate_pinterest(self, pinterest):
        if "https://www.pinterest.com/" not in pinterest.data:
            pinterest.render_kw["class"] = "invalid"
            raise ValidationError("لینک نامعتبر است")
        else:
            pinterest.render_kw["class"] = ""

    submit = SubmitField("بروزرسانی")


class Skill(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=3)],
                       )
    percent = IntegerField(validators=[DataRequired(), NumberRange(5, 100)],
                           )
    submit = SubmitField("بروزرسانی")


class ProfilePic(FlaskForm):
    file = FileField(validators=[DataRequired()], render_kw={"class": "d-none"})
    submit = SubmitField("تغییر")
