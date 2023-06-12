@echo off

REM Activate the virtual environment (if you're using one)
REM Replace 'C:\path\to\venv' with the actual path to your virtual environment
call pipenv shell
pipenv install

REM Navigate to the Django project directory
REM Replace 'C:\path\to\project' with the actual path to your Django project
cd C:\path\to\project

REM Run Django migrations
python cuea\manage.py migrate

REM Start the Django development server
python cuea\manage.py runserver
