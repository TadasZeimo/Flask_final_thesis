from models import *
from forms import *



menu = [
    {
        'name': 'Main page',
        'url': 'index'
    },
    {
        'name': 'Registration',
        'url': 'addUsers'
    },
    {
        'name': 'Climbers',
        'url': 'climbers'
    },

    {
        'name': 'Add data about climber',
        'url': 'addClimbers'
    },
        {
        'name': 'Admin',
        'url': 'dataDB'
    },
]

@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(userName=form.userName.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.chekbox.data)
                return redirect(url_for('addClimbers'))
            else:
                flash('Username or password is incorrect!!!', category='error')
        else:
            flash('Username or password is incorrect!!!', category='error')
           
    return render_template("index.html", menu=menu, title="Main page", form=form)

        

@app.route("/climbers")
def climbers():
    dataMountersDB = Mountaineers.query.all()
    return render_template("climbers.html", menu=menu,  title="Climbers", dataMountersDB=dataMountersDB)


@app.route("/<string:title>")
def article(title):
    dataMountersDB = Mountaineers.query.all()
    return render_template("article.html", menu=menu, title=title, dataMountersDB=dataMountersDB)


# FORM add Climbers data to data base


@app.route("/addClimbers", methods=['GET', 'POST'])
@login_required
def addClimbers():
    dataMountersDB2 = Mountaineers.query.all()
    form = AddClimbers()
    if form.validate_on_submit():
        try:
            date = datetime.fromtimestamp(math.floor(time.time()))
            addDateToDB = Mountaineers(fname=form.fname.data, lname=form.lname.data, fotoUrl=form.fotoUrl.data, biography=form.biography.data, date=date)
            db.session.add(addDateToDB)
            db.session.commit()
            flash('Data sent successfully', category='success')
        except:
            flash('An error occurred while entering data into the database.', category='error')
    return render_template("addClimbers.html", menu=menu, title="Climbers", form=form, dataMountersDB2 = dataMountersDB2)

@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully disconnected', category='success')
    return redirect(url_for('index'))

# FORM add Users data to data base

@app.route("/addUsers", methods=['GET', 'POST'])
def addUsers():
    form = RegisterForm()
    if form.validate_on_submit():
        date = datetime.fromtimestamp(math.floor(time.time()))

        checkUserName = len([i for i in Users.query.filter_by(userName=form.userName.data)])
        checkEmail = len([i for i in Users.query.filter_by(email=form.email.data)])

        if form.password1.data == form.password2.data and checkUserName == 0 and checkEmail == 0:
            hashpass = generate_password_hash(form.password1.data)
            addDateToDB = Users(userName=form.userName.data, email=form.email.data, password=hashpass, date=date)
            db.session.add(addDateToDB)
            db.session.commit()
            if addDateToDB:
                flash('User registered successfully', category='success')
                return redirect(url_for('index'))
        else:
            if checkUserName > 0:
                flash(
                    'A user with this username already exists, please choose another username.', category='error')
            elif checkEmail > 0:
                flash(
                    'A user with this email already exists, please choose another email.', category='error')
            elif form.password1.data != form.password2.data:
                flash('Password mismatch!!!', category='error')

    return render_template("addUsers.html", menu=menu, title="Users", form=form)

# ----------------------------------------------------------------------------------------------------------------------------------

# ERRORS PAGES

@app.errorhandler(500)
def pageError500(error):

    return render_template("error500.html", menu=menu), 500


# ----------------------------------------------------------------------------------------------------------------------------------

# Data from DB

@app.route("/dataDB")
@login_required
def dataDB():
    id = current_user.id
    MountersDB = Mountaineers.query.all()
    UsersBD = Users.query.all()
    if id == 1:
        return render_template("dataDB.html", menu=menu,  title="Data from DB", MountersDB = MountersDB, UsersBD = UsersBD)
    else:
        return render_template("index.html", menu=menu)
    

@app.route('/deleteUser/<int:id>')
def deleteUser(id):
    deleteUser = Users.query.get_or_404(id)
    try: 
        db.session.delete(deleteUser)
        db.session.commit()
        return redirect("/dataDB")
    except:
        flash('Error', category='error')
        
@app.route('/deleteClimber/<int:id>')
def deleteClimber(id):
    deleteClimber = Mountaineers.query.get_or_404(id)
    try: 
        db.session.delete(deleteClimber)
        db.session.commit()
        return redirect("/dataDB")
    except:
        flash('Error', category='error')

@app.route("/updateUser", methods = ['GET', 'POST'])
def updateUser():
    if request.method == 'POST':
        user_data = Users.query.get(request.form.get('id'))
        user_data.userName = request.form['userName']
        user_data.email = request.form['email']
        try:
            db.session.commit()
            return redirect("/dataDB")
        except:
            flash('Error', category='error')

@app.route("/updateClimber", methods = ['GET', 'POST'])
def updateClimber():
    if request.method == 'POST':
        user_data = Mountaineers.query.get(request.form.get('id'))
        user_data.fname = request.form['fname']
        user_data.lname = request.form['lname']
        user_data.fotoUrl = request.form['fotoUrl']
        user_data.biography = request.form['biography']
        try:
            db.session.commit()
            return redirect("/dataDB")
        except:
            flash('Error', category='error')
        

# ----------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
    
