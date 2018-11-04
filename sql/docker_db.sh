#!/bin/bash

#Docker container initialization
docker run -d --name db \
    -e WEB_CONSOLE=false \
    -p 1521:1521 \
    -v $(pwd)/db-data:/u01/app/oracle sath89/oracle-12c