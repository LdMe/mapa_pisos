#! /bin/bash

docker run  -d --network=pisos_net --mount type=bind,source=/home/danel/Python/Python3/mapa_pisos/src/,target=/app/ mapa_pisos