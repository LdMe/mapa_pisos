#! /bin/bash

docker run  -d  --mount type=bind,source=/home/danel/Python/Python3/mapa_pisos/mapa_pisos/,target=/app/ mapa_pisos