from selenium.webdriver.common.by import By
from tools import in_world
from selenium.webdriver.common.action_chains import ActionChains
from tools import num, in_map_selection, world_number, current_cell, fight_stats, get_elem
from selenium.webdriver.support import expected_conditions as EC
import config
from selenium.webdriver.support.ui import WebDriverWait
special_maps = {
	#"The Wall" : 15, 
	#"The Block" : 14, 
	#"Dimension of Anger" : 21,
	#"Trimple Of Doom" : 38,
	"The Prison" : 80,
	#"Bionic Wonderland" : 125,
	"Imploding Star" : 10000

}

map_runs = {
	8 : 1,
	10 : 1
}


def farming_maps(driver, state):
	if in_world(driver):
		if current_cell(driver) > 80:
			try:

				if "(+4)" in get_elem(driver,"CoordinationOwned").text:
					print("Farming maps")
					get_elem(driver, "mapsBtnText").click()
					if "Abandon" in get_elem(driver, "mapsBtnText").text:
							get_elem(driver, "mapsBtnText").click()
					try:
						get_elem(driver, "recycleMapBtn").click()
					except Exception as e:
						pass
					old_maps_id = [x.get_attribute("id") for x in driver.find_elements(By.XPATH, "//div[@id='mapsHere']/*")]
					create_map(driver, state, 3, "fast")
					maps_id = [x.get_attribute("id") for x in driver.find_elements(By.XPATH, "//div[@id='mapsHere']/*")]
					for m in maps_id:
						if m not in old_maps_id:
							get_elem(driver, m).click()
					get_elem(driver, "selectMapBtn").click()
			except Exception as e:
				pass

def maps(driver, state):
	world_num = world_number(driver)
	if world_num > 5 :
		#"cellColorCurrent" in get_elem(driver, "mapCell0").get_attribute("class") and
		if in_world(driver):
			#print("Maps")
			cs = current_cell(driver)
			if world_num >= config.CHALLENGES[config.current_challenge]["void_maps_at"] and cs >30:
				pass
				
				void_maps(driver)
			else:
				fs = fight_stats(driver)[0]
				if (not "%" in get_elem(driver, "mapBonus").text and world_num > 10) or (not "10" in get_elem(driver, "mapBonus").text and fs > 20):
					#print(fs, world_num % 2 == 0)
					if fs > 5:
						mod = "fast"
						lvl = 0
						cursors = ["difficulty", "loot"]
					elif world_num % 10 == 0 or get_elem(driver, "worldName").text == "Spire":
						if fs < 0.5:
							cursors = ["size"]
						else:
							cursors = ["size", "difficulty"]
						mod = "prestige"
						lvl = 0
					elif world_num == 165 and config.current_challenge == "Toxicity":
						cursors = ["difficulty", "loot"]
						mod = "fast"
						lvl = 0
					else:
						return
					# Going to maps
					get_elem(driver, "mapsBtnText").click()
					if "Abandon" in get_elem(driver, "mapsBtnText").text:
							get_elem(driver, "mapsBtnText").click()

					try:
						get_elem(driver, "recycleMapBtn").click()
					except Exception as e:
						pass

					# Old maps
					old_maps_id = [x.get_attribute("id") for x in driver.find_elements(By.XPATH, "//div[@id='mapsHere']/*")]

					special_map = False
					for m in old_maps_id:
						elem = get_elem(driver, m)
						special_map_name = elem.find_element(By.XPATH, "./div[2]").text
						
						if special_map_name in special_maps and not "noRecycleDone" in elem.get_attribute("class"):
							if world_num >= special_maps[special_map_name]:
								print("Go", special_map_name)
								elem.click()
								special_map = True

					

					if special_map:
						get_elem(driver, "selectMapBtn").click()
					else:

						create_map(driver, state, lvl, mod, cursors)

						maps_id = [x.get_attribute("id") for x in driver.find_elements(By.XPATH, "//div[@id='mapsHere']/*")]							
						for m in maps_id:
							if m not in old_maps_id:
								get_elem(driver, m).click()

						get_elem(driver, "selectMapBtn").click()


def map_cursors(driver, state, cursors_valid):
	# Cursors
	cursors = ["difficulty", "size", "loot"]
	print("Creating map")
	for c in cursors:
		if c in cursors_valid:
			difficulty = get_elem(driver, c + "AdvMapsRange")
			act = ActionChains(driver)
			width = difficulty.size['width']
			offsets = [-(width/2) + width/10 * x for x in range(0,11)[::-1]]
			last_offset = offsets[0]
			very_last_offset = offsets[0]
			for o in offsets:
				act.move_to_element(difficulty).move_by_offset(o, 0).click().perform()
				if  state["fragmentsOwned"] > num(driver.find_element(By.ID, "mapCostFragmentCost").text):
					break


