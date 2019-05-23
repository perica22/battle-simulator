

class AttackService():

	def __int__(self, attack_army, defense_army):
		self.attack_army = attack_army
		self.defense_army = defense_army # try to cast it to dict using __dict__ or something else

	def attack(self):
		attack_chance = calculate_attack_chance(attack_army['number_squads'])

