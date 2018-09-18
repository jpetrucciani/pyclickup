# pyclickup

[![PyPI version](https://badge.fury.io/py/pyclickup.svg)](https://badge.fury.io/py/pyclickup)
[![Build Status](https://travis-ci.org/jpetrucciani/pyclickup.svg?branch=master)](https://travis-ci.org/jpetrucciani/pyclickup)
[![Coverage Status](https://coveralls.io/repos/github/jpetrucciani/pyclickup/badge.svg?branch=master)](https://coveralls.io/github/jpetrucciani/pyclickup?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A python wrapper for the ClickUp API

## Quick start

### Installation

```bash
# install pyclickup
pip install pyclickup
```

### Basic Usage

```python
from pyclickup import ClickUp


clickup = ClickUp('$ACCESS_TOKEN')

main_team = clickup.teams[0]
main_space = main_team.spaces[0]
members = main_space.members

main_project = main_space.projects[0]
main_list = main_project.lists[0]

tasks = main_list.get_all_tasks(include_closed=True)
```
