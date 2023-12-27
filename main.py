from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, math
import config

from portal import portal
from tools import num, argmin, in_world, in_map_selection, world_number, get_elem, reset_state, fight_stats
from maps import maps, exit_map, leaving_map_selection, leaving_void_map_selection, farming_maps
from saves import import_save, export
import threading

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return

showcounter = 0

def my_callback(inp):
	global showcounter
	showcounter += 1
	if showcounter % 2 == 0:
		print("=" * 10, " Resuming ", "=" * 10)
	else:
		print("=" * 10," Paused ","=" * 10)

driver = webdriver.Firefox()
driver.get("https://trimps.github.io/")

state = {
 	"food" : 0,
 	"wood" : 0,
 	"stage" : 0,
 	"gathering" : "none",
 	"build" : "none",
 	'current_map_done' : 0 ,
 	"heliumPh" : 0,
 	"maxHeliumPh" : 0,
 	"lastHeliumPh" : 0,
 }


def main():
	kthread = KeyboardThread(my_callback)
	driver.find_element(By.XPATH, "//div[@id='tipCost']/div[1]/div[2]").click()
	import_save(driver)

	start_time = time.time()
	while(True):
		try:
			if time.time() - start_time > 60 * 3:
				start_time = time.time()
				export(driver)
				print("=" * 30 , "  Saved  ", "=" * 30)

			if showcounter % 2 == 0:

				reset_state()
				#update_states()
				#leaving_map_selection(driver)

				armor()

				geneticit_assist()

				#gather(upgrades_to_do)

				fight()
				#build()

				formation(driver)


				#exit_map(driver, state)
				#leaving_void_map_selection(driver)

				#maps(driver, state)

				if world_number(driver) >= config.CHALLENGES[config.current_challenge]["portal_at"] :
					if in_world(driver):
						check_heirlooms()
						spend_magmite()
						portal(driver)
					pass
				nurseries()
			else: 
				time.sleep(5)

			
			
			

		except Exception as e:
			print("Main loop", e)
		

def check_geneticist():
	try:
		gen = get_elem(driver,  "Geneticist")
		if num(get_elem(driver,  "trimpsTimeToFill").text.split(" ")[-2]) > config.CHALLENGES[config.current_challenge]["geneticist_target"] + 1:

			get_elem(driver,  "fireBtn").click()
			while num(get_elem(driver,  "trimpsTimeToFill").text.split(" ")[-2]) > config.CHALLENGES[config.current_challenge]["geneticist_target"] + 1:
				gen.click()
			get_elem(driver,  "fireBtn").click()
	except Exception as e:
		#print(e)
		pass

def geneticit_assist():

	if world_number(driver) > 80 and world_number(driver) < 201:
		while not "30" in driver.find_element(By.ID,"GeneticistassistSetting").text:
			driver.find_element(By.ID, "GeneticistassistSetting").click()
	if world_number(driver) > 200:
		while not "3 " in driver.find_element(By.ID,"GeneticistassistSetting").text:
			driver.find_element(By.ID, "GeneticistassistSetting").click()


