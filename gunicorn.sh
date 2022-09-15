#!/bin/sh
gunicorn --chdir app app:app -w 2 --timeout 1000 --threads 4 -b 0.0.0.0:80