import ckan.plugins as plugins
import ckan.lib.helpers as helpers
import pylons.config as config

def piwik_url_config():
    return config.get('ckan.piwik.url')


class PiwikPluginClass(plugins.SingletonPlugin):
    """
    Setup plugin
    """

    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IConfigurable, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)


    def update_config(self, config):
        print 'piwik: update_config'
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_resource('fanstatic', 'piwik')

    def get_helpers(self):

        return {'ckanext_piwik_piwik_url': piwik_url_config}