LTI 1.3 Development Scripts
###########################

This is a collection of scripts used on the development of LTI 1.3 platforms or tools.
I created these scripts as a set of tools to help on the debugging of LTI 1.3 platform or tools.

Getting Started
***************

Setup
=====

- Clone this repository
- Set up a virtualenv

.. code-block:: bash

  cd lti1p3_scripts
  virtualenv venv
  source venv/bin/activate

- Install dependencies.

.. code-block:: bash

  make requirements

- Create an platforms.json configuration file.
- Add a configuration for a platform to platforms.json file. (Use platforms.example.json has an example).

Scripts
=======

- token_request.py: Request LTI 1.3 Service Token.
