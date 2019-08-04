XLSForm API
===========

XLSForm API is a Flask web service that internally uses xls2xform for converting Excel.

Requirements
------------

* Python 3
* pip 3
* virtualenv

Installation
------------

Use the package manager `pip`_ to install dependencies.

.. code:: bash

   virtualenv env
   pip install -r requirements.txt

Usage
-----

In development:

.. code:: bash

   FLASK_APP=xlsform_api FLASK_DEBUG=1 python -m flask run

In production:

.. code:: bash

   FLASK_APP=xlsform_api python -m flask run

This will launch the API on port 5000.

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

License
-------

`Apache License 2.0`_

.. _pip: https://pip.pypa.io/en/stable/
.. _Apache License 2.0: https://choosealicense.com/licenses/apache-2.0/
