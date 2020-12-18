# SI507-FinalProject (Bingzhao Shan)

## Setup

### step1: Clone the github repo: https://github.com/zuoyigehaobing/SI507-FinalProject.git

### step2: go inside SI507-FinalProject and create a virtual python environment

- Make sure you are in SI507-FinalProject

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


## Database

- Schema: https://github.com/zuoyigehaobing/SI507-FinalProject/blob/main/wiki_crawler/schema.sql

- Database: https://github.com/zuoyigehaobing/SI507-FinalProject/tree/main/var 

## Demo Video:

https://www.youtube.com/watch?v=AMiAtRLl8KM
