# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="Vaultier",
    install_requires=[
        'BeautifulSoup==3.2.1',
        'Django==1.7.3',
        'argparse==1.2.1',
        'cssutils==1.0',
        'django-appconf==0.6',
        'django-extensions==1.2.5',
        'django-filter==0.7',
        'djangorestframework==2.4.3',
        'flup==1.0.2',
        'html2text==3.200.3',
        'jsonfield==0.9.20',
        'psycopg2==2.5.1',
        'pycrypto==2.6.1',
        'pynliner==0.5.0',
        'six==1.9',
        'wsgiref==0.1.2',
        'raven==5.0.0',
        'pytz==2014.7',
        'celery==3.1.9',
        'requests==2.3.0',
        'python-dateutil==2.2',
        'logan==0.5.10',
        'django-mptt==0.6.1',
        'iso8601==0.1.10',
        'django-mptt-acl==0.1.0'
    ],
    dependency_links=['git+git@git.rclick.cz:jakub.bokoc/django-mptt-acl.git#egg=Django_MPTT_ACL'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    entry_points={
        'console_scripts': [
            'vaultier = vaultier.runner:main'
        ],
    },
    data_files=[
        (
            'vaultier-config-examples',
            ['cfg/nginx', 'cfg/supervisord', 'cfg/uwsgi']
        )
    ],
    packages=['vaultier', ],
    author=u"rclick s.r.o.",
    author_email='info@rclick.cz',
    zip_safe=True,
    include_package_data=True,
    description="Vaultier project backend",
    long_description="Vaultier combines strong security with the option to "
                     "share sensitive data within the working teams, supliers "
                     "and clients. Concept of Vaultier tool was based on our "
                     "own needs and was designed to solve our problem to "
                     "collaborate on hundreds of login credentials with the "
                     "proper level of security and access control.",
    #version="1.0.0",
    url="https://www.vaultier.org"
)
