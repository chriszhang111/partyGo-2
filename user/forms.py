from wtforms import Form,StringField,PasswordField,validators,ValidationError
from wtforms.fields.html5 import EmailField
from user.models import User
from wtforms.widgets import TextArea
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed

class BaseUserForm(FlaskForm):
  name = StringField('Username',[
    validators.DataRequired(),
    validators.Length(min=3,max=25),
  ])
  
  email = EmailField('Email address',[
    validators.DataRequired(),validators.Email()
  ])
  
class EditForm(BaseUserForm):
  image = FileField("Profile image",
                   validators=[FileAllowed(['jpg','jpeg','png','gif','bmp'],"Only allow .jpg .png files")])
  bio = StringField("Bio",widget=TextArea(),
                   validators=[validators.Length(max=200)])


class RegisterForm(BaseUserForm):
  
  
  password = PasswordField('New Password',[
    
    validators.DataRequired(),
    validators.EqualTo('confirm',message='Password must match'),
    validators.Length(max=80)
    
  ])
  confirm = PasswordField('Repeat password',[
    validators.Length(max=80)
  ])
  
  def validate_email(Form,field):
    if User.objects.filter(email=field.data).first():
      raise ValidationError("Email already in use")
    
    
    
class PasswordForm(FlaskForm):
  old_password = PasswordField('Old Password',[validators.DataRequired()])
  new_password = PasswordField('New Password',[validators.DataRequired(),
                                              validators.EqualTo('confirm',message="Password must match")])
  confirm = PasswordField('Confirm Password',[validators.DataRequired()])
  
class LoginForm(FlaskForm):
    email = EmailField("Email",[
      validators.DataRequired(),
      validators.Email()
    ])
    
    password = PasswordField('Password',[
      validators.DataRequired(),
      validators.Length(max=80)
    ])