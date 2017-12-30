ledgerlink-contract
===================

|

Ledgerlink (or ledgr.link) is a URL shortener service that uses the NEO blockchain as a mean to
store irreplaceable short URLs. Such shortened URLs are protected against any third party
interferences because they cannot be changed by anybody - they will live forever on the NEO
blockchain. Thus the NEO blockchain is used as a source of trust, ensuring that the shortened links
always lead to where they are supposed to.

This repository embeds the smart contract used by the Ledgerlink service. This smart contract
provides a secure way of generating shortened-URLs and storing the related uniques codes into the
NEO blockchain. This smart contract is written in Python and makes use of the neo-boa_ compiler.

.. contents:: Table of Contents
    :local:

Main requirements
-----------------

* Python_ 3.4 or 3.5.
* Pipenv_ 3.5+

Development setup
-----------------

Quickstart
~~~~~~~~~~

You can install the project locally using the following commands:

.. code-block:: shell

  $ git clone https://github.com/ellmetha/ledgerlink-contract && cd ledgerlink-contract
  $ pipenv install --dev --python /usr/bin/python3.5  # or any other valid path

Once all the dependencies have been installed, you can trigger the compilation of the smart contract
using the following command:

.. code-block:: shell

  $ make avm

The resulting ``ledgerlink.avm`` file will be stored under the ``./build`` directory.

Testing the contract using a privnet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

License
-------

MIT. See ``LICENSE`` for more details.


.. _neo-boa: https://github.com/CityOfZion/neo-boa
.. _Pipenv: https://github.com/kennethreitz/pipenv
.. _Python: https://www.python.org
