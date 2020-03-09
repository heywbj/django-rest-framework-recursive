# djangorestframework-recursive

[![build-status-image]][travis]
[![pypi-version]][pypi]

## Overview

Recursive Serialization for Django REST framework

This package provides a `RecursiveField` that enables you to serialize a tree,
linked list, or even a directed acyclic graph. Also supports validation,
deserialization, ModelSerializers, and multi-step recursive structures.


## Example

```python
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

class TreeSerializer(serializers.Serializer):
    name = serializers.CharField()
    children = serializers.ListField(child=RecursiveField())
```

see [**here**][tests] for more usage examples


## Requirements

* Python (Tested on 2.7, 3.4, 3.6)
* Django (Tested on 1.8, 1.9, 2.0)
* Django REST Framework (Tested on 3.3, 3.7)


## Installation

Install using `pip`...

```bash
$ pip install djangorestframework-recursive
```

## Release notes

### 0.1.2
* This is the first release to include release notes.
* Use inspect.signature when available. This avoids emitting deprecation warnings on Python 3.
* Updated CI versions. djangorestframework-recursive is now tested against DRF
  3.3-3.6, Python 2.7 and 3.6 and Django 1.8-1.11.

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
[pypi-version]: https://img.shields.io/pypi/v/djangorestframework-recursive.svg
[pypi]: https://pypi.python.org/pypi/djangorestframework-recursive
[tests]: https://github.com/heywbj/django-rest-framework-recursive/blob/master/tests/test_recursive.py
