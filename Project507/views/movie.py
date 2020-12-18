import Project507
from flask import render_template, session


@Project507.app.route('/movie/<movieid>/')
def movie(movieid):
    """ Handles get requests to endpoint /movie/<movieid>

    Parameters
    ----------
    movieid: int
        the id of a movie

    Returns
    -------
    An HTML file rendered from the template
    """

    # initialize the flask variable and the logged user
    info = {'logname': Project507.app.config['CURRENT_USER']}

    # Connect to the database,
    # the database will automatically be closed after requests
    connection = Project507.db_config.get_db()

    # get the movies crawled from WIKI
    query = "SELECT * FROM Movie WHERE movieid=?"
    cur = connection.execute(query, (movieid, ))
    results = cur.fetchall()
    info['movie'] = results[0]
    info['movie']['img'] = 'https://' + info['movie']['img']

    # get the actor and casting information about this movie
    query = """
        SELECT * FROM
        (SELECT Casting.actorid as actorid FROM 
            Movie INNER JOIN Casting 
            ON Movie.movieid=Casting.movieid 
        WHERE Movie.movieid=?) as Temp1
        INNER JOIN 
        Actor on Temp1.actorid=Actor.actorid
    """
    cur = connection.execute(query, (movieid, ))
    results = cur.fetchall()
    info['actors'] = results

    for actor in info['actors']:

        if actor['imageurl']:
            actor['imageurl'] = "https://" + actor['imageurl']

    # return render_template("index.html", **info)
    return render_template("movie.html", **info)