def spend_magmite():
	print("Spending Magmite")
	get_elem(driver, "upgradeMagmiteTotal").click()

	bought = True
	magmite_upgrades = [
		"generatorUpgradeCapacity",
		"generatorUpgradeSupply",
		"generatorUpgradeEfficiency",
		"generatorUpgradeOverclocker",
	]

	while bought:
		bought = False

		for u in magmite_upgrades:
			e = driver.find_element(By.ID, u)
			if "thingColorCanAfford" in e.get_attribute("class"):
				bought = True
				print("Bought " + u)
				e.click()
				driver.find_element(By.ID, "magmiteCost").click()
	webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def check_heirlooms():
	print("Checking Heirlooms")
	rarity = "heirloomRare7"
	get_elem(driver, "heirloomsBtn").click()

	heirlooms = driver.find_elements(By.XPATH, "//div[@id='extraHeirloomsHere']/*")
	for h in heirlooms:
		if rarity in h.get_attribute("class"):
			h.click()
			driver.find_element(By.ID, "carryHeirloomBtn").click()
			print("Saved Heirloom")
			break

	webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def geneticist():
	try:

		# alive time  ===  respawn time

		life = float(get_elem(driver,  "goodGuyBar").get_attribute("style").split("%;")[0].split(" ")[1])

		if life > 0:
			if life > 50 + config.current_life:
				config.alive_time = time.time() - config.alive_start
				config.alive_start = time.time()

				config.alive_array.append(config.alive_time)
				if len(config.alive_array) > 5:
					config.alive_array.pop(0)
				mean = sum(config.alive_array) / len(config.alive_array)
				print("Respawn time : ", config.alive_time, "Mean : ", mean)
			config.dead_start = 0

		else:
			if config.dead_start == 0:
				config.dead_start = time.time()
			config.dead_time = time.time() - config.dead_start
			print("Dead time : ", config.dead_time)

		if config.dead_time > 1:
			print("Firing geneticist")
			get_elem(driver, "tab2Text").click()
			get_elem(driver, "fireBtn").click()
			get_elem(driver, "Geneticist").click()
			get_elem(driver, "fireBtn").click()
			get_elem(driver, "tab1Text").click()

		elif num(get_elem(driver, "trimpsTimeToFill").text.split(" ")[-2]) < mean - config.dead_time:

			get_elem(driver, "tab2Text").click()
			gen = get_elem(driver, "Geneticist")

			if "thingColorCanAfford" in gen.get_attribute("class"):
				print("Firing Farmer and hiring geneticist")
				get_elem(driver, "fireBtn").click()
				get_elem(driver, "Farmer").click()
				get_elem(driver, "fireBtn").click()
				gen.click()


			get_elem(driver, "tab1Text").click()


		config.current_life = life

		return



		if config.gen_start == 0:
			config.gen_start = time.time()

		info = get_elem(driver, "trimpsTimeToFill").text

		breeding_time = 0
		if "/" in info:
			breeding_time = num(info.split("/")[0].split(" ")[0])
			max_breeding_time = num(info.split("/")[1].split(" ")[0])
		else:
			max_breeding_time = num(info.split(" ")[0])

		if breeding_time  == 0:
			config.gen_time = time.time() - config.gen_start
		else:
			config.gen_start = time.time()
			config.gen_time = 0

		if config.gen_time > max_breeding_time and config.gen_time < config.max_gen_time:

			get_elem(driver, "tab2Text").click()
			gen = get_elem(driver, "Geneticist")

			if "thingColorCanAfford" in gen.get_attribute("class"):
				print("Firing Farmer")
				get_elem(driver, "fireBtn").click()
				get_elem(driver, "Farmer").click()
				get_elem(driver, "fireBtn").click()
				gen.click()

			get_elem(driver, "tab1Text").click()

		elif config.gen_time == 0:
			pass







			while num(get_elem(driver, "trimpsTimeToFill").text.split(" ")[-2]) > \
					config.CHALLENGES[config.current_challenge]["geneticist_target"] + 1:
				gen.click()
			get_elem(driver, "fireBtn").click()



			gen = get_elem(driver, "Geneticist")


		if float(get_elem(driver, "trimpsBar").get_attribute("style").split("%;")[0].split(" ")[1]) < 100:
			print("breeding")
			num(get_elem(driver, "trimpsTimeToFill").text.split(" ")[-2])
		gen = get_elem(driver, "Geneticist")

		num(get_elem(driver, "trimpsTimeToFill").text.split(" ")[-2])



	except Exception as e:
		print("Geneticist", e)


def armor():
	try:
		equipments = driver.find_elements(By.XPATH, "//div[@id='equipmentHere']/*")

		for e in equipments:
			name = e.get_attribute("id")
			classes = e.get_attribute("class")
			
			if "thingColorCanAfford" in e.get_attribute("class"):
				if int(get_elem(driver,  name + "Owned").text) < 11:
					if "efficientYes" in classes:
						e.click()
					elif name == "Shield":
						e.click()
	except Exception as e:
		print("Armor", e )




