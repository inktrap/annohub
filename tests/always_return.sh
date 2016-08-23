#!/bin/bash

# check that every redirecting or rendered template will be returned (or is an
# import statement) otherwise they are pointless and a mistake

grep 'redirect|render_template' ../app/annohub/routes.py ../app/annohub/blueprint/* | grep -v 'return|import'

# found nothing? good
# else: bad
if [[ $? -eq 1 ]]; then
    exit 0
else
    exit 1
fi

