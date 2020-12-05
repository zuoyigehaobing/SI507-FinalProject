from bs4 import BeautifulSoup
import requests
import json
import sqlite3


DB_PATH = "../database/movies.db"
CACHE_FILENAME = "cache.json"
CACHE_DICT = {}
MOVIE_COUNTER, ACTOR_COUNTER = 0, 0
REGISTERED_ACTORS = {}

def check_cache_or_make_requests(url, params=None):
    """ Construct the unoqiue key based on the url and params, if the unique
    key already exists in the cache, load from cache directly, otherwise
    make new fetching requests

    Parameters
    ----------
    url: string
        the url to make request to
    params: dict or None
        the params associated with the request

    Returns
    -------
    The response: requests
    """
    # get the cache variable
    global CACHE_DICT

    # get the unique key
    unique_key = url if params is None else construct_unique_key(url, params)

    # check the unique key in the cache
    if unique_key in CACHE_DICT:
        print("Using cache")
    else:
        print("Fetching")
        if params:
            response = requests.get(url, params=params)
            CACHE_DICT[unique_key] = response.json()
        else:
            response = requests.get(url)
            CACHE_DICT[unique_key] = response.text
        save_cache(CACHE_DICT)

    # return the content
    return CACHE_DICT[unique_key]


def open_cache():
    """ Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------

    Returns
    -------
    The opened cache: dict
    """
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    """ Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    """
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, "w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(baseurl, params):
    """ constructs a key that is guaranteed to uniquely and
    repeatably identify an API request by its baseurl and params

    AUTOGRADER NOTES: To correctly test this using the autograder,
    use an underscore ("_") to join your baseurl with the params and all
    the key-value pairs from params E.g., baseurl_key1_value1

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs

    Returns
    -------
    string
        the unique key as a string
    """
    # initialize parameter strings and connector
    param_strings, connector = [], '_'

    # loop over parameters
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')

    # sort the parameter string to make a unique key
    param_strings.sort()
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key


def get_movie_list():

    # container
    rval = []

    # starts from the root url
    root_url = r'https://en.wikipedia.org/wiki/List_of_American_films_of_2016'

    # check cache, get a soap object
    html_content = check_cache_or_make_requests(root_url)
    soap = BeautifulSoup(html_content, "html.parser")

    # section by month
    sections = soap.find_all("table", class_="wikitable sortable")

    # loop over sections and get the movies
    for section in sections:
        movies = section.find_all("tbody")[0]
        movies = movies.find_all('tr')

        date = 'January'
        for movie in movies:

            # check/update the dates
            check_date = movie.find_all("div", recursive=True)
            date = check_date[0].text if check_date else date

            fields = movie.find_all("td")
            # pass on headers
            if len(fields) == 0:
                continue

            movie_item = process_a_movie_item(fields, date)
            rval.append(movie_item)

    return rval


def process_a_movie_item(fields, date):

    # to exclude the sub header
    if len(fields) == 5:
        fields = fields[1:]

    wiki_base = r"https://en.wikipedia.org"

    title = fields[0].text
    movie_url = wiki_base + fields[0].a["href"]
    production = fields[1].text
    date = date

    movie = Movie(title, movie_url, production, date)

    return movie


