#!/bin/bash

mkdir -p deploy/logs
rm public/FusEd.zip
cd deploy
zip ../public/FusEd.zip Dockerfile main.py mcu.py python_svc requirements.txt logs
cd ..
vim -N -u NONE -n -es \
    fused.cue \
    -c "g/sha256sum/s/\".*\"/\"$(sha256sum public/FusEd.zip | cut -f 1 -d ' ')\"" \
    -c 'wq'
    
