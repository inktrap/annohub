#!/usr/bin/env python2.7
u''' only run app here, configure it in config.py and models in
app/models/__init__.py'''

from annohub import app
app.run(threaded=True)
