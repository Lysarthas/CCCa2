#!/bin/bash

working_dir=$(~)
mkdir -p $working_dir/haproxy
cp haproxy.cfg $working_dir/haproxy/

docker run -d --name haproxy -v $working_dir/haproxy:/usr/local/etc/haproxy:ro haproxy:1.7-alpine