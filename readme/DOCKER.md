<h1 align="center">
  <br>
  <a href="https://stepik.org/course/125859/info">
    <img src="stepik.jpeg"
    alt="Stepik" width="200">
  </a>
  <br>
  Docker commands
  <br>
</h1>

<hr>

<p align="center">
  <a href="#how-to-use">How To Use</a> •
  <a href="#local-env">Local env</a> •
  <a href="#prod-env">Prod env</a>
</p>


## How To Use
To use this command, you'll need:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker compose](https://docs.docker.com/compose/install/)


### Local env
<details>
<summary>Step-by-step commands</summary>

1. Create containers
   ```bash
   docker-compose -f docker-compose.yaml build
   ```

2. Containers up
   ```bash
   docker-compose -f docker-compose.yaml up -d
   ```

3. Or create & build
   ```bash
   docker-compose -f docker-compose.yaml up -d --build
   ```

4. Stop containers
   ```bash
   docker-compose down -v
   ```

</details>


### Prod env
<details>
<summary>Step-by-step commands</summary>

1. Create containers
   ```bash
   sudo docker-compose -f docker-compose.prod.yaml build
   ```

2. Containers up
   ```bash
   sudo docker-compose -f docker-compose.prod.yaml up -d
   ```

3. Or create & build
   ```bash
   sudo docker-compose -f docker-compose.prod.yaml up -d --build
   ```

4. Enter into container
   ```bash
   sudo docker-compose -f docker-compose.prod.yaml exec django bash
   ```

5. run Migrate into container
   ```bash
   sudo docker-compose -f docker-compose.prod.yaml exec django python app/manage.py migrate --noinput
   ```

6. Create superuser (?)
   ```bash
   sudo docker-compose -f docker-compose.prod.yaml exec django python app/manage.py createsuperuser
   ```

7. Collect static into container
   ```bash
   sudo docker-compose -f docker-compose.prod.yaml exec django python app/manage.py collectstatic --noinput --clear
   ```

8. Generate Let's Encrypt cert
    ```bash
      sudo docker-compose run --rm --entrypoint "\
      certbot certonly --webroot -w /var/store/web \
      --email <your_email> \
      -d <your_domain> \
      --rsa-key-size 2048 \
      --agree-tos \
      --force-renewal" certbot
      ```

9. Stop containers
   ```bash
   sudo docker-compose down -v
   ```

</details>


<br>
<br>
<p align="center">
  <a href="https://github.com/mrKazzila">GitHub</a> •
  <a href="https://mrkazzila.github.io/resume/">Resume</a> •
  <a href="https://www.linkedin.com/in/i-kazakov/">LinkedIn</a>
</p>