def update_states():
	variables = [
		"fragmentsOwned",
		"trimpsUnemployed",
		"trimpsMax",
		"trimpsOwned",
		"jobsTitleUnemployed",
		"FarmerOwned",
		"MinerOwned",
		"TrainerOwned",
		"ScientistOwned",
		"LumberjackOwned",
		"GeneticistOwned",
		"MagmamancerOwned",
		"gemsOwned",
		"ExplorerOwned",
		"trimpTrapText",
		"foodOwned",
		"woodOwned",
		"metalOwned",
		"scienceOwned",
		"trimpsEmployed",
		"maxEmployed"
	]



	
	state["lastHeliumPh"] = state["heliumPh"]
	hpr = get_elem(driver,  "heliumPh").text
	if hpr != "":
		state["heliumPh"] = num(hpr.replace("/hr",""))
	try:
		if state["heliumPh"] > state["lastHeliumPh"]:
			print("Gained helium")
			if state["heliumPh"] < state["maxHeliumPh"] and False:
				print("Progress has slow down, (best : ",state["maxHeliumPh"], " current : ",state["heliumPh"],") attempting to portal")
				portal(driver)
			else:
				print("New max helium/h : ", state["heliumPh"])
				state["maxHeliumPh"] = state["heliumPh"]
	except Exception as e:
		pass


	for v in variables:
		update_state(v)

	try:
		if len(driver.find_elements(By.XPATH, "//div[@id='queueItemsHere']/*")) > 0:
			state["build"] = "up"
		else:
			state["build"] = "none"
	except:
		state["build"] = "none"

	try:
		state["available_jobs"] = [x for x in driver.find_elements(By.XPATH, "//div[@id='jobsHere']/*")]
	except Exception as e:
		print("Jobs", e)
		pass
	try:
		if world_number(driver) > 69:
			state["available_jobs"].append(get_elem(driver,  "Geneticist"))
	except Exception as e:
		print("Jobs gen", e)
		pass



def update_state(name):
	try:
		elem = get_elem(driver,  name).text.split(" ")[0]
		if elem != "":
			state[name] = num(elem)
		else:
			state[name] = 0
	except Exception as e:
		state[name] = 0

	
def fight():
	if world_number(driver) < 8:
		try:
			get_elem(driver,  "fightBtn").click()
		except Exception as e:
			print("Fight", e)

def upgrades():
	not_to_buy = [
		"Shieldblock",
		"Trapstorm",
	]
	tried = False
	try:
		upgrades = driver.find_elements(By.XPATH, "//div[@id='upgradesHere']/*")
		for u in upgrades:
			classes = u.get_attribute("class")
			name = u.get_attribute("id")
			elem = u

			if (name == "Battle" and state["trimpsOwned"] == state["trimpsMax"]) or (not name in not_to_buy) :
				if name not in armor_upgrades and name != "Coordination" and name != "Gigastation":
					tried = True

				if "thingColorGoldenUpgrade" in classes:
					if elem.get_attribute("id") == "HeliumGolden":
						elem.click()
						print("Bought " + name)

				if name == "Gigastation":
					base, inc = config.CHALLENGES[config.current_challenge]["gigastation_preset"]
					wait = WebDriverWait(driver, 10)
					giga = wait.until(EC.element_to_be_clickable((By.ID, "GigastationOwned")))

					if num(get_elem(driver,  "WarpstationOwned").text) > base + inc * num(giga.text.split("(")[0]):
						wait = WebDriverWait(driver, 10)
						giga = wait.until(EC.element_to_be_clickable((By.ID, "GigastationOwned")))
						giga.click()
						get_elem(driver,  "confirmTooltipBtn").click()
						print("Gigastation target :", base + inc * num(get_elem(driver,  "GigastationOwned").text.split("(")[0]))

						print("Bought " + name)

				elif "thingColorCanAfford" in classes:
									
					elem.click()
					print("Bought " + name)



				if name == "Shieldblock":
					get_elem(driver,  "confirmTooltipBtn").click()

	except Exception as e:
		print("upgrades", e)
		return False
	return tried


def housing_cost(building):
	
	if not building in housing:
		print(building, "not housing")
		return 0
	elif building == "Warpstation":
		gigastations = 0
		lvl = num(get_elem(driver,  building + "Owned").text)
		try:
			gigastations = num(get_elem(driver,  "GigastationOwned").text.split("(")[0])
		except Exception as e:
			#print("Error giga", e)
			pass
		tot = sum(housing[building]["Initial_Cost"]) * (pow(1.75,gigastations)  * pow(1.4, lvl) / (housing[building]["Trimps"] *pow(1.2,gigastations)))
		return tot
	else:
		lvl = num(get_elem(driver,  building + "Owned").text)
		increase = pow(housing[building]["Increase"], lvl) 
		tot = sum(housing[building]["Initial_Cost"]) * increase / housing[building]["Trimps"]
		


		


		return tot


