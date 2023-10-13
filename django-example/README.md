# Django Example

## Installation

1. Create a virtual env and activate it
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
1. Update `pip` and install requirements
   ```
   pip install -U pip
   pip install -r requirements.txt
   ```

## Django

1. Change to the `django_excel` folder
1. Run all migrations
   ```
   python manage.py migrate
   ```
1. Create a superuser
   ```
   python manage.py createsuperuser
   ```
1. Start Django
   ```
   python manage.py runserver
   ```
