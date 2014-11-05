ckanext-piwik
=============

Adds page tracking using a remote [Piwik](https://www.google.com) web analytics instance. Unlike Google Analytics which is a service that you use an account to access, Piwik is open source software which you can easily deploy on a remote server (see Piwik website for deployment and setup instructions).

Piwik Javascript Tracking Code
-------------

Configuring one or more sites in Piwik is trivial following the installation but you need to obtain the Javascript tracking code for the site that you want to track (if you didn't already copy it down during the site setup):

1. Click Admin -> Settings
2. Click Websites in the left-hand menu
3. Click 'View Tracking Code'

ckanext-piwik configuration
---------------------------

Install extension:


    cd /usr/lib/ckan/default/src
    git clone https://github.com/XVTSolutions/ckanext-piwik
    cd ckanext-piwik
    python setup develop


Add 'piwik' to the list of extensions in the .ini file e.g. /etc/ckan/default/production.ini

    plugins = ... piwik


Next, add configuration item to [app:main] section:

Get the `src` value from the `<img>` tag in the `<noscript>` element of the Javascript tracking code e.g.

    <noscript><p><img src="//0.0.0.0/piwik.php?idsite=1" style="border:0;" alt="" /></p></noscript>

For the above, the configuration value would be:

    ckan.piwik.url = //0.0.0.0/piwik.php?idsite=1


Edit _ckanext-piwik/ckanext/piwik/fanstatic/piwik.js_ and paste in the Javascript tracking code for the site:
NOTE: only paste in the code _between_ the script tags. For example:


    var _paq = _paq || [];
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {
        var u="//0.0.0.0/";
        _paq.push(['setTrackerUrl', u+'piwik.php']);
        _paq.push(['setSiteId', 2]);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
      })();


Restart web server
