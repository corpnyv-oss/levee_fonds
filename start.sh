#!/bin/bash
cd /opt/render/project/src
gunicorn fapag_collecte_backend.wsgi:application --bind 0.0.0.0:$PORT
