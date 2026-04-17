#!/usr/bin/env bash
echo "---Updating pip---"
pip install --upgrade pip

echo "---Installing requirements---"
pip install -r requirements.txt

echo "---Colleting statics files---"
python manage.py collectstatic --noinput

echo "---Migrating database---"
python manage.py migrate

echo "---Loading user fixtures---"
python3 manage.py loaddata users

# echo "---Starting server---"
# python manage.py runserver 8001
