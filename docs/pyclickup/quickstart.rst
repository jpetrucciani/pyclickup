.. _quickstart:

Quickstart
==========

This document presents a brief, high-level overview of pyclickup's primary features.

pyclickup is a python wrapper for the ClickUp API

.. note::
    Be aware that this uses the `ClickUP API <https://clickup.com/api>`_ directly. The ClickUp API is currently in beta, and is subject to change.

At the time of writing, ClickUp has the following limits in place for API requests:

- 100 requests per minute per token

Installation
------------

.. code-block:: bash

    # install pyclickup
    pip install pyclickup


Basic Usage
-----------

.. code-block:: python

   from pyclickup import ClickUp


   clickup = ClickUp('$ACCESS_TOKEN')

   main_team = clickup.teams[0]
   main_space = main_team.spaces[0]
   members = main_space.members

   main_project = main_space.projects[0]
   main_list = main_project.lists[0]

   tasks = main_list.get_all_tasks(include_closed=True)
