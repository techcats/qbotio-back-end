[![Stories in Ready](https://badge.waffle.io/techcats/qbotio-back-end.png?label=ready&title=Ready)](https://waffle.io/techcats/qbotio-back-end)
[![Build stats](https://circleci.com/gh/techcats/qbotio-back-end.svg?style=shield&circle-token=0063d363c60c818096169987c5bc7f0a5033eb60)](https://circleci.com/gh/techcats/qbotio-back-end)
# qbotio-back-end

Powered by Django REST framework.

> For front-end development visit: https://github.com/techcats/qbotio.github.io

## Development

See [Django](https://docs.djangoproject.com/) and [Django REST framework](http://www.django-rest-framework.org/) documentations for API usage.

### Git Setup

1. Clone the git repository: ```$ git clone https://github.com/techcats/qbotio-back-end.git```


### Environment Setup

1. Install [python 3.6+](https://www.python.org/)
2. Install/Upgrade [pip](https://pip.pypa.io/en/stable/installing/)
3. Install virtualenv: ```$ pip install virtualenv```
4. Install virtualenvwrapper. Follow and see usage with [Windows](https://pypi.python.org/pypi/virtualenvwrapper-win), [Linux & Mac](https://virtualenvwrapper.readthedocs.io/en/stable/) guides.
6. Create (```$ mkvirtualenv qbotio```) and work (```$ workon qbotio```) on a local environment using virtualenvwrapper.
7. Set the default project directory: ```(qbotio) $ setvirtualenvproject <path to cloned repo>``` or use ```setprojectdir``` (Windows)
8. ```(qbotio) $ deactivate```
9. ```$ workon qbotio```

You should now be at the root directory of 'qbotio-back-end/'. Calling ```$ workon qbotio``` should now automatically direct to the your sources directory.

> A tip for step 3 & 4 (Linux & Mac): Similiar to ```python3```, ```pip3``` is the python 3.x's equivalent. virtualenvwrapper.sh may require the correct python version in your "VIRTUALENVWRAPPER_PYTHON" environment variable.

### Install/Update python libraries

Run ```(qbotio) $ pip install -r requirements.txt```

> To include a new library use ```(qbotio) $ pip install [package]```, and then ```(qbotio) $ pip freeze > requirements.txt```

### Configure settings.json

In the top most directory, create etc/settings.json. Add the following JSON, for example:
```json
{
  "SECRET_KEY": "secret",
  "ALLOWED_HOSTS": [
    "localhost",
    "127.0.0.1",
    "api.qbotio.com",
    "qbotio.us-west-2.elasticbeanstalk.com"
  ],
  "DATABASES" : {
    "default": {
      "NAME" : "F:\\github\\qbotio-back-end\\db.sqlite3"
    },
    "repository": {
        "ENGINE": "django_mongodb_engine",
        "NAME": "qbotio",
        "USER": "admin",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "PORT": 27017
    }
  }
}
```

### Configure Administration

> For now, this is only required once for setup. If db.sqlite3 file exist, delete it: ```$ rm -f tmp.db db.sqlite3```

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

### Test Locally

```bash
$ python manage.py runserver
```

Verify by going to http://localhost:8000/.

## Deployment

Guide for deploying back end service.

## AWS Beanstalk

### Setup

> See [guide](https://realpython.com/blog/python/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/)

#### Configure environment variables

1. Create setting.json and upload it to your S3 bucket associated to your Elastic Beanstalk instance
2. Modifiy .ebextentions/environment.config to use the bucket

### Circle CI
See Gist for setting up [Circle CI configuration](https://gist.github.com/RobertoSchneiders/9e0e73e836a80d53a21e)