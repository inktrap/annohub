u''' Define public config here. Put private/secret stuff into
./instance/config.py'''

import time
import os
import logging

DEBUG = True # Turns on debugging features in Flask
BCRYPT_LEVEL = 12 # Configuration for the Flask-Bcrypt extension

COMPANY = "annohub"
YEAR = time.strftime("%Y")

LOG_FILE = 'annohub'
LOG_DIR = os.path.join(os.curdir, 'tmp')

DEFAULT_USER='annohub'
DEFAULT_USER_EMAIL='annohub@foo.tld'

#SERVER_NAME = "annohub.flask.int:5000"
ENCODINGS_ALLOWED = ['utf8', 'ascii', 'latin1']
MAIL_SUPPRESS_SEND=True, # Disable Flask-Mail send

# external urls
GITHUB_URL = 'http://github.com'

# nltk data dir is in the same directory as this file
NLTK_DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'nltk_data')
os.environ["NLTK_DATA"] = NLTK_DATA_DIR

NLTK_DOWNLOAD = ['tagsets',
    'universal_tagset',
    'punkt',
    'maxent_treebank_pos_tagger',
    'hmm_treebank_pos_tagger',
    'averaged_perceptron_tagger'
]

# languages
OTHER_LANGUAGE = 'other'
LANGUAGES = [ 'czech',
    'danish',
    'dutch',
    'english',
    'estonian',
    'finnish',
    'french',
    'german',
    'greek',
    'italian',
    'norwegian',
    'polish',
    'portuguese',
    'slovene',
    'spanish',
    'swedish',
    'turkish',
    OTHER_LANGUAGE
]

# currently, these are from the brown-corpus
OTHER_GENRE = 'other'
GENRES = [ 'news',
    'editorial',
    'reviews',
    'religion',
    'hobbies',
    'lore',
    'belles_lettres',
    'government',
    'learned',
    'fiction',
    'mystery',
    'science_fiction',
    'adventure',
    'romance',
    'humor',
    OTHER_GENRE
]

# tagsets included in nltk, but unfortunately no taggers or mappings exist for them, so use upenn
#TAGSETS = [ 'brown_tagset', 'claws5_tagset', 'upenn_tagset' ]
TAGSETS = [ 'upenn_tagset' ]

# these names are reserved names
# extended by <https://ldpreload.com/files/names-to-reserve.txt>
USER_BLACKLIST = [
    #'annohub',
    'default',
    'user',
    'guest',
    'moderator',
    'techsupport',
    'abuse'
    'admin',
    'administrator',
    'autoconfig',
    'broadcasthost',
    'ftp',
    'hostmaster',
    'imap',
    'info',
    'is',
    'isatap',
    'it',
    'localdomain',
    'localhost',
    'mail',
    'mailer-daemon',
    'marketing',
    'mis',
    'news',
    'nobody',
    'noc',
    'noreply',
    'no-reply',
    'pop',
    'pop3',
    'postmaster',
    'root',
    'sales',
    'security',
    'smtp',
    'ssladmin',
    'ssladministrator',
    'sslwebmaster',
    'support',
    'sysadmin',
    'usenet',
    'uucp',
    'webmaster',
    'wpad',
    'www'
    ]

# how long is one tokenization/annotation session in sentences?
SENTENCE_LIMIT=3

# 15MB upload limit is the largest (bson documents can not be greater than this)
# the resulting document is always bigger than the raw text
# this is why I choose to use 0.25 of the limit, which is 
# (just to be safe) ~3.8MB
# also this has an effect on the size of the test-files
SIZE_LIMIT = (15 * 1024 * 1024) * 0.25 #  = 3932160.0 which is ~ 3.8MB

if os.environ.has_key('FLASK_ANNOHUB_TESTING')\
    and int(os.environ['FLASK_ANNOHUB_TESTING']) == 1:
    # wether this is a test run via unittest or selenium
    TESTING = True
    DEBUG = False
    # logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(\
        #level=logging.INFO, \
        level=logging.ERROR, \
        format='%(asctime)s %(name)s %(levelname)s %(message)s'
        )
    #werkzeug_logging = logging.getLogger('werkzeug')
    #werkzeug_logging.setLevel(logging.ERROR)

else:
    # wether this is a test run via unittest or selenium
    TESTING = False
