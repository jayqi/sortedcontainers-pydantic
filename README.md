# sortedcontainers-pydantic

[![PyPI](https://img.shields.io/pypi/v/sortedcontainers-pydantic.svg)](https://pypi.org/project/sortedcontainers-pydantic/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/sortedcontainers-pydantic)](https://pypi.org/project/sortedcontainers-pydantic/)
[![tests](https://github.com/jayqi/sortedcontainers-pydantic/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jayqi/sortedcontainers-pydantic/actions/workflows/tests.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/jayqi/sortedcontainers-pydantic/branch/main/graph/badge.svg)](https://codecov.io/gh/jayqi/sortedcontainers-pydantic)

This package adds [Pydantic](https://docs.pydantic.dev/latest/) support to [sortedcontainers](https://github.com/grantjenks/python-sortedcontainers/), a fast, pure-Python sorted collections library. 

It implements [Pydantic's special methods](https://docs.pydantic.dev/latest/concepts/types/#customizing-validation-with-__get_pydantic_core_schema__) on sortedcontainer's `SortedDict`, `SortedList`, and `SortedSet` classes so that you can use them with Pydantic's models, validation, and serialization. To use, simply import the respective class from `sortedcontainers_pydantic` instead of `sortedcontainers`. 

```python
from pydantic import BaseModel, TypeAdapter
from sortedcontainers_pydantic import SortedList

class MyModel(BaseModel):
    sorted_list: SortedList

MyModel(sorted_list=[3, 1, 2])
#> MyModel(sorted_list=SortedList([1, 2, 3]))

TypeAdapter(SortedList).validate_python([3, 1, 2])
#> SortedList([1, 2, 3])

TypeAdapter(SortedList).validate_json("[3, 1, 2]")
#> SortedList([1, 2, 3])
```

<sup>Reproducible example created by [reprexlite](https://github.com/jayqi/reprexlite) v0.5.0</sup>

## Installation

...
