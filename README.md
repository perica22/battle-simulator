# battele-simulator

## HOW TO RUN:
    1. Create new empty directory - mkdir projekt
    2. Clone this repository with git clone <project_url>
    3. Change directory to battle_simulator dir by running cd battle_simulator
    4. Run bash script flask.sh by running . flask.sh command


## ADDITIONAL NOTES:
     In order to stop server running, since it is in a bacground process,
     that process needs to be stoped explicitly by:
     searching that process: ps -fA | grep python
     and than stopping it using: kill <process_id> (process_id from previous command output)

## Pylint issue with DB:
     Any class you declare as inheriting from db.Modelwon't have
     query member until the code runs so Pylint can't detect it.
     Mine soluiton for this is:
        - runnning pylint --generate-rcfile>~/.config/pylintrc
        - and then find the ignored-modules line,
        - rewrite it to: ignored-modules=flask_sqlalchemy

# TASK DESCRIPTION:

The goal of this task is to build a Battle simulation app between 5 and n armies. The system is built with the main server app, whose purpose is to connect other armies and allow them to attack each other. 

We can imagine this as a server app and clients app. Clients(Armies) communicate with the Server by using the REST API and JSON. The server communicates with the Clients by sending them a Webhook with JSON data.

The Server is the main source of the truth for the app. The server needs to log all data and behaviours in the database (MySQL/Postgres)

IMPORTANT: THERE IS NO UI. The client is just another python app contacting the Server app.

You should have an automated system, which will run Server and at least 5 clients. The clients can join each with a delay. 

### Start

The Server app is always available and any client can connect to it. The client connects to the server by using the join API. The server will provide a client with an accessToken upon join which will be used to allow Client the access to the Server.

On joining, the client is obligated to provide the Server with
    - Name
    - Number of squads (min 10 max 100)
    - Webhook URL

Upon a successful join, a record for that army will be stored in the database.
To start the battle there must be at least one more Army alive and registered in the server app.

Whenever a client joins, the server will trigger army.join webhook. All joined clients will receive a webhook event with the event type army.join 
In the body of the request, there will be the ID of the army, the number of their squads.

After at least two armies have joined, the clients can initiate attacks.

### Client (Armies)
The purpose of the client is to decide who to attack and speed of the attack. Based on webhooks he will know which army is available and if it can be attacked.


#### Strategy
The client will choose an army to attack based on its initial setting. Value of this setting can be
    - Weakest (lowest number of squads)
    - Strongest (highest number of squads)
    - Random

Based on the strategy, the client will decide which army to attack from the pool of the armies.
Clients cannot change strategy once the battle starts.

NOTE: Client must wait for API call to finish before triggering a new API call.

### Server (Manager)
The server will do all of the battle logic. The server will store all the data in the database. Also, it will validate all of the data and make sure that everything goes as it should.

NOTE: The architecture of the server and the structure of the database are not defined. You can define it as you see it fit.

When a client calls attack API, multiple factors need to be calculated.

#### Attack chances
Not every attack is successful. The chance of a successful attack is the 1 in the number of squads. If an army has 100 squads, they have a chance of 1% to do successful damage.

#### Repeat attack
The army will attack until it does have a successful attack. If for example, the army has 100 squads, it can do a 100 attacks until one succeeded. If none succeed, no damage will be applied to the attacked army


#### Attack damage
The army does damage equal to the number of squads it has. If for example, the army has 100 squads it will do 100 damage.
Also, the maximum damage an attack can do is calculated by dividing the number of squads with the number of repeats. If for example, an army of 100 squads hits after the second attack, the damage it can deal is 50, but if it hits after 10th repeat, the damage it can deal is 10 (Squads/Repeats)

#### Received damage
Each squad has 1 health. There is also a %  (chance) to receive half of the damage. This chance increases from 0 up to 99% based on a number of squads in the army who will receive the damage. If the army has 100 squads, a chance to receive half damage is 0%, but if the army has 1 unit, the chance to receive half damage is 99%

#### Reload time
Reload time takes 1 second per 10 squads. Completing attack, the server will wait before responding with a successful STATUS 200 to the client’s API request.
NOTE: If a client has 14 squads, do a floor and use 10 for reload time mathematic.

The army is dead when all squads are dead. 

### Server API Routes

    POST {serverURL}/api/join (optional ?accessToken={accessToken})
    API route to register client/army

    PUT {serverURL}/api/attack/{armyId}?accessToken={accessToken}
    API post to attack an army
    200 for a successful response and 404 for not found or dead army.

    PUT {serverURL}/api/leave?accessToken={accessToken}
    API route to leave the battle. To join back, and not register a new army, use join with the accessToken

### Server Webhooks

#### army.join
Sent when an army joins the battle. This event is sent to all alive and registered clients.
Data
    - armyId (id of the joined army)
    - squadsCount (number of squads army have)
    - Type of join (new or returned)

#### army.leave
Sent when an army activates stop function, leave the game or die. This event is sent to all alive and registered clients.
Data
    - armyId
    - Type of leave

#### army.update
Sent every time an army is updated by being attacked or by successfully attacking.
Data
    - armyId id of the army who was attacked or completed a successful attacking.
    - squadsCount
    - rankRate
NOTE: This event is sent to the client who received damage and based on armyId he should know it was him who received damage.

#### Additional notes
If the server doesn’t receive the 200 response on a sent webhook, given army will be removed from active armies and army.leave webhook will be triggered.

### Sum up
The server is a source of all truths. 
All actions are happening asynchronously. There are no blocking events.
Client’s purpose is only to receive webhooks and to decide who to attack
All data must be stored in the database.
##### THERE IS NO UI FOR THIS TASK

