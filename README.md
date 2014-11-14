ckanext-piwik
==========

Adds page tracking statistics using a remote [Piwik](http://piwik.org) web analytics instance. Unlike Google Analytics which is a service that you use an account to access, Piwik is open source software which you can easily deploy on a remote server.  [Piwik setup instructions](http://piwik.org)

Piwik does offer some form of hosting services but this extension covers the use case where you have a deployed instance.

To do:

+ Add more stats. Currently just adds package page views stats
+ Currently doesn't account for pages with locale e.g. /fr/dataset/
+ Not tested for case where Piwik accessed over HTTPS (presumably okay, but untested nonetheless)  

Piwik setup
---------------
In Piwik, you need to configure a new site for tracking your CKAN instance or get the details for an existing configured site

To create new site

1. Login to Piwik
2. Click 'Admin' -> 'Settings'
3. Click 'Websites' in left-hand menu
4. Click 'Add a new website'

Get the the Site ID (sites are numbers 1,2,3 etc.)

In the Websites setting page, click 'View Tracking Code' for the CKAN site to get the tracking code.

Get the API authentication token

1. Click 'Admin' -> 'API'
2. Get the string that follows '&token_auth=' 

ckanext-piwik configuration
---------------------------

Install extension:

    cd /usr/lib/ckan/default/src
    git clone https://github.com/george-sattler/ckanext-piwik
    cd ckanext-piwik
    pip install -r requirements.txt
    python setup develop


Add 'piwik' to the list of extensions in the .ini file e.g. /etc/ckan/default/production.ini

    plugins = ... piwik


Add configuration items to [app:main] section:

Get the `src` value from the `<img>` tag in the `<noscript>` element of the piwik tracking code for the site (see above Piwik setup for where to find tracking code) e.g.

    <noscript><p><img src="//my_remote_server/piwik.php?idsite=1" style="border:0;" alt="" /></p></noscript>

Add the src value here:

    ckan.piwik.url = 

Add the auth token:

    ckan.piwik.auth_token = 
    
Add the site id:

    ckan.piwik.site_id = 
    
Flag whether your Piwik site uses HTTPS e.g.

    ckan.piwik.https = 
    
Add number of days to be counted as 'recent'

    ckan.piwik.recernt_days = 

Sample of complete configuration:

    ckan.piwik.url = //my_remote_server/piwik.php?idsite=1
    ckan.piwik.auth_token = ba66be936a7ac45fd33e
    ckan.piwik.site_id = 1
    ckan.piwik.https = False
    ckan.piwik.recent_days = 14

Edit `ckanext-piwik/ckanext/piwik/fanstatic/piwik.js` and paste in the Javascript tracking code for the site:
NOTE: only paste in the code _between_ the script tags. For example:


    var _paq = _paq || [];
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {
        var u="//my_remote_server/";
        _paq.push(['setTrackerUrl', u+'piwik.php']);
        _paq.push(['setSiteId', 2]);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
      })();


Restart web server


Run the update task
----------------------------
    cd ckanext-piwik
    paster piwik update -c /etc/ckan/default/production.ini

Run the update task daily (e.g. with cron) to refresh statistics.

Notes
--------
+ doesn't affect the native page tracking feature
