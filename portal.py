from selenium.webdriver.common.by import By
from tools import num, world_number, argmin
import time
import config
import math
from copy import deepcopy

def go_portal(driver):
	pass

perks_info = {
	"Agility" : {
		"base_cost" : 4,
		"type" : "m",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : 20,
	},
	"Bait" : {
		"base_cost" : 4,
		"type" : "additive",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Pheromones": {
		"base_cost" : 3,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	}, 
	"Packrat" : {
		"base_cost" : 3,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Trumps": {
		"base_cost" : 3,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Motivation" : {
		"base_cost" : 2,
		"type" : "a",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Power" : {
		"base_cost" : 1,
		"type" : "a",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Toughness" : {
		"base_cost" : 1,
		"type" : "a",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Looting" : {
		"base_cost" : 1,
		"type" : "a",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Range" : {
		"base_cost" : 1,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : 10,
	},
	"Relentlessness" : {
		"base_cost" : 75,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : 10,
	},
	"Artisanistry" : {
		"base_cost" : 15,
		"type" : "m",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Carpentry" : {
		"base_cost" : 25,
		"type" : "m",
		"cost_type" : "m",
		"effect_inc" : 30,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Meditation" : {
		"base_cost" : 75,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : 7,
	},
	"Resilience" : {
		"base_cost" : 100,
		"type" : "m",
		"cost_type" : "m",
		"effect_inc" : 10,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Anticipation" : {
		"base_cost" : 1000,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : 10,
	},
	"Siphonology" : {
		"base_cost" : 10000,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : 3,
	},
	"Coordinated" : {
		"base_cost" : 150000,
		"type" : "m",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},
	"Resourceful" : {
		"base_cost" : 50000,
		"type" : "base",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : -1,
	},	
	"Overkill" : {
		"base_cost" : 1000000,
		"type" : "m",
		"cost_type" : "m",
		"effect_inc" : 5,
		"cost_inc" : 1.3,
		"max_level" : 30,
	},
	"Toughness_II" : {
		"base_cost" : 20000,
		"type" : "a",
		"cost_type" : "a",
		"effect_inc" : 1,
		"cost_inc" : 500,
		"max_level" : -1,
	},
	"Power_II" : {
		"base_cost" : 20000,
		"type" : "a",
		"cost_type" : "a",
		"effect_inc" : 1,
		"cost_inc" : 500,
		"max_level" : -1,
	},
	"Motivation_II" : {
		"base_cost" : 50000,
		"type" : "a",
		"cost_type" : "a",
		"effect_inc" : 1,
		"cost_inc" : 1000,
		"max_level" : -1,
	},
	"Carpentry_II" : {
		"base_cost" : 100000,
		"type" : "a",
		"cost_type" : "a",
		"effect_inc" : 0.25,
		"cost_inc" : 10000,
		"max_level" : -1,
	},
	"Looting_II"  : {
		"base_cost" : 100000,
		"type" : "a",
		"cost_type" : "a",
		"effect_inc" : 0.25,
		"cost_inc" : 10000,
		"max_level" : -1,
	},
}




def perk_cost(perk, lvl):

	if perks_info[perk]["cost_type"] == "m":
		return perks_info[perk]["base_cost"] * pow(1.3, lvl)
	elif perks_info[perk]["cost_type"] == "a":
		return perks_info[perk]["base_cost"] + lvl * perks_info[perk]["cost_inc"]
		#(lvl + 1) * ((spire_perks[perk][0] + (spire_perks[perk][0] + lvl * spire_perks[perk][1]))/2)
	else:
		print("Wrong cost type : ", perk)




def perk_lvl(perk, cost):
	print("Perk lvl for " + perk)
	if perks_info[perk]["cost_type"] == "m":
		print("Multiplicative cost")
		lvl = 0
		c = 0 
		while c < cost:
			c += perks_info[perk]["base_cost"] * pow(1.3, lvl)
			lvl += 1
		return lvl -1

	
	elif perks_info[perk]["cost_type"] == "a":
		print("Additive cost")
		#cost = 
		# 2 * cost = lvl * (base * 2  + lvl * inc)
		# (2 * cost) = lvl * base * 2 + lvl² * inc
		lvl = 0
		c = 0 
		while c < cost:
			c += perks_info[perk]["base_cost"] + lvl * perks_info[perk]["cost_inc"]
			lvl += 1
		return lvl -1



def get_multiplier(perks_lvl):
	final_multiplier = 1
	for p in perks_lvl:
		if perks_info[p[0]]["type"] == "a":
			final_multiplier = final_multiplier * (1 + (perks_info[p[0]]["effect_inc"] * p[1]) / 100)
		elif perks_info[p[0]]["type"] == "m":
			final_multiplier = final_multiplier * pow(1 + perks_info[p[0]]["effect_inc"]/100, p[1])
		else:
			print("No type for ", p[0])
	return final_multiplier


