import Project507
from flask import render_template, request, flash, session, redirect, url_for
from Project507.views.utils import get_session_user


@Project507.app.route('/login/', methods=['GET', 'POST'])
def login():

    info = {}

    # Connect to the database, the database will automatically be closed after requests
    connection = Project507.db_config.get_db()

    # check if already logged in, redirect to / if true
    if get_session_user(connection):
        return redirect(url_for('index'))

    # Handle the post request
    if request.method == 'POST':
        username = request.form['username']
        raw_password = request.form['password']

        # get the username and password from db
        query = "SELECT password FROM users WHERE username=?"
        cur = connection.execute(query, (username, ))
        user_pass_db = cur.fetchall()

        # warn if the user does not exist
        if not user_pass_db:
            flash("No such user", "danger")
        
        # check the password
        elif raw_password == user_pass_db[0]['password']:
            session['username'] = username
            Project507.app.config['CURRENT_USER'] = username
            return redirect(url_for('index'))
        else:
            flash("username or password incorrect", 'danger')

    return render_template("login.html", **info)


@Project507.app.route('/signup/', methods=['GET', 'POST'])
def signup():

    info = {}

    # Connect to the database, the database will automatically be closed after requests
    connection = Project507.db_config.get_db()

    # check if already logged in, redirect to / if true
    if get_session_user(connection):
        return redirect(url_for('index'))

    # Handle the post request
    if request.method == 'POST':

        # get the name, the  username, email, and raw passwords out of the forms
        name = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        user_pass = request.form['password']

        # need the user to fullfill every fields
        if not name or not username or not email or not user_pass:
            flash("Error, please fill all of the forms in below", 'danger')
            return render_template("signup.html", **info)
        
        # check the existence of the user in the database
        query = "SELECT username FROM Users WHERE username = ?"
        cur = connection.execute(query, (username, ))
        check_username = cur.fetchall()

        if check_username:
            flash("Username already exists, please use another one", 'danger')
            return render_template("signup.html", **info)
        
        # add the user to the database and session
        query = r"INSERT INTO users(username, fullname, email, password) VALUES (?, ?, ?, ?)"
        connection.execute(query, (username, name, email, user_pass))
        session['username'] = username
        Project507.app.config['CURRENT_USER'] = username
        return redirect(url_for('index'))


    return render_template("signup.html", **info)


@Project507.app.route('/logout/', methods=['GET'])
def logout():

    connection = Project507.db_config.get_db()

    # check if already logged in, redirect to / if true
    username = get_session_user(connection)
    
    # If the user haven't signed in
    if not username:
        return redirect(url_for('login'))
    
    session['username'] = None
    Project507.app.config['CURRENT_USER'] = None
    return redirect(url_for('login'))