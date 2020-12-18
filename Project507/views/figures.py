import Project507
from flask import render_template, session, request, flash, Response
from Project507.views.utils import login_required
import sqlite3
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


@Project507.app.route('/figures/', methods=['GET'])
@login_required
def figure_plot():
    """ Handles get requests to endpoint /figures/

    Parameters
    ----------

    Returns
    -------
    An HTML file rendered from the template
    """

    info = {"logname": Project507.app.config['CURRENT_USER']}

    return render_template("plot.html", **info)


@Project507.app.route('/plot.png', methods=['GET'])
@login_required
def figures():
    """ Handles get and post requests to endpoint /plot.png/. The figure is
    the an matplotlib figure where the x axis indicates the months and the
    y axis indicates how many movies are released on that month

    Parameters
    ----------

    Returns
    -------
    A figure response
    """
    # Connect to the database,
    # the database will automatically be closed after requests
    connection = Project507.db_config.get_db()

    x = ['January', 'February', 'March', 'April',
         'May', 'June', 'July', 'August', 'September',
         'October', 'November', 'December']
    y = []
    for month in x:
        query = "SELECT COUNT(*) as number FROM Movie WHERE release=?"
        y.append(int(connection.execute(query, (month, )).fetchone()['number']))

    x = [i[:3] for i in x]
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
