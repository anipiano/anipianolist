# anipianolist (name is a work-in-progress)
> "ok guys we need to make the myanimelist of all piano arrangements" – fruit 2022

## Getting started 
```bash
git clone https://github.com/anipiano/anipianolist
source env/bin/activate
cd anipianolist
pip install -r requirements.txt
#edit your .env before starting
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```

## Before you dive in
- We use Django 4.1.4 with PostgreSQL 14.5 and Python 3.11.1 (check `requirements.txt` for full list of dependencies)
- Smaller code changes can be committed, but significant changes should be PR'd and reviewed before merging with the main branch
- If you have any trouble with anything, feel free to ask in #anipianolist on Yeh's server :D although things might look difficult, just remind yourself nothing is more difficult than Animenz Sincerely :kekw:
- Feedback is welcome in #anipianolist on Yeh's server or #collab on Fruit's server. Or just spam ping every contributor on this GitHub repo (no don't actually do this :facepalmcry:)

### Authentication

You'll need to register applications in both Discord and Google to use OAuth2 authentication.

1. **Discord** - https://discord.com/developers > New application > OAuth2 > redirect URL: http://replace-me-you-baka.net/oauth2/discord/login/callback/
2. **Google** - https://console.cloud.google.com/apis/credentials > OAuth2 client ID > Web application > redirect URI: `http://replace-me-you-baka.net/oauth2/google/login/callback/`

### Database
You'll need to set some things up before you can spam your love for 150bpm in every row of the object-relational database. We use PostgreSQL over the default SQLite3 setup due to its support for write concurrency and generally better performance in our specific production use case.

This guide assumes you're running a derivative of Ubuntu or Debian, but you should easily be able to substitute commands for Microsoft Windows, other Linux distributions or macOS where necessary. 

Thanks to [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04) for being my senpai for this guide.

1. Start by installing the necessary psql-related dependencies for your operating system. For example, on Ubuntu/Debian-based Linux distributions:

```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
```

2. Log into a `psql` session.

```bash
sudo -u postgres psql
```

3. In the `postgres=#` console, set up your PostgreSQL database. Feel free to change names like `myproject` and `myprojectuser` to something more descriptive.

```sql
CREATE DATABASE myproject;
CREATE USER myprojectuser WITH PASSWORD 'password';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

You can leave the console with `\q`.

4. In `$ROOT/anipianolist/anipianolist/.env`, where `$ROOT` is the root of the git repository as given by `git rev-parse --show-toplevel`, you'll need to amend the environment variables with the credentials you set up in Step 3. **This should not be committed** and will be automatically ignored as specified by `.gitignore`.

```bash
...
DB_NAME=myproject
DB_USERNAME=myprojectuser
DB_PASSWORD=password
...
``` 

#### Groups

Set up these groups in Django to take advantage of internal management systems.

- **Admin** - full access to systems except for internal Django dashboard (reserve this for superuser)
- **Moderator** - access to modifying user data
- **Maintainer** - access to modifying arrangement database entries

All moderation actions are logged.

### Environment variables
Use the provided `.env.example` template to set up your environment variables for local or production instances.
```
$ROOT/anipianolist/anipianolist/.env
``` 
where `$ROOT` is the root of the git repository as given by `git rev-parse --show-toplevel`

`.env` and other files beginning with a dot may be hidden by macOS. Use `Command+Shift+Dot` in Finder or `ls -a` in shell to unhide these files.

## Apps
Different components of the anipianolist application are segmented into their own app.

- **accounts** - handles account management, IAM, profiles, authentication (note this is different from `account` which is an app in `django-allauth`)
- **base** - handles the base of the site (e.g index page, general viewing pages)
- **database** - handles all features of the site which interact heavily with the database 

## i18n

i18n is **not** supported at the time. 

- Although some packages included may have i18n support, in general this is not maintained.
- Templates may use `{% trans %}` template tags to indicate strings which should be translated. This is grandfathered from default templates but does not affect final output.
- In the future, adding i18n support is reasonable simple from a technical viewpoint and involves updating templates and providing mappings. Therefore, i18n support can be added later when the need arises.