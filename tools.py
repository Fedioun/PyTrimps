from selenium.webdriver.common.by import By

state = {}

def get_elem(driver, elem_id):
	if elem_id in state:
		return state[elem_id]
	else:
		state[elem_id] = driver.find_element(By.ID, elem_id)
		return state[elem_id]

def reset_state():
	global state
	state = {}

def fight_stats(driver):
	stats = {
		"goodGuyAttack" : 0,
		"goodGuyHealthMax" : 0,
		"goodGuyBlock" : 0,
		"badGuyAttack" : 0,
		"badGuyHealthMax" : 0,
	}

	for s in stats :
		stats[s] = num(driver.find_element(By.ID, s).text.split("-")[0])
	
	full_block = stats["goodGuyBlock"] > stats["badGuyAttack"] * 1.5
	one_shot = stats["goodGuyAttack"] > stats["badGuyHealthMax"]
	got_one_shot =  stats["badGuyAttack"] > stats["goodGuyHealthMax"] + stats["goodGuyBlock"]

	number_of_hits =  stats["badGuyHealthMax"] / stats["goodGuyAttack"] 
	number_of_hits_tank = stats["goodGuyHealthMax"] / (max(0, stats["badGuyAttack"] * 0.8  - stats["goodGuyBlock"]) + 0.2 *  stats["badGuyAttack"] )


	#print("full_block" , full_block)
	#print("one_shot" , one_shot)
	#print("got_one_shot" , got_one_shot)
	#print("Number of hits" , '{:.4f}'.format(number_of_hits))
	#print("number_of_hits_tank" , number_of_hits_tank)

	return [number_of_hits, number_of_hits_tank]

	'''
	form0Container  #Normal
	form1Container  #Heap
	form2Container  #Dominance 
	'''

def num(number):
	if number != "":
		try:
			return float(number)
		except Exception as e:
			
				
			if "Qa" in number:
				return int(float(number.replace("Qa", "")) * 1e15)
			elif "Qi" in number:
				return int(float(number.replace("Qi", "")) * 1e18)
			elif "Sx" in number:
				return int(float(number.replace("Sx", "")) * 1e21)
			elif "Sp" in number:
				return int(float(number.replace("Sp", "")) * 1e24)
			elif "Oc" in number:
				return int(float(number.replace("Oc", "")) * 1e27)
			elif "No" in number:
				return int(float(number.replace("No", "")) * 1e30)
			elif "Dc" in number:
				return int(float(number.replace("Dc", "")) * 1e33)
			elif "Ud" in number:
				return int(float(number.replace("Ud", "")) * 1e36)
			elif "Dd" in number:
				return int(float(number.replace("Dd", "")) * 1e39)
			elif "Td" in number:
				return int(float(number.replace("Td", "")) * 1e42)
			elif "K" in number:
				return int(float(number.replace("K", "")) * 1e3)
			elif "M" in number:
				return int(float(number.replace("M", "")) * 1e6)
			elif "B" in number:
				return int(float(number.replace("B", "")) * 1e9)
			elif "T" in number:
				return int(float(number.replace("T", "")) * 1e12)
			else:
				print(number)
				print(e)
				return 0
	else:
		print("num() : Empty String")

def world_number(driver):
	#print("W N : " + get_elem(driver,  "worldNumber").text.replace("Lv: ", ""))
	if get_elem(driver, "worldName").text == "Spire":
		return 200
	return num(get_elem(driver,  "worldNumber").text.replace("Lv: ", ""))


def current_cell(driver):

	world_cell = -1
	map_cell = -1
	cells = driver.find_elements(By.CLASS_NAME, "cellColorCurrent")

	for c in cells:
		cell_id = c.get_attribute("id")
		if "mapCell" in cell_id:
			map_cell = int(cell_id.replace("mapCell", ""))
		else:
			world_cell = int(cell_id.replace("cell", ""))

	#print("Map cell ", map_cell)
	#print("World cell", world_cell)
	if in_world(driver):
		return world_cell
	else:
		return map_cell

def in_map_selection(driver):
	try:
		get_elem(driver,  "mapCostFragmentCost").click()
		return True
	except Exception as e:
		return False


def in_world(driver):
	try:
		get_elem(driver, "realTrimpName").click()
		return get_elem(driver, "worldName").text == "Zone" or get_elem(driver, "worldName").text == "Spire"
	except Exception as e:
		return False


def argmin(liste):
	min_val = liste[0]
	min_index = 0
	for k in range(len(liste)):
		if liste[k] < min_val:
			min_val = liste[k]
			min_index = k
	return min_index