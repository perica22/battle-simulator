# battele-simulator

# HOW TO RUN:
    1. Create new empty directory - mkdir projekt
    2. Clone this repository with git clone <project_url>
    3. Change directory to battle_simulator dir by running cd battle_simulator
    4. Run bash script flask.sh by running . flask.sh command


# ADDITIONAL NOTES:
     In order to stop server running, since it is in a bacground process,
     that process needs to be stoped explicitly by:
     searching that process: ps -fA | grep python
     and than stopping it using: kill <process_id> (process_id from previous command output)

# Pylint issue with DB:
     Any class you declare as inheriting from db.Modelwon't have
     query member until the code runs so Pylint can't detect it.
     Mine soluiton for this is:
        - runnning pylint --generate-rcfile>~/.config/pylintrc
        - and then find the ignored-modules line,
        - rewrite it to: ignored-modules=flask_sqlalchemy

