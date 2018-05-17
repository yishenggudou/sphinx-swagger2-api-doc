=====================================
sphinxcontrib-sphinx-swagger2-api-doc
=====================================

.. image:: https://travis-ci.org/yishenggudou/sphinxcontrib-sphinx-swagger2-api-doc.svg?branch=master
    :target: https://travis-ci.org/yishenggudou/sphinxcontrib-sphinx-swagger2-api-doc

a tools for sphinx gen doc from swagger2 api

Overview
--------

Add a longer description here.

INSTALL
--------------------

.. code-block::bash

    pip install sphinxcontrib-sphinx-swagger2-api-doc


USAGE
----------


in config.py

.. code-block::py
    
  extensions += ['sphinxcontrib.swagger2', ]
  swagger_api_url = os.path.join(PROJECT_DIR, "_static", "api-docs.json")
  swagger_api_domain = "timger.com.cn"

in rst file

.. code-block:: rst

    .. swagger:: /v1/api/test/
        :method: GET
        :title: test API
        :summary: sssss

Links
-----

- Source: https://github.com/yishenggudou/sphinxcontrib-sphinx-swagger2-api-doc
- Bugs: https://github.com/yishenggudou/sphinxcontrib-sphinx-swagger2-api-doc/issues
