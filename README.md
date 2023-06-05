<h1 align="center">
  <br>
  <a href="https://stepik.org/course/125859/info">
    <img src="readme/stepik.jpeg"
    alt="Stepik" width="200">
  </a>
  <br>
  Store
  <br>
</h1>

<h4 align="center">
    Store shop. The project for study Django
    <br>
    <a href="https://stepik.org/course/125859/info" target="_blank">
      Stepik | Backend development on Django: from scratch to a specialist
    </a>
</h4>

<div align="center">

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Stepik](https://img.shields.io/badge/stepik-course-green)](https://stepik.org/course/101042/info)
 <br>
[![Builde Status](https://github.com/mrKazzila/mini_online_store/actions/workflows/basic_code_style_checks.yml/badge.svg?)](https://github.com/mrKazzila/mini_online_store/actions/workflows/basic_code_style_checks.yml)
[![Django simple tests](https://github.com/mrKazzila/mini_online_store/actions/workflows/django_simple_tests.yml/badge.svg)](https://github.com/mrKazzila/mini_online_store/actions/workflows/django_simple_tests.yml)

</div>
<hr>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech stack</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#additional-material">Additional material</a> •
  <a href="https://store-server-test.ru/">Website</a>
</p>


## Features
* Registration new user
  - Verification with e-mail
* Authorisation
  - Also, authorisation with GitHub account
* Change profile settings
* Add goods into cart
* Fake buying
* History orders


## Tech stack
- [Django 3](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Sprite](https://stripe.com/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev/en/stable/index.html)


## How To Use
To clone and run this project, you'll need:
- [Git](https://git-scm.com)
- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

Step-by-step commands or use [Docker](readme/DOCKER.md)
<details>
<summary>commands</summary>

1. Firstly clone repo
   ```bash
   git clone git@github.com:mrKazzila/mini_online_store.git
   ```

2. Copy an example .env file because the real one is git ignored
   ```bash
   cp env/.env.example env/.env
   ```

3. Settings Poetry
   ```bash
   poetry config virtualenvs.in-project true
   ```

4. Activate venv
   ```bash
   poetry shell
   ```

5. Install packages
   ```bash
   poetry install
   ```

6. Install pre-commit
    ```bash
    pre-commit install
    ```

7. Move to app dir
    ```bash
   cd app
    ```

8. Run project dependencies, migrations, fill the database with the fixture data etc
   ```bash
   python manage.py migrate
   python manage.py loaddata <path_to_fixture_files>
   python manage.py runserver
   ```

9. Run [Redis Server](https://redis.io/docs/getting-started/installation/)
   ```bash
   redis-server
   ```

10. Run Celery
    ```bash
    celery -A config worker --loglevel=INFO
    ```

11. Test purchase webhook
     ```bash
     stripe listen --forward-to 127.0.0.1:8000/webhook/stripe/
     ```

12. Start yapf (manual)
    ```bash
    yapf --style=.style.yapf -ir -vv app/
    ```

13. Start pre-commit (manual)
    ```bash
    pre-commit run --all-files
    ```

14. Start bandit (manual)
    ```bash
    bandit -c style/bandit.yaml -r app/ -f json -o bandit_report.json
    ```

</details>


## Additional material

[how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04#further-troubleshooting)


<br>
<br>
<p align="center">
  <a href="https://github.com/mrKazzila">GitHub</a> •
  <a href="https://mrkazzila.github.io/resume/">Resume</a> •
  <a href="https://www.linkedin.com/in/i-kazakov/">LinkedIn</a>
</p>
