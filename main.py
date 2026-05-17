from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def navigate_to_tourney(driver : webdriver.Chrome, link:str):
    driver.get(link)
    
    divbutton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="tournaments"]/div/div/div[2]/div[3]/div/div/div/div[1]/div[2]/div'))
    )
    divbutton.click()


def get_biggest_point(sorted):
    points = [i[0] for i in sorted]
    big = max(points)
    return len(str(big))


def main():
    tourneylink = r"https://playtennis.usta.com/Competitions/vancouver-tennis-center/Tournaments/players/12F62C8C-92BE-4A89-AD70-9174EE2F326D"
    division = 3
    pointsmethod = "Boys' 16 National Standings List (combined)"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    try:
        driver = webdriver.Chrome(options)
    except:
        # tweaky school firewall
        chrome_service = Service(executable_path=r"C:\Users\segea631\Documents\ChromeDriver\chromedriver.exe")
        driver = webdriver.Chrome(service=chrome_service)    
    navigate_to_tourney(driver, tourneylink)
    select_division(driver, division)

    player_points = scrape_player_points(driver, pointsmethod)
    sorted_player_points = sort_point_dictionary(player_points)
    
    biggets_points = get_biggest_point(sorted_player_points)
    
    i = 0
    for points, name in sorted_player_points:
        i += 1
        print(f'{str(i).ljust(len(str(len(sorted_player_points))))} | {str(points).ljust(biggets_points)} | {name}')
    pass


def select_division(driver, division : int):
    divisioncontainer = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div[3]/ul"))
    )

    children = divisioncontainer.find_elements(By.XPATH, "./*")
    
    children[division].click()


def sort_point_dictionary(unsorted : dict[str, int]):
    new_list = []
    for key, val in unsorted.items():
        new_list.append((val,key))
    
    new_list.sort(reverse=True)
    return new_list


def scrape_player_points(driver: webdriver.Chrome, points_method) -> dict[str, int]:
    playerpoints = {}
    bodyelement = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located((By.XPATH, r'//*[@id="player-list"]/tbody'))
    )

    elementtable = bodyelement.find_elements(By.XPATH, "./*")
    player_index = 0
    for element in elementtable:
        grandchildren = element.find_elements(By.XPATH, "./*")
        if len(grandchildren) == 1:
            
            # it is a Alphabetically placeholdeer
            continue
        player_index += 1
        print(f'Starting player {player_index}')
        original_window_handle = driver.current_window_handle
        playerlink = grandchildren[0].find_elements(By.XPATH, "./*")[0]
        playerlink.click()

        # switch tabs
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        new_window_handle = (set(driver.window_handles) - {original_window_handle}).pop()
        driver.switch_to.window(new_window_handle)
        assert driver.current_window_handle == new_window_handle

        name_element = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.XPATH,'//*[@id="container-cdeaf649fc"]/div/div[1]/div[1]/div/div/span/h3'))
        )
        playername = name_element.text

        ranking_button = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.XPATH,"//*[@data-title='Rankings']"))
        )
        ranking_button.click()

        try:
            pointstable = WebDriverWait(driver,10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="container-85da4eb619"]/div/div/div/div[2]/div/div[1]/div/div/div/div'))
            )
        except Exception as e:
            print(f"Failed to find {playername}'s points, possible due to no ranking data available. Setting as 0 and Continuing")
            playerpoints[playername] = 0
            
            driver.close()
            WebDriverWait(driver,10).until(
                EC.number_of_windows_to_be(1)
            )
            driver.switch_to.window(original_window_handle)
            assert driver.current_window_handle == original_window_handle
            continue

        pointelements = pointstable.find_elements(By.XPATH, "./*")
        correct_element = None
        for row in pointelements:
            if points_method in row.text:
                correct_element = row
                break
        
        if correct_element == None:
            # this means they dont have poitns since they have no element in table that is that points
            playerpoints[playername] = 0
        else:
            split_text = correct_element.text.split("\n")
            points = int(split_text[2])
            playerpoints[playername] = points
        
        # closeing tabs n stuff

        driver.close()
        WebDriverWait(driver,10).until(
            EC.number_of_windows_to_be(1)
        )

        driver.switch_to.window(original_window_handle)
        assert driver.current_window_handle == original_window_handle

    return playerpoints


if __name__ == "__main__":
    main()
    input()