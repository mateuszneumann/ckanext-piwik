from sqlalchemy import Table, Column, types, orm
from ckan.model.meta import metadata
from ckan.model import Session

piwik_package_table = Table('piwik_package', metadata,
                            Column('package_name', types.UnicodeText, primary_key=True),
                            Column('total_visits', types.Integer),
                            Column('recent_visits', types.Integer),
                            )


class PiwikPackage(object):
    pass

orm.mapper(PiwikPackage, piwik_package_table)

def setup_db():

    piwik_package_table.create(checkfirst=True)


def update_package_stats(package_name, total_visits, recent_visits):
    q_result = Session.query(PiwikPackage).filter(PiwikPackage.package_name == package_name).first()

    #update if package is already in table
    if q_result:
        q_result.total_visits = total_visits
        q_result.recent_visits = recent_visits
        Session.commit()
    else:
        #add new entry for package
        pt = PiwikPackage()
        pt.package_name = package_name
        pt.total_visits = total_visits
        pt.recent_visits = recent_visits
        Session.add(pt)
        Session.commit()


def get_stats_for_package(package_name):
    q_result = Session.query(PiwikPackage).filter(PiwikPackage.package_name == package_name).first()

    if not q_result:
        return None

    return {'total': q_result.total_visits,
            'recent': q_result.recent_visits}

