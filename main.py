import random
import json
import time

from Animation import animate, puzzle

class Player:
	level_stairs = [None, "leather", "copper", "gold", "diamond", "dragon"]
	def __init__(self):
		self.gold = 0
		fill_tool = Tool(None,None,5,1)
		self.gear = {
			"helmet" : fill_tool,
			"torso" : fill_tool,
			"trousers" : fill_tool,
			"shoes" : fill_tool,
			"jewellery" : fill_tool
			}
		self.level = None
	def get_score(self):
		score = sum( list(self.gear.values()) )
		return score
	def change_gear(self, gear):
		cls = gear._class
		trash = self.gear[cls]
		self.gear[cls] = gear
		self.gold += trash.sell()
		self.ask_levelup()
	def ask_levelup(self):
		for i in self.gear.values():
			if i.material == self.level:
				return
		lvl_indx = self.level_stairs.index(self.level)
		self.level = self.level_stairs[lvl_indx + 1]
		animate(f"You reached Level {self.level}!", duration=3)
		self.ask_levelup()


class Tool:
	def __init__(self, *stats):
		self.material = stats[0]
		self._class = stats[1]
		self.score = stats[2]
		self.level = stats[3]
	def sell(self):
		return self.get_score()//2
	def get_score(self):
		return self.score // (7 - self.level)
	def __int__(self):
		return self.get_score()
	def __radd__(self, other):
		return self.get_score() + int(other)
	def __str__(self):
		return f"|{self.material}-{self._class} [{self.level}] {self.get_score()}|"


class MysteryBox:
	def __init__(self):
		with open("gear.txt", "r") as file:
			self.space = json.load(file)
	def random_gear(self, score):
		gear    = list(self.space.keys())
		weights = self.weight(list(self.space.values()), score)
		res = random.choices(gear, weights=weights)[0]
		score = self.space[res]
		level = random.choices([1,2,3,4,5], weights=[0.5, 0.25, 0.15, 0.07, 0.03])[0]
		stats = res.split("-") + [score, level]
		return Tool(*stats)
	def weight(self, weights, score):
		w_list = weights
		for nr, w in enumerate(w_list):
			w = abs(score - w)
			if w == 0:
				w = 0.5
			w_list[nr] = 1 / w
		return w_list


class Game:
	def __init__(self):
		print("Game setup")
		self.classes = ["helmet", "torso", "trousers", "shoes", "jewellery"]
		self.materials = ["leather", "diamond", "dragon"]
		self.player = Player()
		self.box = MysteryBox()
	def mainloop(self):
		start = round(time.time())
		while True:
			input("\nDraw a random tool!")
			rand_tool = self.box.random_gear(self.player.get_score())
			puzzle("You drew: "+str(rand_tool), duration=0.5)
			time.sleep(0.1)
			print("Your tool:", self.player.gear[rand_tool._class])
			eing = input("austauschen? [y/n]")
			if eing == "y":
				self.player.change_gear(rand_tool)
				print("changed! Your score:", self.player.get_score())
			else:
				gold = rand_tool.sell()
				self.player.gold += gold
				print(f"tool selled for {gold}g.")
			print("Your gold:", self.player.gold)
			if self.player.level == "dragon":
				break
		end = round(time.time())
		print("\n\nYOU WON!!!")
		print(f"You needed {end-start} seconds.")
		


app = Game()
app.mainloop()