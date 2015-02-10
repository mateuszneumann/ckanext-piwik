from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-piwik',
    version=version,
    description="Page tracking statistics using a remote Piwik instance",
    long_description='''Adds page tracking statistics using a remote Piwik
    web analytics instance.  Extension originally written by George
    Sattler.''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='George Sattler, Mateusz Neumann',
    author_email='M.Neumann@icm.edu.pl',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.piwik'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        piwik=ckanext.piwik.plugin:PiwikPluginClass

        [paste.paster_command]
        piwik=ckanext.piwik.commands:PiwikTrackingUpdate
    ''',
)
