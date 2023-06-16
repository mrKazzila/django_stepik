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
   docker-compose -f docker-compose.yaml down -v
   ```


### Prod env
[DEPLOY](DEPLOY.md)


<br>
<br>
<p align="center">
  <a href="https://github.com/mrKazzila">GitHub</a> •
  <a href="https://mrkazzila.github.io/resume/">Resume</a> •
  <a href="https://www.linkedin.com/in/i-kazakov/">LinkedIn</a>
</p>
