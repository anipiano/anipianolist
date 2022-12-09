# anipianolist (name is a work-in-progress)
> "ok guys we need to make the myanimelist of all piano arrangements" – fruit 2022

## Getting started 
```bash
git clone https://github.com/anipiano/anipianolist
cd anipianolist
source env/bin/activate
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```

## Before you dive in
- We use Django 4.1.4 with PostgreSQL and Python 3.11.1 as the backbone of this project
- Smaller code changes can be committed, but significant changes should be PR'd and reviewed before merging with the main branch

## Environment variables
```
anipianolist/anipianolist/.env
``` 

### Apps
Different components of the anipianolist application are segmented into their own app.

- **accounts** - handles account management, IAM, profiles, authentication
- **base** - handles the base of the site (e.g index page, general viewing pages)