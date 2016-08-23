# Developer Documentation

First we need to setup a virtualenv, nltk, mongodb and selenium (for testing). Also install ``autopep8``. Then configure your application.

# Virtualenv

 - Because it is hip (and actually very useful), create a virtualenv: ``virtualenv .env``
 - activate the virtualenv: ``source .env/bin/activate``
 - install the requirements: ``pip install -r requirements.txt``

# NLTK

Get all the resources like:

 - tokenizers/punkt/english.pickle
 - taggers/maxent_treebank_pos_tagger/english.pickle'
 - via nltk.downloader()
 - this means to download the packages: ``punkt maxent_treebank_pos_tagger``

# DB  Setup

 - install mongodb: ``sudo apt-get install mongodb``
 - bind it to localhost:27017: add to ``mongodb.conf``:
~~~
 bind_ip = 127.0.0.1
 bind_port = 27017
~~~
 - then start/restart it: ``sudo service mongodb start``
 - check that it is running, navigate to: <http://localhost:27017/>
 - you should get the notice: ``You are trying to access MongoDB on the native driver port. For http diagnostic access, add 1000 to the port number``
 - and if you visit ``28017``, as told: ``http://localhost:28017/`` you will se the http-diagnostic page. :)

# DB Insert Data

 - check ``app/instance/config.py`` for the value of:
~~~
SECRET_RESET_DB_TOKEN='abc'
RESET_DB_URL='/reset-db/<secret_token>'
~~~
 - call ``127.0.0.1:5000/reset-db/abc``
 - TODO: this should not be possible in released versions!!

# DB Management

 - personally I just call ``php -S localhost:8000 index.php``, where index.php is [adminer](https://www.adminer.org/static/download/4.2.3/adminer-4.2.3-en.php).

# Setup Testing (optional)

 - install ``autopep8`` via your distribution.
 - install ``selenium`` via pip (should be included in ``requirements.txt``)
 - use the latest selenium-ide firefox plugin
 - selenium-ide: enable experimental features to be able to export to python

# Application

 - run the application, call ``./run.py``
 - populate the database, by calling: ``127.0.0.1:5000/reset-db/abc`` **this might change in the future, because it is insecure and makes it easy to make the mistake of leaving it enabled**.
 - tun the tests, via ``./tests/testrunner.sh`` (if not texts are there to test with, check if you have internet, because alice in wonderland will be downloaded for you)


