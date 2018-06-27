#! /bin/bash

set -e

if [ $SERVICE != 'srv' ]; then
  echo "Running lottery $SERVICE ..."
  exec python manage.py $SERVICE
elif [ $SERVICE = 'srv' ]; then
  echo "Running cdd-admin-srv server..."
  cd /home/app
  gunicorn cdd-admin-srv.wsgi:application -c deploy/gunicorn.conf
else
  echo "Please specify service."
  exit
fi
