#!/bin/bash


ASSETS=./app/annohub/templates/page
HA=./_docs/ha/
pandoc --bibliography ${ASSETS}/template.bib --csl ${ASSETS}/association-for-computational-linguistics.csl --filter pandoc-citeproc ${ASSETS}/content.md -S -o ${ASSETS}/content.html || true
#cp ./app/annohub/templates/page/content.md -S -o ./_docs/ha/
#cd ./_docs/ha/ \
#pandoc --bibliography ./_docs/ha/template.bib --filter pandoc-citeproc content.md -S -o content.tex
pandoc --bibliography ${ASSETS}/template.bib --csl ${ASSETS}/association-for-computational-linguistics.csl --filter pandoc-citeproc ${ASSETS}/content.md -S -o ${HA}/content.tex || true
cd ${HA} && rubber -d template.tex && cd -

