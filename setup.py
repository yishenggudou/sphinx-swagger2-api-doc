#!/usr/bin/env python

import setuptools, os
from setuptools import setup, find_packages

root = os.path.dirname(os.path.abspath(__file__))

setuptools.setup(
    setup_requires=['pbr', "sphinxcontrib-httpdomain", "jinja2"],
    pbr=True,
    url='https://github.com/yishenggudou/sphinx_swagger2_api_doc',
    python_requires='>3.0',
    include_package_data=True,
    license='BSD 2',
    version='0.0.3',
    author='timger',
    packages=find_packages(),
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    namespace_packages=['sphinxcontrib'],
    author_email='yishenggudou@gmail.com',
    # setup_requires=['flask', 'gevent', 'requests', 'browsercookie'],
    description=open(os.path.join(root, 'README.rst')).read(),
)
