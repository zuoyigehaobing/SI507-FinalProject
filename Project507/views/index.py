import Project507
from flask import render_template, session, request, flash
from Project507.views.utils import login_required
import sqlite3
from Project507.views.twitter import get_twitter_content


@Project507.app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """ Handles get and post requests to endpoint /

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
    SELECT *, Movie.movieid as movieid FROM 
        Movie 
        LEFT JOIN 
        (SELECT * FROM Likes WHERE Likes.owner=?) as Temp1  
        ON Movie.movieid=Temp1.movieid 
    LIMIT 200
    """
    cur = connection.execute(query, (Project507.app.config['CURRENT_USER'], ))
    results = cur.fetchall()

    # for better displaying
    for item in results:
        item['img'] = 'https://' + item['img']
        item['bio'] = item['bio'][:380] + "..."

    # info['Torender'] = results[0]
    info['movies'] = results
    tweets_text = get_twitter_content()

    for tweet in tweets_text:
        flash("Twitter: " + tweet, 'info')

    return render_template("index.html", **info)
