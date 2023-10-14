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


## Usage

1. Open [Django Admin](http://localhost:8000/admin/)
1. Open [Constant datas](http://localhost:8000/admin/excel/constantdata/)
1. Click on [Ingest Data from Sheet](http://localhost:8000/admin/excel/constantdata/ingest_constant_data/)\
   This will load data from the sample Excel file and populate it into the model
1. Select the new data row, and execute the `Generate results` action.
1. Switch to the [Output data tables](http://localhost:8000/admin/excel/outputdatatabel/)
1. Review the generated results
