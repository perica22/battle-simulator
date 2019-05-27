"""
Export file
****************************************************************
	Any class you declare as inheriting from db.Modelwon't have
	query member until the code runs so Pylint can't detect it.
	Mine soluiton for this is:
		- runnning pylint --generate-rcfile>~/.config/pylintrc
		- and then find the ignored-modules line,
		- rewrite it to: ignored-modules=flask_sqlalchemy
****************************************************************
"""
from app import APP
