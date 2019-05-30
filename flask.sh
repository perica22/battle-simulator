#!/bin/bash
#Activate virtual enviroment
echo 'Activating virtual enviroment...'
source env/bin/activate
wait

#Remove previous db data
echo 'Removing previous database data...'
rm -f app.db && rm -rf migrations/
wait

#After the remove finishes init the db
echo 'Initializing new flask database...'
flask db init &&  flask db migrate && flask db upgrade
wait

#After the db init finishes run the server, but in the background
echo 'Starting the flask server in the background'
flask run &

echo 'Sleeping for 5 seconds to allow flask server to start'
sleep 5;

echo 'Running python init script'
python3 initial_script.py

##########################################################################################
# In order to stop server running, since it is in a bacground process,
# that process needs to be stoped explicitly by:
# searching that process: ps -fA | grep python
# and than stopping it using: kill <process_id> (process_id from previous command output)
##########################################################################################
##########################################################################################
# pylint issue with DB:
# Any class you declare as inheriting from db.Modelwon't have
# query member until the code runs so Pylint can't detect it.
# Mine soluiton for this is:
#    - runnning pylint --generate-rcfile>~/.config/pylintrc
#    - and then find the ignored-modules line,
#    - rewrite it to: ignored-modules=flask_sqlalchemy
##########################################################################################
