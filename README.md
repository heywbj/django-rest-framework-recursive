# djangorestframework-recursive

[![build-status-image]][travis]
[![pypi-version]][pypi]

## Overview

Recursive Serialization for Django REST framework

## Requirements

* Python (2.7, 3.3, 3.4)
* Django (1.6, 1.7)
* Django REST Framework (3.0)

## Installation

Install using `pip`...

```bash
$ pip install djangorestframework-recursive
```

## Example

```python
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

class TreeSerializer(serializers.Serializer):
    name = serializers.CharField()
    children = serializers.ListField(child=RecursiveField())
```

see [tests][here] for more usage examples

## Testing

Install testing requirements.

```bash
$ pip install -r requirements.txt
```

Run with runtests.

```bash
$ ./runtests.py
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
$ tox
```


[build-status-image]: https://secure.travis-ci.org/heywbj/django-rest-framework-recursive.png?branch=master
[travis]: http://travis-ci.org/heywbj/django-rest-framework-recursive?branch=master
[pypi-version]: https://pypip.in/version/djangorestframework-recursive/badge.svg
[pypi]: https://pypi.python.org/pypi/djangorestframework-recursive
[tests]: https://github.com/heywbj/django-rest-framework-recursive/blob/master/tests/test_recursive.py
