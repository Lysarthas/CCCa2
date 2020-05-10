#!/bin/bash
set -e

git clone https://jalllychun:compgliCit5y@github.com/Lysarthas/CCCa2.git
cd CCCa2
git checkout couchdb_store ## checkout the correct branch
cd docker_image
docker build  -t harvester --build-arg http_proxy=http://wwwproxy.unimelb.edu.au:8000/ --build-arg https_proxy=http://wwwproxy.unimelb.edu.au:8000/ .


target_ip=$1
target_port=$2
user_name=$3
pass=$4
url=http://$user_name:$pass@$target_ip:$target_port
echo $url

## check connectivity
curl $url
if [ "$?" = "7" ]; then 
    echo "fail to connect couchdb. please check connectivity"
    exit 1
fi

## check db existence
for db in junlin history finished_user
do
    rstatus=$(curl -s -w %{http_code} $1 $url/$db)
    if [[ $rstatus == *"error"* ]]; then
        echo "failed to check existence of db"
        exit 1
    fi
done

## wait view to init
echo "$url/junlin/_design/results/_view/user?group_level=1&reduce=true"
rstatus=$(curl -w $1 -o /dev/null $url/junlin/_design/results/_view/user?group_level=1&reduce=true)
if [[ $rstatus == *"error"* ]]; then
    echo $rstatus
    echo "failed to get view"
    exit 1
fi


#boot the harvester up
docker run -d  --name=realtime -e pyscript=StreamToCouchDB.py -e dbip=172.17.0.1:$target_port --restart=on-failure harvester

docker run -d  --name=history -e pyscript=HistoryCrawler.py -e dbip=172.17.0.1:$target_port --restart=on-failure harvester