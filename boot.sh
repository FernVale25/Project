#!/bin/sh
. venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - LogView:app