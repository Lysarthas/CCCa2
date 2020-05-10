#!/bin/bash
set -e

node1=$1
node2=$2
node3=$3
node4=$4

working_dir=/home/ubuntu
mkdir -p $working_dir/haproxy
cp haproxy.cfg $working_dir/haproxy/

sed -i -e "s/\${node1_ip}/$node1/" \
    -e "s/\${node2_ip}/$node2/" \
    -e "s/\${node3_ip}/$node3/" \
    -e "s/\${node4_ip}/$node4/" \
    $working_dir/haproxy/haproxy.cfg


docker run -d --name haproxy -p 80:80 -v $working_dir/haproxy:/usr/local/etc/haproxy:ro haproxy:1.7-alpine