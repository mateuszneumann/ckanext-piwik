import json
from pprint import pprint
from logging import getLogger

import ckan.plugins as plugins
import ckan.lib.base as base
import ckan.lib.helpers as helpers
import pylons.config as config
from model import setup_db, get_stats_for_package

log = getLogger(__name__)

def piwik_url_config():
    return config.get('ckan.piwik.url')

def stats_for_package(package_name):
    stats = get_stats_for_package(package_name)
    return base.render_snippet('piwik_snippets/piwik_stats.html',
                               total=stats['total'],
                               recent=stats['recent'],
                               recent_days=recent_days())

def recent_days():
    return config.get('ckan.piwik.recent_days')

class PiwikPluginClass(plugins.SingletonPlugin):
    """
    Setup plugin
    """

    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_resource('fanstatic', 'piwik')

        setup_db()

    def get_helpers(self):
        return {'ckanext_piwik_piwik_url': piwik_url_config,
                'ckanext_piwik_stats_for_package': stats_for_package,
                'ckanext_piwik_recent_days': recent_days}

