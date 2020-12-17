"""
Setup script for the final project
"""

from setuptools import setup

setup(
    name='MovieApp',
    version='0.1.0',
    packages=['MovieApp'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'nodeenv',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
        'selenium',
        'psycopg2-binary',
    ],
    python_requires='>=3.6',

)
