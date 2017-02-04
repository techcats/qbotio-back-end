[![Stories in Ready](https://badge.waffle.io/techcats/qbotio-back-end.png?label=ready&title=Ready)](https://waffle.io/techcats/qbotio-back-end)
# qbotio-back-end

Powered by Django REST framework.

## Development

See [Django](https://docs.djangoproject.com/) and [Django REST framework](http://www.django-rest-framework.org/) documentations for API usage.

### Environment Setup

1. Install [python 3.6+](https://www.python.org/)
2. Install/Update [pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip)
3. Install virtualenv: ```$ pip install virtualenv```
4. Install virtualenvwrapper. Follow and see usage with [Windows](https://pypi.python.org/pypi/virtualenvwrapper-win), [Linux & Mac](https://virtualenvwrapper.readthedocs.io) guides.
6. Create and work on a local environment (e.g. qbotio) using virtualenvwrapper.

### Git Setup

1. Clone the git repository: ```$ git clone [url]```

### Install/Update python libraries
1. cd into your local repository folder
2. Run ```$ pip install -r requirements.txt```

> To include a new library use ```$ pip install [package] && freeze > requirements.txt```

### Test Locally

```bash
$ py manage.py runserver
```

> ```py``` is the latest python on Windows. Depending on your environment it can be ```python3``` or just ```python```.

Verify by going to http://localhost:8000/.
