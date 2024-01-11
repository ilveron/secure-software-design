django-admin startproject my_project
cd my_project
poetry init
poetry add django djangorestframework django-cors-headers coreapi dj-rest-auth django-allauth="^0.55.0" pytest-django mixer
poetry shell