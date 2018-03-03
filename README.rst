.. raw:: html

    <p align="center">
      <img
        src="https://raw.githubusercontent.com/ellmetha/ledgerlink-contract/master/_files/ledgerlink_logo.svg"
        width="125px;">
    </p>

    <h1 align="center">ledgerlink-contract</h1>

    <p align="center">
        Smart contract backing a hypothetical ledgr.link URL shortener service.
    </p>

|
|

Ledgerlink (or ledgr.link) is a hypothetical URL shortener service that uses the NEO blockchain as a
mean to store irreplaceable / unfalsifiable short URLs. Such shortened URLs are protected against
any third party interferences because they cannot be changed by anybody - they will live forever on
the NEO blockchain. Thus the NEO blockchain is used as a source of trust, ensuring that the
shortened links always lead to where they are supposed to.

This repository embeds the smart contract used by this URL shortener service. This smart contract
provides a secure way of generating shortened-URLs and storing the related uniques codes into the
NEO blockchain. It is written in Python and makes use of the neo-boa_ compiler.

.. contents:: Table of Contents
    :local:

Main requirements
=================

* Python_ 3.4 or 3.5.
* Pipenv_ 3.5+

Development setup
=================

Quickstart
----------

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
------------------------------------

You'll need a working Docker_ installation in order to set up such privnet. The first thing to do
is to pull a Docker image containing a working NEO privnet and a wallet associated with a convenient
amount of GAS.

.. code-block:: shell

  $ docker pull metachris/neo-privnet-with-gas
  $ curl https://s3.amazonaws.com/neo-experiments/neo-privnet.wallet -o /tmp/neo-privnet.wallet

You can now start up the privnet using the following command:

.. code-block:: shell

  $ docker run -d --name neo-privnet-with-gas -p 20333-20336:20333-20336/tcp -p 30333-30336:30333-30336/tcp metachris/neo-privnet-with-gas

You now pull the latest version of neo-python_ and start the node with PrivNet configuration using:

.. code-block:: shell

  $ git clone https://github.com/CityOfZion/neo-python
  $ python prompt.py -p

At this point it should possible to open the pre-configured wallet, deploy the compiled version of
the smart contract and start interacting with it:

.. code-block:: shell

  # Open the wallet ; password is: coz
  neo> open wallet /tmp/neo-privnet.wallet
  [password]> ***
  Opened wallet at /tmp/neo-privnet.wallet

  # Rebuild wallet and associated assets.
  neo> wallet rebuild

  # Deploy the compiled AVM version of the ledgerlink contract.
  neo> import contract /path/to/ledgerlink-contract/build/ledgerlink.avm 0710 01 True False
  contract properties: 1
  Please fill out the following contract details:
  [Contract Name] > ledgerlink
  [Contract Version] > 1
  [Contract Author] >
  [Contract Email] >
  [Contract Description] >
  Creating smart contract....
                   Name: ledgerlink
                Version: 1
                 Author:
                  Email:
            Description:
          Needs Storage: True
   Needs Dynamic Invoke: False

  # Wait for the contract to be persisted to the blockchain... and retrieve the hash script of the
  # contract using the search command.
  neo> contract search ledgerlink

  # Invoke the smart contract in order to add a new URL
  neo> testinvoke <scriptHash> addURL ['https://neo.org'] --attach-gas=0.001

  # Wait for the transaction to be confirmed and copy the generated code from the logs.
  # It should now be possible to retrieve the URL using the code with the following invocation.
  neo> testinvoke <scriptHash> getURL ['<code>'] --attach-gas=0.001

License
=======

MIT. See ``LICENSE`` for more details.


.. _Docker: https://www.docker.com/
.. _neo-boa: https://github.com/CityOfZion/neo-boa
.. _neo-python: https://github.com/CityOfZion/neo-python
.. _Pipenv: https://github.com/kennethreitz/pipenv
.. _Python: https://www.python.org
