Django + Websocket + NextJS

Django
https://channels.readthedocs.io/en/stable/
https://medium.com/geekculture/a-beginners-guide-to-websockets-in-django-e45e68c68a71
https://www.youtube.com/watch?v=cw8-KFVXpTE
https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c

Nextjs
https://blog.logrocket.com/implementing-websocket-communication-next-js/

`pyenv virtualenv django-rest`
`python manage.py runserver`
`python manage.py migrate`
`python manage.py startapp myapi`
`python manage.py createsuperuser`
`python manage.py makemigrations`
Go to `mysite/settings.py`
add `myapi.apps.MyapiConfig` to `INSTALLED_APPS`
