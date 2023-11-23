from selenium.webdriver.common.by import By
from tools import num, world_number
import time
import config

def go_portal(driver):
	pass



def portal(driver):
	global state
	try:
		print("Portal")

		driver.find_element(By.ID, "portalBtn").click()

		driver.find_element(By.ID, "clearPerksBtn").click()
		

		perks = config.PERKS
		

		tot = 0
		for p in perks:
			tot += perks[p]

		tot_helium = num(driver.find_element(By.ID, "portalHeliumOwned").text)
		helium = tot_helium

		for p in perks:
			print(p)
			print("Tot and spent")
			print(tot, tot_helium * (perks[p] / tot))
			spent = 0
			elem = driver.find_element(By.ID, p)
			try:
				elem.click()
			except Exception as e:
				print("failed to click")
			cost = helium - num(driver.find_element(By.ID, "portalHeliumOwned").text)
			helium = helium - cost
			spent += cost

			
			print(cost, spent, tot_helium, helium)

			while spent < tot_helium * (perks[p] / tot) and "perkColorOn" in elem.get_attribute("class"):
				try:
					elem.click()
				except Exception as e:
					print("failed to click")
				cost = helium - num(driver.find_element(By.ID, "portalHeliumOwned").text)
				spent += cost
				helium = helium - cost
				print(cost, spent, tot_helium, helium)
			tot_helium = helium
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