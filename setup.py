from setuptools import setup

setup(
    name='Project507',
    version='0.1.0',
    packages=['Project507'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'requests',
    ],
    # entry_points={
    #     'console_scripts': [
    #         'Project507 = Project507.__init__:start'
    #     ]
    # },
)
