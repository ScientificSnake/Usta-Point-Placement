from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def navigate_to_tourney(driver :webdriver.Chrome, link:str):
    driver.get(link)
    
    divbutton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"tournaments\"]/div/div/div[2]/div[3]/div/div/div/div/div/div/div"))
    )
    divbutton.click()

def main():

    division = "Boys' 16 & under Singles"

    chrome_service = Service(executable_path=r"C:\Users\segea631\Documents\ChromeDriver\chromedriver.exe")

    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Chrome(service=chrome_service)    
    navigate_to_tourney(driver, r"https://playtennis.usta.com/Competitions/eugeneswimandtennisclub/Tournaments/players/7D514C1C-55C1-4D60-9939-326209AF52D7")
    select_division(driver, division)


def select_division(driver, division : str):
    division_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), \"{division}\")]"))
    )
    division_button.click()


def scrape_player_points(driver: webdriver.Chrome):
    bodyelement = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located((By.XPATH, r'//*[@id="player-list"]/tbody'))
    )

    

if __name__ == "__main__":
    main()
    input()