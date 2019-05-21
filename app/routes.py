from app import app


@app.route('/starwars/api/join')
def join():
	return "this is a join route"

@app.route('/starwars/api/attack/<int:army_id>')
def attack(army_id):
	return "this is the attack route"

@app.route('/starwars/api/leave')
def leave():
	return "this is a leave route"
