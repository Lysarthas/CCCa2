#!/bin/bash
if [[ -z "${pyscript}" ]]; then
    echo "pyscript required. existing"
    exit 1
fi

sleep 2m

cd /code/crawler

python $pyscript