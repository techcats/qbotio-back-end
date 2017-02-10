[![Stories in Ready](https://badge.waffle.io/techcats/qbotio-back-end.png?label=ready&title=Ready)](https://waffle.io/techcats/qbotio-back-end)
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

> To include a new library use ```$ pip install [package] && freeze > requirements.txt```

### Test Locally

```bash
$ python manage.py runserver
```

Verify by going to http://localhost:8000/.

## Deployment

Guide for deploying back end service.

## AWS Beanstalk

### Setup
1. See [guide](https://realpython.com/blog/python/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/)
2. Modify ALLOWED_HOSTS in web/settings.py to include your Elastic Beanstalk host.
3. Configure CORS_ORIGIN_WHITELIST in web/settings.py. See [django-cors-headers](https://github.com/ottoyiu/django-cors-headers) for more details.

### Circle CI
See Gist for setting up [Circle CI configuration](https://gist.github.com/RobertoSchneiders/9e0e73e836a80d53a21e)