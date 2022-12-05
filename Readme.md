Django + Websocket + NextJS
---------------------------

Main project is [mysite](./mysite)

Django
------
https://channels.readthedocs.io/en/stable/
https://channels.readthedocs.io/en/stable/topics/consumers.html
- This is what was followed to create the chat application

https://medium.com/geekculture/a-beginners-guide-to-websockets-in-django-e45e68c68a71

https://www.youtube.com/watch?v=cw8-KFVXpTE

https://www.honeybadger.io/blog/django-channels-websockets-chat/
- This is a bad tutorial since calling `consumers.ChatRoomConsumer.as_asgi()` results in `AttributeError: type object 'ChatRoomConsumer' has no attribute 'as_asgi'`
- The error above was due to incorrect django version

https://www.infoworld.com/article/3658336/asgi-explained-the-future-of-python-web-development.html#:~:text=Like%20WSGI%2C%20ASGI%20describes%20a,both%20sync%20and%20async%20apps.

https://stackoverflow.com/questions/66104932/django-3-1-5-and-channels-3-0-3-websocket-problem

wsgi - web server gateway interface. Outdated can't natively handle websocket. Is only synchroneous, websocket requires async

asgi - asynchronous server gateway interface. allows multiple, asynchronous events per application. Supports both sync and async.
- scope: a dictionary with information about the current request
- send: an async callable function that lets the application send messages back to the client
- receive: An async callable that lets the application receive messages from the client


### Django commands
`pyenv virtualenv django-rest`\
`python manage.py runserver`\
`python manage.py migrate`\
`python manage.py startapp myapi`\
`python manage.py createsuperuser`\
`python manage.py makemigrations`\
Go to `mysite/settings.py`\
add `myapi.apps.MyapiConfig` to `INSTALLED_APPS`


Nextjs
------
https://blog.logrocket.com/implementing-websocket-communication-next-js/

