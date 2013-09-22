"""
Dump jira tickets to json
"""
from distutils.core import setup

setup(
    name='jira2json',
    version='0.1.0',
    packages=['jira2json',],
    long_description=__doc__,
    author = "Konstantin Nazarov",
    author_email = "mail@kn.am",
    license='MIT',
    install_requires=[
        'requests>=0.8.2',
    ],
    entry_points={
        'console_scripts': [
            'jira2json = jira2json:_main',
        ],
    },
)