def build_housing():
	get_elem(driver,  "tab6").click()
	bought = True
	#while bought:
	bought = False
	cheapest = housing_cost("Hut")
	cheapest_housing = "Hut"
	for h in housing:
		try:

			if h == "Gateway":
				if housing[h]["Initial_Cost"][4] * pow(housing[h]["Increase"], num(get_elem(driver,  h + "Owned").text)) < 0.2 * state["fragmentsOwned"]:
					cost = housing_cost(h)
					#print(h, cost)
					if cost < cheapest:
						cheapest = cost
						cheapest_housing = h


			else:
				cost = housing_cost(h)
				#print(h, cost)
				if cost < cheapest:
					cheapest = cost
					cheapest_housing = h
		except Exception as e:
			pass


	#print("Chepest housing", cheapest_housing)
	elem = get_elem(driver,  cheapest_housing)
	classes = elem.get_attribute("class")
	if "thingColorCanAfford" in classes:
		bought = True
		print("Buying " + cheapest_housing)
		elem.click()
	get_elem(driver,  "tab1").click()


def build():
	not_to_buy = [
		"Shed",
		"Barn",
		"Forge",
	]
	bulk_buy = [ "Tribute"]
	try:
		#print(state["upgrades"])
		#if "Gymystic" not in state["upgrades"]:
		#print("Resume building")
		buildings = driver.find_elements(By.XPATH, "//div[@id='buildingsHere']/*")

		for b in buildings:


			classes = b.get_attribute("class")
			name = b.get_attribute("id")

			
			if name not in housing and name not in not_to_buy:

				if "thingColorCanAfford" in classes:
					if name in bulk_buy:
						driver.find_element(By.ID , "tab6").click()
					if name == "Trap":
						if not is_breeding():
							b.click()
					elif name == "Wormhole":
						if num(get_elem(driver,  "WormholeOwned").text) < 20:
							b.click()
							get_elem(driver,  "confirmTooltipBtn").click()
					elif name == "Nursery":
						#print("Hit taken : ", fight_stats(driver)[1])
						if fight_stats(driver)[1] < 2:

							if 400000 * pow(1.06, num(get_elem(driver,  "NurseryOwned").text)) < 0.2 * state["gemsOwned"]:
								print("Buying Nursery")
								driver.find_element(By.ID, "tab4").click()
								b.click()
					
					else:
						b.click()
					driver.find_element(By.ID , "tab1").click()
		build_housing()


			
	except Exception as e:
		print("Build", e)


def is_breeding():
	try:
		if num(get_elem(driver,  "trimpsPs").text.split("/")[0]) > 0:
			return True
		return False
	except Exception as e :
		print("Breeding", e)
		return False

def nurseries():
	if fight_stats(driver)[1] < 2:
		n = get_elem(driver, "NurseryOwned")
		print("Buying Nursery")
		driver.find_element(By.ID, "tab4").click()
		n.click()
		driver.find_element(By.ID, "tab1").click()


def formation(driver):
	world_num = world_number(driver)
	if world_num > 71:
		try:
			if world_num > config.SCRYING_FORMATION:
				if in_world(driver):
					msg = driver.find_elements(By.CLASS_NAME, "essenceMessage")
					for m in msg:
						if "There are 0 Essence drops left in the current Zone." in m.text:
							get_elem(driver, "formation2").click()
						else:
							get_elem(driver,  "formation4").click()
					if len(msg) == 0:
						get_elem(driver,  "formation4").click()
				else:
					get_elem(driver,  "formation2").click()
			else:
				get_elem(driver,  "formation2").click()
		except Exception:
			pass

