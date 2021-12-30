# django-blog
This is the solution of a test task for the position of Django backend developer

Requirements:
 - git
 - docker and docker-compose

How to run

1. Clone this repo

```bash
# If use https
git clone https://github.com/dmitry-bakeev/django-blog.git

# if use ssh
git clone git@github.com:dmitry-bakeev/django-blog.git
```

2. Build images

```bash
# backend
docker build . -f backend.Dockerfile -t backend:latest

# frontend
docker build . -f frontend.Dockerfile -t frontend:latest
```

3. Edit `./docker-compose.yml`. Set your own environments for backend and celery_worker services:

- `EMAIL_HOST`

- `EMAIL_HOST_USER`

- `EMAIL_HOST_PASSWORD`

- `DEFAULT_FROM_EMAIL`

4. Run project

```bash
docker-compose up -d
```

5. Create first user
```
./manage.sh createsuperuser
```

6. Open url `http://localhost`

7. Enjoy