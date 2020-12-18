import Project507
from flask import render_template, session, request, flash
from Project507.views.utils import login_required
import sqlite3


@Project507.app.route('/friends/', methods=['GET', 'POST'])
@login_required
def friends():
    """ Handles get and post requests to endpoint /friends/

    Parameters
    ----------

    Returns
    -------
    An HTML file rendered from the template
    """

    # initialize the flask variable and the logged user
    info = {'logname': Project507.app.config['CURRENT_USER']}

    # Connect to the database,
    # the database will automatically be closed after requests
    connection = Project507.db_config.get_db()

    if request.method == 'POST':
        if request.form.get('follow') == 'follow':
            try:
                query = r"INSERT INTO Following(user1, user2) VALUES(?, ?)"
                connection.execute(query, (info['logname'],
                                           request.form['username']))
            except sqlite3.IntegrityError:
                # handle the repeating likes link when user refreshes the page
                flash("You've followed the user.", 'success')

        elif request.form.get('unfollow') == 'unfollow':
            try:
                query = r"DELETE FROM Following WHERE user1=? AND user2=?"
                connection.execute(query, (info['logname'],
                                           request.form['username']))
            except sqlite3.IntegrityError:
                # handle the repeating unlikes link when a user
                # refreshes the page
                flash("You've unfollowed the user.", 'success')

    # get the movies crawled from WIKI
    query = """
    SELECT *, Temp2.user2 as followed FROM 
        (SELECT * FROM Users WHERE username!=?) as Temp1 
        LEFT JOIN 
        (SELECT * FROM Following WHERE user1=?) AS Temp2 
        ON Temp1.username=Temp2.user2
    """
    cur = connection.execute(query, (Project507.app.config['CURRENT_USER'],
                                     Project507.app.config['CURRENT_USER']))
    results = cur.fetchall()
    info['users'] = results

    # return render_template("index.html", **info)
    return render_template("friends.html", **info)
