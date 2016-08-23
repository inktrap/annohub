# Annohub

A simple annotation platform to add part-of-speech tags in a semi-automated way.

 - keywords: ``annotation, linguistics, computational linguistics, part-of-speech tagging, web platform, flask, mongodb, mongoengine, nltk``
 - status: ``beta``
 - developer/setup information: ``DEVELOPER.md``
 - license information: Mit License, see ``LICENSE.md``

Since annohub is beta, there is still a lot to do.

## Todo

 - the annotation menu should be sticky so the user does not have to scroll
 - manage annotators: view their status: how far are they? did they skip? (pull the annotation objects from all annotators an calculate percentage)
 - write export, export is always possible
     - in memory python zip-file generation, json
     - do not export users/rights/…
 - the user should be able to select the current token
 - more keybindings would be nice (s: search)
 - rollback when creating projects aso.
 - more unittests

## Milestones

 - publishing
     - select publishing options: check that publishing is only possible if all annotators annotated
         - this has to be triggered if an annotator deletes, is removed or finishes
     - list all projects that are public (new tab)
     - if it is published, you can not invite new annotators
 - write stats, visualization gui, d3js

# Planned Features

 - deleting users: delete all data and projects from that user. what if annotators left?
 - mobile devices, tokenization menu, responsive tables, tables have the same size …
 - list errors and what they mean
 - mail/log unusual exceptions to admin
 - do db consistency checks
 - clean installation/setup
 - users can disable to get invited
 - coverage? <http://coverage.readthedocs.org/en/latest/>

# Bugs

 - empty words, empty sentences
 - POTENTIAL BUG: check uploaded file by filetype
 - POTENTIAL BUG: validate, if you really get text and are able to decode it
 - (re-)check error handling. what if …
    - the db is full or the quota is reached?
    - a connection to the db is not possible?
    - the application dies (f.e.: cpu/memory usage)
    - a db operation fails
    - a user uploads a document and (somehow) creates invalid json?
    - a user injects js into the document?
    - a user changes the document that is tokenized/annotated
    - a user does all the requests with an invalid document-id
    - a user bruteforces logins
    - a user uploads arbitrary filetypes
    - a user uploads arbitrary content
    - a user logs in from two different devices
        - what if his actions contradict each other?
    x a user has no javascript enabled: notice to enable javascript is displayed
    - a user uploads unicode content (what does nltk do?)


# Development

 - start server: ``php -S localhost:8000 /var/www/adminer/index.php``
 - start application: ``./run.py``

