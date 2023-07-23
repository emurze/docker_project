set -e

cd src

python3 manage.py makemigrations
python3 manage.py migrate --noinput

if [ "$ADMIN_EMAIL" ]
then
python3 manage.py createadmin \
        --username "$ADMIN_USERNAME" \
        --password "$ADMIN_PASSWORD" \
        --email "$ADMIN_EMAIL"
else
python3 manage.py createadmin \
      --username "$ADMIN_USERNAME" \
      --password "$ADMIN_PASSWORD"
fi

python3 manage.py runserver 0.0.0.0:8080