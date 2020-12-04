from bs4 import BeautifulSoup
import requests
import json


CACHE_FILENAME = "cache.json"
CACHE_DICT = {}


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

            movie = process_a_movie(fields, date)
            rval.append(movie)

    return rval


def process_a_movie(fields, date):

    # to exclude the sub header
    if len(fields) == 5:
        fields = fields[1:]

    wiki_base = r"https://en.wikipedia.org"

    title = fields[0].text
    movie_url = wiki_base + fields[0].a["href"]
    production = fields[1].text
    date = date

    movie = Movie(title, movie_url, production, date)
    movie.into()

    return movie


class Movie:

    def __init__(self, title, movie_url, production, date):
        self.title = title
        self.production = production
        self.date = date
        self.movie_url = movie_url

    def into(self):
        rval = "<{}> (from {}) on {},2016"
        print(rval.format(self.title, self.production, self.date))

def get_movie_information(movie):

    print("debug")


class MovieInfo:
    def __init__(self, title, bio, plot):
        self.title = title
        self.bio = bio
        self.plot = plot
        self.actors

if __name__ == '__main__':

    # load the Cache
    CACHE_DICT = open_cache()

    movies = get_movie_list()

    for movie in movies:
        get_movie_information(movie)
