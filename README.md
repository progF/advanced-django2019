# JIRA project

Final version is in "Jira" folder inside of repository.

Project is written on python Django (DRF). 
To use the project, do following steps:
1. Clone the repository
2. Create an environment
```
venv env
```
3. activate the environment and install all required libraries
On Windows
```
env/Scripts/activate
```
On Unix based system
```
source env/bin/activate
```
Then install requirements
```
pip install -r requirements.txt
```
4. create all needed tables

```
python manage.py migrate
```

5. Run the project
```
python manage.py runserver
```
or 
```
./manage.py runserver
```
