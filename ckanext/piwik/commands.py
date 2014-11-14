import logging
import sys
from datetime import date, timedelta

import requests
import pylons.config as config
from ckan.lib.cli import CkanCommand
import ckan.plugins.toolkit as toolkit
import model


class PiwikTrackingUpdate(CkanCommand):
    """
    Download tracking data from Piwik

    Downloading data populates the Piwik table in the CKAN database

    Usage:
        paster update [dataset] -c /etc/ckan/default/production.ini

    """

    summary = __doc__.split('\n')[0]
    usage = __doc__
    min_args = 0
    max_args = 3
    pkg_names = []

    def command(self):

        #if not correct args, show help
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print self.usage
            return

        cmd = self.args[0]
        self._load_config()

        #update command
        if cmd == 'update':
            url_id = config.get('ckan.piwik.url').split('/piwik.php')
            piwik_url = url_id[0]
            use_https = toolkit.asbool(config.get('ckan.piwik.https', False))

            if use_https:
                piwik_url = 'https:' + piwik_url
            else:
                piwik_url = 'http:' + piwik_url

            recent_date = date.today() - timedelta(days=int(config.get('ckan.piwik.recent_days', '14')))
            piwik_date_opts = {'total': '2011-01-01,today',
                                    'recent': recent_date.strftime('%Y-%m-%d') + ',today'}

            #setup piwik api GET request params
            piwik_params = {
                'idSite': config.get('ckan.piwik.site_id'),
                'token_auth': config.get('ckan.piwik.auth_token'),
                'module': 'API',
                'method': 'Actions.getPageUrl',
                'format': 'json',
                'period': 'range',
                'pageUrl': None,
                'date': None
            }

            if len(self.args) > 1:
                #update a single package
                self.update_package_stats(self.args[1],
                                          piwik_params,
                                          piwik_date_opts,
                                          piwik_url)
            else:
                #get all the packages
                pkgs_list = toolkit.get_action('package_list')(context=None, data_dict={})
                for pkg in pkgs_list:
                    self.update_package_stats(pkg,
                                              piwik_params,
                                              piwik_date_opts,
                                              piwik_url)
        else:
            print 'command: {cmd} not recognised'.format(cmd=cmd)

    def update_package_stats(self, package_name, piwik_params, piwik_date_opts, piwik_url):

        param = piwik_params.copy()
        param['pageUrl'] = '/dataset/' + package_name

        #get total visits
        param['date'] = piwik_date_opts['total']
        r_total = requests.get(piwik_url, params=param)

        #get recent visits
        param['date'] = piwik_date_opts['recent']
        r_recent = requests.get(piwik_url, params=param,)

        total = 0
        recent = 0

        if r_total.status_code == 200:
            if r_total.json():
                total = r_total.json()[0]['nb_visits']

        if r_recent.status_code == 200:
            if r_total.json():
                recent = r_recent.json()[0]['nb_visits']

        model.update_package_stats(package_name, total, recent)