class Movie:

    def __init__(self, title, movie_url, production, date):
        global MOVIE_COUNTER
        self.title = title
        self.production = production
        self.date = date
        self.movie_url = movie_url
        self.bio = ""
        self.plot = ""
        self.id = MOVIE_COUNTER
        MOVIE_COUNTER += 1

    def info(self):
        rval = "<{}> (from {}) on {},2016"
        print(rval.format(self.title, self.production, self.date))

    def set_bio(self, bio):
        self.bio = bio

    def set_plot(self, plot):
        self.plot = plot

    def to_db(self):
        connection = sqlite3.connect(DB_PATH)
        cur = connection.cursor()
        query = """
        INSERT INTO Movie(movieid, name, release, production, url, bio, plot)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        cur.execute(query, (self.id,
                            self.title,
                            self.date,
                            self.production,
                            self.movie_url,
                            self.bio,
                            self.plot))
        connection.commit()
        connection.close()

    def check_db_size(self):
        connection = sqlite3.connect(DB_PATH)
        cur = connection.cursor()
        query = """
                SELECT COUNT(*) FROM Movie
                """
        cur.execute(query)
        print(cur.fetchone())
        connection.close()


def get_movie_information(movie):


    # starts from the root url
    url = movie.movie_url

    # check cache, get a soap object
    html_content = check_cache_or_make_requests(url)
    soap = BeautifulSoup(html_content, "html.parser")

    # section by month
    section = soap.find_all("div", class_="mw-parser-output", recursive=True)
    assert len(section) == 1
    section = section[0]

    # should be used for future parsing
    cast_info = get_cast_list(section, url)

    bio_text = get_movie_bio(section)
    plot_text = get_movie_plot(section)

    movie.set_bio(bio_text)
    movie.set_plot(plot_text)
    return cast_info


def get_cast_list(content, url):

    satisfied = False
    rval = None
    for child in content.children:
        if child.name == "h2" and child.text.strip().lower() in ("cast[edit]", "cast", "voice cast", "voice cast[edit]", "cast and characters[edit]"):
            satisfied = True
            continue
        if satisfied and child.name == "ul":
            rval = child
            break
        elif satisfied and child.name == "div":
            rval = child.find('ul')
            break

    if not rval:
        return []

    actors = []
    wiki_base = r"https://en.wikipedia.org"
    for item in rval.find_all('a'):
        actor_url = wiki_base + item.get("href")
        actor_name = item.text
        if '[' in actor_name.strip():
            continue
        actors.append(actor_url)
    return actors


def get_movie_plot(content):

    rval = ""
    started = False
    for child in content.children:
        if child.name == "h2" and child.text.strip() == "Plot[edit]":
            started = True
            continue
        if started and child.name and child.name != "p":
            break

        if started and child.name:
            rval += child.text.strip() + "\n"

    # print(rval)

    return rval


def get_movie_bio(content):
    """
    Bio is the information inside <p> between the info box and contents box
    :param content:
    :return:
    """
    rval = ""
    started = False
    for child in content.children:
        if child.name == "table" and \
                ' '.join(child.get("class")) == 'infobox vevent':

            started = True
            continue
        if started and child.name and child.name != "p":
            break

        if started and child.name:
            rval += child.text.strip() + "\n"

    return rval


class Actor:
    def __init__(self, name, url):
        global ACTOR_COUNTER
        self.name = name
        self.url = url
        self.imageurl = None
        self.id = ACTOR_COUNTER
        ACTOR_COUNTER += 1

    def set_imgurl(self, imgurl):
        self.imageurl = imgurl

    def to_db(self):

        global REGISTERED_ACTORS

        if self.url in REGISTERED_ACTORS:
            return

        REGISTERED_ACTORS[self.url] = True

        connection = sqlite3.connect(DB_PATH)
        cur = connection.cursor()

        query = """
                INSERT INTO Actor(actorid, fullname, url, imageurl)
                VALUES(?, ?, ?, ?)
                """
        cur.execute(query, (self.id,
                            self.name,
                            self.url,
                            self.imageurl))

        connection.commit()
        connection.close()

    def check_db_size(self):
        connection = sqlite3.connect(DB_PATH)
        cur = connection.cursor()
        query = """
                SELECT COUNT(*) FROM Actor
                """
        cur.execute(query)
        print(cur.fetchone())
        connection.close()




def crawl_actor_pages(actors):

    rval = []
    for actor_url in actors:

        # check cache, get a soap object
        html_content = check_cache_or_make_requests(actor_url)
        soap = BeautifulSoup(html_content, "html.parser")

        # get full name
        section = soap.find_all("h1", class_="firstHeading", recursive=True)
        actor_name = section[0].text
        assert len(section) == 1

        # get info card
        section = soap.find("table", class_="infobox biography vcard", recursive=True)

        # cur actor
        actor = Actor(actor_name, actor_url)
        rval.append(actor)
        # if no info card
        if not section:
            continue

        # parse image url and born information in the info card
        img_section = section.find("img")
        if img_section:
            actor.set_imgurl(img_section["src"][2:])

    return rval


def add_casting_info_to_db(actor, movie):

    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()

    query = "INSERT INTO Casting(actorid, movieid) VALUES(?, ?)"
    cur.execute(query, (actor.id, movie.id))

    connection.commit()
    connection.close()



if __name__ == '__main__':

    # import database
    # database.create_tables()

    # load the Cache
    CACHE_DICT = open_cache()
    movies = get_movie_list()

    idxer = 0
    for movie in movies:

        idxer += 1
        print("{}/149".format(idxer))

        # update
        actor_urls = get_movie_information(movie)

        # get the casting actors
        actors = crawl_actor_pages(actor_urls)

        # add the movie information into the database
        movie.to_db()

        # add actor info into database
        for actor in actors:
            actor.to_db()
            add_casting_info_to_db(actor, movie)

        if len(actors):
            actors[0].check_db_size()
        else:
            print("debug")

        # add


    movies[0].check_db_size()
