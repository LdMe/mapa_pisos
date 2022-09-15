#! /bin/bash

docker run  -d  --mount type=bind,source=$PWD,target=/app/ mapa_pisos