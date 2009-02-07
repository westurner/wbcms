#!/bin/sh

# Configure ODBC in Debian/Ubuntu
# http://lambie.org/2008/02/28/connecting-to-an-mssql-database-from-ruby-on-ubuntu/

echo "export ODBCINI=/etc/odbc.ini
export ODBCSYSINI=/etc" >> ~/.profile

# Set Host/Port in freetds/freetds.conf 

# Ubuntu packages
apt-get install freetds-dev unixodbc-dev sqsh tdsodbc

# Configure ODBC for django
easy_install pyodbc
# svn checkout http://django-pyodbc.googlecode.com/svn/trunk/ django-pyodbc
# ... to PYTHONPATH

