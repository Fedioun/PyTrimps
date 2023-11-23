import time
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys




def export(driver):
	driver.find_element(By.XPATH, "//table[@id='settingsTable']/tbody/tr/td[2]/div").click()


	with open("save.txt", "w", encoding="utf8") as file:
		file.write(driver.find_element(By.ID, "exportArea").text)
	driver.find_element(By.ID, "confirmTooltipBtn").click()

def import_save(driver):
	driver.find_element(By.XPATH, "//table[@id='settingsTable']/tbody/tr/td[3]/div").click()
	with open("save.txt", "r", encoding="utf8") as file:
		txt = file.readline()
		print("Loading the save")
		pyperclip.copy(txt)
		clipboard_text= pyperclip.paste()
		print(len(clipboard_text))


	action = ActionChains(driver)
	action.key_down(Keys.CONTROL).perform()
	driver.find_element(By.ID, "importBox").send_keys("v")
	action.key_up(Keys.CONTROL).perform()
	driver.find_element(By.ID, "confirmTooltipBtn").click()

	try:		
		divs = driver.find_elements(By.XPATH, "//div[@id='offlineExtraBtnsContainer']/*")
		time.sleep(10)
		for d in divs:
			if "Stop Here" in d.text:
				d.click()
				driver.find_element(By.ID, "confirmTooltipBtn").click()
				break
	except Exception as e:
		print(e)