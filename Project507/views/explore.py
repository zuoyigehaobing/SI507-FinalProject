import Project507
from flask import render_template, session, request, flash
from Project507.views.utils import login_required
import sqlite3


@Project507.app.route('/explore/', methods=['GET', 'POST'])
@login_required
def explore():

    # initialize the flask variable and the logged user
    info = {'logname': Project507.app.config['CURRENT_USER']}

    # Connect to the database,
    # the database will automatically be closed after requests
    connection = Project507.db_config.get_db()

    # Handle the post request
    if request.method == 'POST':
        if request.form.get('like') == 'like':
            try:
                query = r"INSERT INTO Likes(owner, movieid) VALUES(?, ?)"
                connection.execute(query, (info['logname'],
                                           request.form['movieid']))
            except sqlite3.IntegrityError:
                # handle the repeating likes link when user refreshes the page
                flash("You've liked this movie.", 'success')

        elif request.form.get('unlike') == 'unlike':
            try:
                query = r"DELETE FROM likes WHERE owner=? AND movieid=?"
                connection.execute(query, (info['logname'],
                                           request.form['movieid']))
            except sqlite3.IntegrityError:
                # handle the repeating unlikes link when a user
                # refreshes the page
                flash("You've unliked this movie.", 'success')

    # get the movies crawled from WIKI
    query = """
    SELECT *, Temp4.movieid as movieid, Temp5.owner as liked 
    FROM 
    (SELECT * FROM 
        (SELECT * FROM 
            (SELECT user2 as username FROM Following WHERE user1=?) AS Temp1 
            INNER JOIN Likes on Likes.owner=Temp1.username) AS Temp3 
            INNER JOIN Movie on Movie.movieid=Temp3.movieid) 
        AS Temp4 LEFT JOIN (SELECT * FROM Likes WHERE owner=?) 
    AS Temp5 on Temp4.movieid=Temp5.movieid
    """
    cur = connection.execute(query, (Project507.app.config['CURRENT_USER'],
                                     Project507.app.config['CURRENT_USER']))
    results = cur.fetchall()

    # for better displaying
    for item in results:
        item['img'] = 'https://' + item['img']
        item['bio'] = item['bio'][:380] + "..."

    info['movies'] = results

    return render_template("explore.html", **info)
