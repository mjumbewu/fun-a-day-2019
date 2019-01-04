Following the Channels tutorial at https://channels.readthedocs.io/en/latest/tutorial/

Decided to try out `pipenv` too!

```bash
venv env -p python3
pipenv install django channels

django-admimn startproject helloworld
cd helloworld

./manage.py startapp chat
cd chat

rm admin.py apps.py models.py tests.py
mkdir -p templates/chat
```