def gather(upgrades_to_do):
	try:
		if state["trimpTrapText"] > 0 and (state["trimpsOwned"] < state["trimpsMax"] or state["trimpsMax"] == 0) and False:
			get_elem(driver,  "trimpsCollectBtn").click() # Traps
		elif state["build"] == "up" :
			pass

			#get_elem(driver,  "buildingsCollectBtn").click() #Build
		else:
			ressourcesName = ["food", "wood", "metal", "science"]
			ressources = []
			for rn in ressourcesName:
				try:
					elem = driver.find_element(By.XPATH, "//div[@id='" + rn + "']")
					if "hidden" not in elem.get_attribute("style"):
						if rn == "science":
							if "none" in get_elem(driver,  "turkimpBuff").get_attribute("style") or upgrades_to_do:
								ressources.append(rn +"Owned")
						else:
							ressources.append(rn +"Owned")
				except Exception as e:
					pass

			r = argmin([state[x] for x in ressources])
			get_elem(driver,  ressources[r].split("Owned")[0] + "CollectBtn").click()
	except Exception as e:
		print("Gather", e)


def hire():
	try:
		if state["trimpsOwned"] == state["trimpsMax"] and state["jobsTitleUnemployed"] > 0:
			fixed_jobs = []
			fixed_job_names = []
			for j in state["available_jobs"]:
				classes = j.get_attribute("class")
				name = j.get_attribute("id")
				if "thingColorCanAfford" in classes:
					if name == "Scientist":
						fixed_jobs.append(math.ceil(int(state[name+"Owned"])*20)) 							
						fixed_job_names.append(j)
					elif name == "Trainer":
						owned = int(state[name+"Owned"])
						price = 750 * pow(1.1, owned)
						if price < 0.1 * state["foodOwned"]:
							fixed_jobs.append(math.ceil(owned*2))
							fixed_job_names.append(j)
					elif name == "Explorer":
						owned = int(state[name+"Owned"])
						price = 15000 * pow(1.1, owned)
						if price < 0.2 * state["foodOwned"]:
							fixed_jobs.append(math.ceil(owned*4))
							fixed_job_names.append(j)
					elif name == "Geneticist":
						if num(get_elem(driver,  "trimpsTimeToFill").text.split(" ")[-2]) < config.CHALLENGES[config.current_challenge]["geneticist_target"]:
							j.click()
							return
					else:
						fixed_jobs.append(int(state[name+"Owned"]))	
						fixed_job_names.append(j)
					state[name+"Owned"] += 1
			new_job = argmin(fixed_jobs)
			driver.find_element(By.ID , "tab6").click()
			fixed_job_names[new_job].click()
			driver.find_element(By.ID , "tab1").click()
	except Exception as e:
		print("Hire", e)


armor_upgrades = {
 	"Supershield",
 	"Dagadder",
 	"Bootboost",
 	"Megamace",
 	"Hellishmet",
 	"Polierarm",
 	"Pantastic",
 	"Axeidic",
 	"Smoldershoulder",
 	"Greatersword",
 	"Bestplate",
 	"Harmbalest",
 	"GambesOP"
}

housing = {
		"Hut" : {
			"Trimps" : 6,
			"Increase" : 1.24,
			"Initial_Cost" : [125, 75, 0, 0, 0]

		},
		"House" : {
			"Trimps" : 10,
			"Increase" : 1.22,
			"Initial_Cost" : [1500, 750, 150, 0, 0]

		}, 
		"Mansion" : {
			"Trimps" : 20,
			"Increase" : 1.2,
			"Initial_Cost" : [3000, 2000, 500, 100, 0]

		},
		"Hotel" : {
			"Trimps" : 40,
			"Increase" : 1.18,
			"Initial_Cost" : [10000, 12000, 5000, 2000, 0]

		},
		"Resort" : {
			"Trimps" : 80,
			"Increase" : 1.16,
			"Initial_Cost" : [100000, 120000, 50000, 20000, 0]

		},
		"Gateway" : {
			"Trimps" : 100,
			"Increase" : 1.14,
			"Initial_Cost" : [0, 0, 75000, 20000, 3000]

		},
		"Collector" : {
			"Trimps" : 5000,
			"Increase" : 1.12,
			"Initial_Cost" : [0, 0, 0, 500000000000, 0]

		},
		"Warpstation" : {
			"Trimps" : 50000,
			"Increase" : 1.4,
			"Initial_Cost" : [0, 0, 1000000000000000,  1e14, 0]

		},

	}

main()