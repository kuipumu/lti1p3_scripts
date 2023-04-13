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

Scripts
=======

- token_request.py: Request LTI 1.3 Service Token. To use this script first make sure to add your id_rsa and id_rsa.pub keys on the project folder. Also create a platforms.json file with a JSON containing at least one object with the name of the playtform, and it's client_id and token_url, you can use the file platforms.example.json has a reference.
