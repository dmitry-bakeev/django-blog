# django-blog
This is the solution of a [test task](https://docs.google.com/document/d/1oS2m4lLskCUQCUpPqzwcS8mcPCAvlBLqUM6u-cHc_38/edit) for the position of Django backend developer

Requirements:
 - git
 - docker and docker-compose

How to run:

1. Clone this repo

```bash
# If use https
git clone https://github.com/dmitry-bakeev/django-blog.git

# if use ssh
git clone git@github.com:dmitry-bakeev/django-blog.git
```

2. Edit `./docker-compose.yml`. Set your own environments for backend and celery_worker services:

- `SITE_ROOT` - using for generate link in email, you can set public IP or domain name

- `EMAIL_HOST`

- `EMAIL_HOST_USER`

- `EMAIL_HOST_PASSWORD`

- `DEFAULT_FROM_EMAIL`

3. Run project

```bash
docker-compose up -d
```

4. Create first user

```bash
./manage.sh createsuperuser
```

5. Open url `http://localhost`. if you change `SITE_ROOT` open your public IP or domain name

6. Enjoy
