#!/bin/bash
if [[ -z "${pyscript}" ]]; then
    echo "pyscript required. existing"
    exit 1
fi

sleep 2m

cd CCCa2
git checkout couchdb_store
git pull https://jalllychun:compgliCit5y@github.com/Lysarthas/CCCa2.git couchdb_store

cd crawler
pip install -r requirements.txt

python $pyscript