def compounding_perks(perks_lvl, cost):
	print("Compounding perks")
	spent = 0

	
	while spent < cost:
		m = []
		c = []
		for k in range(len(perks_lvl)):
			c.append(perk_cost(perks_lvl[k][0], perks_lvl[k][1]))
			tmp = deepcopy(perks_lvl)
			tmp[k][1] += 1
			m.append(get_multiplier(tmp))
			print("Mult ", k, " : ", m[-1], " Cost : ",c[-1] ," Ratio : ", c[-1]/m[-1])

		chosen_perk = argmin([c[k]/m[k] for k in range(len(perks_lvl))])
		spent += c[chosen_perk]
		perks_lvl[chosen_perk][1] += 1
		
	return perks_lvl

best_perk_settup = [[], 0]
def brute_force(perks_lvl, cost, index=0):
	#print("Brute force", index, cost)
	print(perks_lvl)
	if index > len(perks_lvl) - 1:
		print("Solution : ")
		multiplier = get_multiplier(perks_lvl)
		print(multiplier, "for", cost)
		print(perks_lvl)
		if multiplier > best_perk_settup[1]:
			best_perk_settup[0] = deepcopy(perks_lvl)
			best_perk_settup[1] = multiplier
			print("Best : ", best_perk_settup)

	else:
		p_cost = perk_cost(perks_lvl[index][0], perks_lvl[index][1] + 1)
		tmp = deepcopy(perks_lvl)

		while  p_cost < cost:

			perks_lvl[index][1] += 1
			tmp = deepcopy(perks_lvl)
			cost = cost - p_cost
			if index < len(perks_lvl) - 1:
				brute_force(tmp, cost, index+1)
			else:
				if perk_cost(perks_lvl[index][0], perks_lvl[index][1] + 1) > cost:
					brute_force(tmp, cost, index+1)


			p_cost = perk_cost(perks_lvl[index][0], perks_lvl[index][1] + 1)


		brute_force(tmp, cost, index + 1)






	










	


def click_perk(driver, perk, lvl):
	driver.find_element(By.ID, "ptab5Text").click()
	driver.find_element(By.ID, "customNumberBox").send_keys(lvl)
	driver.find_element(By.ID, "confirmTooltipBtn").click()
	driver.find_element(By.ID, perk).click()
	
	

def portal(driver):
	global state
	global best_perk_settup
	try:
		print("Portal")

		driver.find_element(By.ID, "portalBtn").click()
		driver.find_element(By.ID, "clearPerksBtn").click()
		
		

		perks = config.PERKS
		

		tot = 0
		for p in perks:
			tot += perks[p]

		tot_helium = num(driver.find_element(By.ID, "portalHeliumOwned").text)

		for p in perks:

			helium = tot_helium * (perks[p] / tot) 
			print("Helium reserved for " + p + " : ", helium)

			if p in config.PERK_GROUP:
				print("Group")
				perks_lvl = [ [x, 0] for x in config.PERK_GROUP[p]]
				#res = compounding_perks(perks_lvl, helium)
				best_perk_settup = [[], 0]
				brute_force(perks_lvl, helium)
				print("best_perk_settup : ", best_perk_settup)
				res = best_perk_settup[0]
				for r in res:
					click_perk(driver, r[0], r[1])
			else:
				print("Single")
				lvl = perk_lvl(p, helium)
				print(lvl)
				if perks_info[p]["max_level"] != -1:
					if lvl > perks_info[p]["max_level"]:
						lvl = perks_info[p]["max_level"]
				click_perk(driver, p, lvl)

			tot_helium = num(driver.find_element(By.ID, "portalHeliumOwned").text)
			print("Helium left : ", tot_helium)
			tot = tot - perks[p]


		print("Challenges")
		elem = driver.find_element(By.ID, "challengesHere")
		childs = elem.find_elements(By.XPATH, "./*")
		for c in childs:
			print("challenge", c.get_attribute("id"))
			#if c.get_attribute("id") == "challengeCrushed":
			if c.get_attribute("id") == "challenge" + config.current_challenge:
				#if c.get_attribute("id") != "challenge0" and not "nextChallenge" in c.get_attribute("class") and not "finishedChallenge" in c.get_attribute("class"):
				
				c.click()
				break

		
		time.sleep(30)
		driver.find_element(By.ID, "activatePortalBtn").click()
		driver.find_element(By.XPATH, "//div[@id='tipCost']/div[1]").click()
		state = {
		 	"food" : 0,
		 	"wood" : 0,
		 	"stage" : 0,
		 	"gathering" : "none",
		 	"build" : "none",
		 	'current_map_done' : 0,
		 	"trimpsMax" : 0,
		 	"trimpsOwned" : 0,
		 	"trimpTrapText" : 0,

		 }
	except Exception as e :
		print("Portal", e)
		pass