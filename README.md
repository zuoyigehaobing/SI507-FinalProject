# SI507-FinalProject (Bingzhao Shan)

## Setup

### step0: the environment log can be found here for your reference: [HERE](https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/doc/env.txt) 

### step1: Clone the github repo: https://github.com/zuoyigehaobing/SI507-FinalProject.git

### step2: go inside SI507-FinalProject and create a virtual python environment

- Make sure you are in folder SI507-FinalProject

- On Mac: **/usr/local/bin/python3 -m venv env**

- OnWindows: **python3 -m venv env**

### step3: initialize the virtual python environment

- **source env/bin/activate**

- **pip install --upgrade pip setuptools wheel**

- **pip install -r requirements.txt**

- **pip install -e .**

### (optional) step4: crawl the contents and create database from scratch

The third step is to initialize the database and fetch data from the wiki root page using a crawler. Since this is time consuming, I already put a copy of the dataset in my GitHub so this step can be skipped. However, if there’s need to redo it, please run **python ./wiki_crawler/wiki_crawler.py** from the root directory.

### step5: run the start script

- **./bin/run**

### step6: go to localhost:8000


## Wiki Crawler and Twitter API

- The root wiki page: https://en.wikipedia.org/wiki/List_of_American_films_of_2016

- The crawling code: https://github.com/zuoyigehaobing/SI507-FinalProject/tree/main/wiki_crawler 

- Twitter (API keys included inside the code): https://developer.twitter.com/en/docs/twitter-api 

- Twitter intergration with the project: https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/Project507/views/twitter.py

## Database

- Schema: https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/wiki_crawler/schema.sql

- Database: https://github.com/zuoyigehaobing/SI507-FinalProject/tree/main/var 


## Interaction:

### Signin/Signup

- Signup a new user or login a user before start

<img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/signin.png" width="540"> <img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/signup.png" width="540">

### Index page

- In the index page, users are able to see most recent movie reviews from twitter as well as a list of movies crawled from Wiki. Users can also click to see detailed information about each movie or click like to mark it favourite.

<img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/index1.png" width="540"> <img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/index2.png" width="540">

### Movie page

- This page contains the detailed information of a movie including producer, release date, bio, plot and casting actors.

<img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/movie1.png" width="540"> <img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/movie2.png" width="540">

### Favourite page

- This page showsthe movies you've marked as favourite.

<img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/favourite.png" width="540"> 

### Users page

- Explore other users and follow them to see their favourite movies.

<img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/users.png" width="540"> 

### Explore page

- Explore other users and follow them to see their favourite movies.

<img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/explore.png" width="540"> 

### Figure page

- A figure demostrated months v.s. number of movies released on that month

<img src="https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/demo/figure.png" width="540"> 
