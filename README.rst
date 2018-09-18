
pyclickup
=========


.. image:: https://badge.fury.io/py/pyclickup.svg
   :target: https://badge.fury.io/py/pyclickup
   :alt: PyPI version


.. image:: https://travis-ci.org/jpetrucciani/pyclickup.svg?branch=master
   :target: https://travis-ci.org/jpetrucciani/pyclickup
   :alt: Build Status


.. image:: https://coveralls.io/repos/github/jpetrucciani/pyclickup/badge.svg?branch=master
   :target: https://coveralls.io/github/jpetrucciani/pyclickup?branch=master
   :alt: Coverage Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code style: black


A python wrapper for the ClickUp API

Quick start
-----------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   # install pyclickup
   pip install pyclickup

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from pyclickup import ClickUp


   clickup = ClickUp('$ACCESS_TOKEN')

   main_team = clickup.teams[0]
   main_space = main_team.spaces[0]
   members = main_space.members

   main_project = main_space.projects[0]
   main_list = main_project.lists[0]

   tasks = main_list.get_all_tasks(include_closed=True)
