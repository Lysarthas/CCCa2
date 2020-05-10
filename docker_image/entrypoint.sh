#!/bin/bash
if [[ -z "${pyscript}" ]]; then
    echo "pyscript required. existing"
    exit 1
fi

cd CCCa2
git checkout couchdb_store
git pull https://jalllychun:compgliCit5y@github.com/Lysarthas/CCCa2.git couchdb_store

pip install -r /CCCa2/requirements.txt

cd crawler
python $pyscript