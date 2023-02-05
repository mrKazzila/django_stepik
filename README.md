<h1 align="center">🛍️ Store 🛍️</h1>

<br>

The project for study Django.

[Stepik | Backend development on Django: from scratch to a specialist](https://stepik.org/course/125859/info)

[View project (prod version)](https://store-server-test.ru/)


#### Stack:

- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev/en/stable/index.html)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.
1. Firstly clone repo
   ```bash
   git clone git@github.com:Kazzila/django_stepik.git
   ```

2. Install Poetry
   ```bash
   pip install poetry
   ```

3. Settings Poetry
   ```bash
   poetry config virtualenvs.in-project true
   ```
   
4. Install packages:
   ```bash
   poetry install
   ```
   
5. Run project dependencies, migrations, fill the database with the fixture data etc.:
   ```bash
   ./manage.py migrate
   ./manage.py loaddata <path_to_fixture_files>
   ./manage.py runserver 
   ```
   
6. Run [Redis Server](https://redis.io/docs/getting-started/installation/):
   ```bash
   redis-server
   ```
   
7. Run Celery:
   ```bash
   celery -A store worker --loglevel=INFO
   ```
