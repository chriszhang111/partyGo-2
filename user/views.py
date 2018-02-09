from flask import Blueprint,render_template,request,session,flash,abort
from user.models import User
from user.forms import RegisterForm,LoginForm,EditForm,PasswordForm
import bcrypt
from flask import redirect,url_for
from user.decorator import login_required
from utilities.storage import upload_image_file
import bson
from party.models import Party

user_page = Blueprint('user_page', __name__)
@user_page.route('/login',methods=['GET','POST'])
def login():
  
  form = LoginForm(request.form)
  error = None
  
  if request.method == 'POST' and form.validate():
    user = User.objects.filter(email=form.email.data).first()
    if user:
      if bcrypt.checkpw(form.password.data,user.password):
        session['email'] = user.email
        session['username'] = user.name
        if request.args.get('next') != None:
          
          return redirect(request.args.get('next'))
        
        else:
          return redirect(url_for('user_page.hello',name=session['username']))
        
        
        
      else:
        flash("Wrong password")
    else:
      flash("User has not registered")
  
  return render_template('user/login.html',form=form)


@user_page.route('/hello/<name>')
@login_required
def hello(name):
  user = User.objects.filter(name=name).first()
 
  return render_template('hello.html',name=name,user=user)

@user_page.route('/password',methods=["GET","POST"])
@login_required
def password():
  user = User.objects.filter(email=session.get('email')).first()
  if user:
    error = None
    message = None
    form = PasswordForm()
    if request.method == 'POST' and form.validate():
      if bcrypt.checkpw(form.old_password.data,user.password):
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(form.new_password.data,salt)
        user.password = hash_password
        user.save()
        message = "Password updated"
      else:
        message = "Wrong old Password"
    return render_template('user/password.html',form=form,error=error,message=message)

  else:
    abort(404)
        



@user_page.route('/logout')
@login_required
def logout():
  session.pop('email')
  session.pop('username')
  return redirect(url_for('user_page.login'))


@user_page.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = User.objects.filter(email=session['email']).first()
    if user:
        error = None
        message = None
        form = EditForm(obj=user)
        
        if request.method == 'POST' and form.validate():
            if user.email != form.email.data:
                if User.objects.filter(email=form.email.data).first():
                    error = "Email is already in use"
                else:
                    session['email'] = form.email.data.lower()
            if not error:
                form.populate_obj(user)
                image_url = upload_image_file(request.files.get('image'),'proflie_image',str(user.id))
                if image_url:
                  
                  user.profile_image = image_url
                
                  
             
                
                
                user.save()
                message = "Profile updated"
                
        return render_template('user/edit.html', user=user, form=form, error=error, message=message)
    else:
        abort(404)


        
        
        
        
@user_page.route('/user/<id>/<int:page>')
@user_page.route('/user/<id>')
def profile(id,page=1):
  try:
    user = User.objects.filter(id=bson.ObjectId(id)).first()
  except bson.InvalidId:
    abort(404)
  if user:
    parties = Party.objects(attendees__in=[user],cancel=False).order_by('-start_datetime').paginate(page=page,per_page=4)
    return render_template('user/profile.html',user=user,parties=parties)
  else:
    abort(404)
@user_page.route('/signup',methods=['GET','POST'])
def signup():
  form = RegisterForm(request.form)
  if request.method == 'POST' and form.validate():
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(form.password.data,salt)
    user = User(
    name = form.name.data,
      email = form.email.data,
      password = hash_password
      
    
    )
    user.save()
    flash("Registered successfully")
    
    return redirect(url_for('user_page.login'))
    

  return render_template('user/sign.html',form=form)