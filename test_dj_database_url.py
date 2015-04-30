# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import unittest

import dj_database_url


CUSTOM_SCHEMES = {
    'somecustomdb': 'somecustomdb.django.backend',
    'mysql': 'django_mysqlpool.backends.mysqlpool',
    'postgres': 'django_db_geventpool.backends.postgresql_psycopg2',
}

ENVIRON_VARNAME = 'DATABASE_URL'

class TEST_URL:
    CLEARDB = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
    MYSQLGIS = 'mysqlgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
    POSTGRESS = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
    POSTGRESS_UNIX = 'postgres://%2Fvar%2Frun%2Fpostgresql/d8r82722r2kuvn'
    POSTGIS = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
    SOMECUSTOMDB = 'somecustomdb://someuser:somepassword@some-location.somecustomdbdomain.com/some_db_key'


class DatabaseTestSuite(unittest.TestCase):

    def test_postgres_parsing(self):
        url = dj_database_url.parse(TEST_URL.POSTGRESS)

        assert url['ENGINE'] == dj_database_url.SCHEMES['postgres']
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_postgres_unix_socket_parsing(self):
        url = dj_database_url.parse(TEST_URL.POSTGRESS_UNIX)

        assert url['ENGINE'] == dj_database_url.SCHEMES['postgres']
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == '/var/run/postgresql'
        assert url['USER'] == ''
        assert url['PASSWORD'] == ''
        assert url['PORT'] == ''

    def test_postgis_parsing(self):
        url = dj_database_url.parse(TEST_URL.POSTGIS)

        assert url['ENGINE'] == dj_database_url.SCHEMES['postgis']
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_mysql_gis_parsing(self):
        url = TEST_URL.MYSQLGIS
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == dj_database_url.SCHEMES['mysqlgis']
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_cleardb_parsing(self):
        url = TEST_URL.CLEARDB
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == dj_database_url.SCHEMES['mysql']
        assert url['NAME'] == 'heroku_97681db3eff7580'
        assert url['HOST'] == 'us-cdbr-east.cleardb.com'
        assert url['USER'] == 'bea6eb025ca0d8'
        assert url['PASSWORD'] == '69772142'
        assert url['PORT'] == ''

    def test_database_url(self):
        del os.environ[ENVIRON_VARNAME]
        a = dj_database_url.config()
        assert not a

        os.environ[ENVIRON_VARNAME] = TEST_URL.POSTGRESS

        url = dj_database_url.config()

        assert url['ENGINE'] == dj_database_url.SCHEMES['postgres']
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_empty_sqlite_url(self):
        url = 'sqlite://'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == dj_database_url.SCHEMES['sqlite']
        assert url['NAME'] == ':memory:'

    def test_memory_sqlite_url(self):
        url = 'sqlite://:memory:'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == dj_database_url.SCHEMES['sqlite']
        assert url['NAME'] == ':memory:'

    def test_parse_engine_setting(self):
        engine = CUSTOM_SCHEMES['mysql']
        url = TEST_URL.CLEARDB
        url = dj_database_url.parse(url, engine)

        assert url['ENGINE'] == engine

    def test_config_engine_setting(self):
        engine = CUSTOM_SCHEMES['mysql']
        os.environ[ENVIRON_VARNAME] = TEST_URL.CLEARDB
        url = dj_database_url.config(engine=engine)

        assert url['ENGINE'] == engine

    def test_parse_custom_schemes(self):
        method = dj_database_url.parse

        url1 = method(TEST_URL.SOMECUSTOMDB, custom_schemes=CUSTOM_SCHEMES)
        url2 = method(TEST_URL.CLEARDB, custom_schemes=CUSTOM_SCHEMES)
        url3 = method(TEST_URL.POSTGRESS, custom_schemes=CUSTOM_SCHEMES)

        assert url1['ENGINE'] == CUSTOM_SCHEMES['somecustomdb']
        assert url2['ENGINE'] == CUSTOM_SCHEMES['mysql']
        assert url3['ENGINE'] == CUSTOM_SCHEMES['postgres']

    def test_config_custom_schemes(self):
        method = dj_database_url.config

        os.environ[ENVIRON_VARNAME] = TEST_URL.SOMECUSTOMDB
        url1 = method(ENVIRON_VARNAME, custom_schemes=CUSTOM_SCHEMES)

        os.environ[ENVIRON_VARNAME] = TEST_URL.CLEARDB
        url2 = method(ENVIRON_VARNAME, custom_schemes=CUSTOM_SCHEMES)

        os.environ[ENVIRON_VARNAME] = TEST_URL.POSTGRESS
        url3 = method(ENVIRON_VARNAME, custom_schemes=CUSTOM_SCHEMES)

        assert url1['ENGINE'] == CUSTOM_SCHEMES['somecustomdb']
        assert url2['ENGINE'] == CUSTOM_SCHEMES['mysql']
        assert url3['ENGINE'] == CUSTOM_SCHEMES['postgres']


if __name__ == '__main__':
    unittest.main()
