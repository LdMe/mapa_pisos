#!/bin/sh
gunicorn --chdir app app:app -w 2 --timeout 1000 --threads 2 -b 0.0.0.0:80