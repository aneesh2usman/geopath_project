==========================================
Point A to Point B continuous path finder
==========================================


function to find Point A to Point B continuous path finder



1. Write a python code to find the latitude and longitude coordinates that are out of line and
automatically fix the same to form a continuous path.
2. From the given terrain list with kilometeres, write a python script to generate DB of each
latitude and longitude pair with matching terrain information (NB: take the starting
latitude and longitude and 0 KM and end as )
3. Write Query to list all the points with terrain “road” in it without “civil station”

Tool Using
============
csv : import and export csv file

math : calculation distance from one point to another point

mysql-connector-python : Mysql connection and function

Install requirement.txt
=======================
	enquiries==0.1.0
	mysql_connector_repackaged==0.3.1
	python-dotenv==0.19.0
	mysql-connector-python==8.0.26

RUN Continuous Path Finder
============

#. run file python 3+ ::

    python3 geo.py


Screenshot:

.. image:: https://github.com/aneesh2usman/geopath_project/blob/master/A%20to%20Point%20B%20continuous.png

RUN Terrain Finder
==================

#. run file ````::

    python3 finding_terrain.py



Screenshot:

.. image:: https://github.com/aneesh2usman/geopath_project/blob/master/finding-terrain.png

.. image:: https://github.com/aneesh2usman/geopath_project/blob/master/finding-terrain2.png













    

