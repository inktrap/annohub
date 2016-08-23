# Setup

## Installation

 - put this in your ``~/.bash_profile``
~~~
PYTHONPATH=$HOME
export PYTHONPATH
~~~
 - and source it again: ``source ~/.bash_profile``

 - install virtualenv and pip via easy_install
~~~
easy_install-2.7 --install-dir=$HOME --prefix=$HOME virtualenv pip
~~~

 - create your virtualenv and install the packages via pip
~~~
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
~~~

 - you only need pythoscope if you want to create additional tests with it
 - this howto uses flipflop to run annohub via fastcgi

## DB

 - setup mongodb (this is done via uberspace, see <https://wiki.uberspace.de/database:mongodb>)

## Config & Run

 - change the config in instance/config.py
    - db settings
    - change the value of ``SECRET_KEY`` (i used pwgen multiple times for this)
    - change the values for the ``SECRET_{RESET/SETUP/NLTK}_TOKEN`` (again, I used pwgen multiple times)
    - change ``WTF_CSRF_SECRET_KEY`` (pwgen?? hell yeah!)
    - mail settings are currently not used
 - config.py
    - set ``DEBUG=False``

 - test
 - run the application with fast-cgi and flipflop wsgi

