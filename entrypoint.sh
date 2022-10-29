#!/bin/sh

echo "$DATABASE is my db"
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
echo "----- Entrypoint Commands Execution Finished -----"
flask run
