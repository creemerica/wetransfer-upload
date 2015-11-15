wetransfer-upload
=================

|PyPI version| |PyPI license|

Upload files or directories to WeTransfer. Tie into your Bitly account
to create custom short urls for your downloads. Inspired by
`upload-wetransfer <https://github.com/kraynel/upload-wetransfer>`__ by
`kraynel <https://github.com/kraynel>`__.

Feautures
---------

-  Upload files or directories of files
-  Create custom bitly link for upload
-  Show progress of upload

Installation
------------

``$ pip install wetransfer-upload``

Usage
-----

.. code:: python

    from wetransfer import WeTransfer

    wt = WeTransfer()
    upload = wt.start('file.txt')
    print upload

.. |PyPI version| image:: https://badge.fury.io/py/wetransfer-upload.svg
   :target: https://badge.fury.io/py/wetransfer-upload
.. |PyPI license| image:: https://img.shields.io/pypi/l/wetransfer-upload.svg
   :target: https://img.shields.io/pypi/l/wetransfer-upload.svg