def map_level(driver, lvl):
	# Level
	if lvl != 0:
		down_button = get_elem(driver, "mapLevelContainer")	
		childs = down_button.find_elements(By.XPATH, "./*")
		down_button = childs[0]
		for p in range(lvl):
			down_button.click()

def map_biome(driver, state):
	# Biome
	biome_select = get_elem(driver, "biomeAdvMapsSelect")
	biome_select.click()
	get_elem(driver, "gardenOption").click()
	if  state["fragmentsOwned"] < num(driver.find_element(By.ID, "mapCostFragmentCost").text):
		biome_select.click()
		biome_select.find_element(By.XPATH, "./option").click()

def map_modifiers(driver, mod, state):
	# Modifiers
	modifiers = get_elem(driver, "advSpecialSelect")	
	childs = modifiers.find_elements(By.XPATH, "./*")
	no_mod = None
	fast_mod = None
	prestigious_mod = None
	for c in childs:
		if c.text == "No Modifier":
			no_mod = c
		if c.text == "Prestigious":
			prestigious_mod = c
			
		if c.text == "Fast Attacks":
			fast_mod = c


	modifiers.click()
	if mod == "fast":
		fast_mod.click()
	if mod == "prestige":
		prestigious_mod.click()
	if  state["fragmentsOwned"] < num(driver.find_element(By.ID, "mapCostFragmentCost").text):
		modifiers.click()
		no_mod.click()
	get_elem(driver, "mapCreateBtn").click()

def create_map(driver, state, lvl, mod, cursors):

	
	map_level(driver, lvl)

	

	map_cursors(driver, state, cursors)
	map_modifiers(driver, mod, state)


	map_biome(driver, state)

	

	


def exit_map(driver, state):
	try:
		if not in_world(driver):
			if not "Abandon" in get_elem(driver, "mapsBtnText").text:
				worldName = get_elem(driver, "worldName").text
				if worldName in special_maps:
					cell_num = current_cell(driver)
					print(state['current_map_done'])
					print("Let me out", cell_num)
					if cell_num < 20:
						if state['current_map_done'] > 0 :
							print("Im Leaving")
							leave_map(driver)
							state['current_map_done'] = 0
					else:
						state['current_map_done'] = 1 + state['current_map_done']
				elem = get_elem(driver, "mapsBtnText").text
				world_num = world_number(driver)

				void = is_a_void_map(worldName)
				farm_map = False
				giga = len(driver.find_elements(By.XPATH, "//div[@id='mapGrid']/ul/li/span[@class='glyphicon glyphicon-book']"))
				if giga == 0:
					print("FS : ", fight_stats(driver)[0])
					if config.current_challenge == "Corrupted":
						leave = fight_stats(driver)[0] < 0.3 or '10' in elem
					elif config.current_challenge == "Domination":


						leave = fight_stats(driver)[0] < 0.0001
					else:
						leave = fight_stats(driver)[0] <1
					print(leave)
					# Toxicity
					if config.current_challenge == "Toxicity":
						if world_num == 165 and num(get_elem(driver, "toxicityStacks").text) < 1400:
							leave = False

					if leave:
						leave_map(driver)


	except Exception as e:
		print(e)
		pass

			


def leave_map(driver):
	try:

		get_elem(driver, "mapsBtnText").click()

	except Exception as e:
		print("leave", e)



def is_a_void_map(worldName):	
	prefix = [
		"Deadly",
		"Heinous",
		"Destructive",
		"Deadly",
		"Poisonous"
	]
	return worldName.split(" ")[0] in prefix



def leaving_map_selection(driver):
	if in_map_selection(driver):
		get_elem(driver, "mapsBtnText").click()
		try:
			get_elem(driver,  "fightBtn").click()
		except Exception as e:
			print("leaving_map_selection", e)




def leaving_void_map_selection(driver):
	if "display: block" in get_elem(driver, "heirRare").get_attribute("style"):
		maps = driver.find_elements(By.XPATH, "//div[@id='voidMapsHere']/*")
		for m in maps:
			m.click()
		get_elem(driver, "selectMapBtn").click()
		print("Let's go")


def void_maps(driver):


	
	try:
		
		if num(get_elem(driver, "voidAlert").text) > 0:
			print("Void")
			get_elem(driver, "mapsBtnText").click()
			if "Abandon" in get_elem(driver, "mapsBtnText").text:
					get_elem(driver, "mapsBtnText").click()

			get_elem(driver, "voidMapsBtn").click()

			maps = driver.find_elements(By.XPATH, "//div[@id='voidMapsHere']/*")
			for m in maps:
				m.click()
			get_elem(driver, "selectMapBtn").click()
			print("Let's go")
	except Exception as e :
		#print("Void", e)
		pass