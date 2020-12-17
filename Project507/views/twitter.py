from requests_oauthlib import OAuth1
import json
import requests
import Project507


client_key = "SE0jTe8FgYLacMKHppFCQyyEX"
client_secret = "bqsTUKmu8d7nk796MegmhTywQCirj6b6J1ytn13ZewKEL6TZ8G"
access_token = "1319797198180257795-59BOJyfFD13CBGecvLFSFE3703HGjQ"
access_token_secret = "tN9XYdjqfpW0VwveixOjzPawWBAuxz6jJq8PlTa3OrAvP"

CACHE_FILENAME = Project507.app.config['TWITTER_CACHE']
CACHE_DICT = {}


oauth = OAuth1(client_key,
               client_secret=client_secret,
               resource_owner_key=access_token,
               resource_owner_secret=access_token_secret)


def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a
    representation of the requesting user if authentication was
    successful; returns a 401 status code and an error message if
    not. Only use this method to test if supplied user credentials are
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token, access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, "w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and
    repeatably identify an API request by its baseurl and params

    AUTOGRADER NOTES: To correctly test this using the autograder, use an underscore ("_")
    to join your baseurl with the params and all the key-value pairs from params
    E.g., baseurl_key1_value1

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
    '''
    #TODO Implement function

    # initialize parameter strings and connector
    param_strings, connector = [], '_'

    # loop over parameters
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')

    # sort the parameter string to make a unique key
    param_strings.sort()
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs

    Returns
    -------
    dict
        the data returned from making the request in the form of
        a dictionary
    '''
    #TODO Implement function

    # make a request to the server and parse the response into json
    response = requests.get(baseurl, params=params, auth=oauth)
    return response.json()


def make_request_with_cache(baseurl, hashtag, count):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    AUTOGRADER NOTES: To test your use of caching in the autograder, please do the following:
    If the result is in your cache, print "fetching cached data"
    If you request a new result using make_request(), print "making new request"

    Do no include the print statements in your return statement. Just print them as appropriate.
    This, of course, does not ensure that you correctly retrieved that data from your cache,
    but it will help us to see if you are appropriately attempting to use the cache.

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search for
    count: integer
        The number of results you request from Twitter

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    #TODO Implement function

    # read the cache
    CACHE_DICT = open_cache()

    # initialize the param
    params = {"q": hashtag, "count": count}

    # get the unique key
    request_key = construct_unique_key(baseurl, params)

    # check if the request is cached
    if request_key in CACHE_DICT:
        print("fetching cached data")
        return CACHE_DICT[request_key]
    else:
        print("making new request")
        CACHE_DICT[request_key] = make_request(baseurl, params)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]


def get_twitter_content():

    CACHE_DICT = open_cache()
    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    count = 5
    hashtag = "#moviereview"
    tweet_data = make_request_with_cache(baseurl, hashtag, count)

    info = []
    counter = 0
    for item in tweet_data['statuses']:

        if counter % 1 == 0:
            info.append(item['text'])
        counter += 1

    return info
