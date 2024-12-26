from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

service = Service()
driver = webdriver.Chrome(service=service)
driver.get("https://thai.tourismthailand.org/Search-result/attraction?destination_id=227&sort_by=datetime_updated_desc&page=1&perpage=15&menu=attraction")

place_title = []
place_location = []
place_detail = []


# WebDriverWait setup
wait = WebDriverWait(driver, 10)  # 10-second timeout

page_number = 1

# ลูปสถานที่แต่ละ page
while True:
    try:
        # รวม link ที่ href มี attraction
        links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='Attraction']")))

        for link in links:
            try:
                # Get the href and text from the link
                href = link.get_attribute("href")
                text = link.text
                
                print(f"Opening link: {text} ({href})")
                
                # เปิด link 
                driver.execute_script("window.open(arguments[0], '_blank');", href)
                driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
                

                title = driver.find_element(By.CSS_SELECTOR, ".headline").text
                try:
                    if len(driver.find_elements(By.XPATH, "/html/body/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[3]/div/div")) > 0 :
                        location = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[3]/div/div").text
                    elif len(driver.find_elements(By.XPATH, "/html/body/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[2]/div/div")) > 0 :
                        location = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[2]/div/div").text
                    elif len(driver.find_elements(By.XPATH, "/html/body/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div")) > 0 :  
                        location = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div").text
                except Exception as e:
                    print(f"Error: {e}")       
                
                detail = driver.find_element(By.CSS_SELECTOR, ".highlight-and-fact-content > div:nth-child(1)").text
                

                print(title)
                print(location)
                print(detail)

                place_title.append(title)
                # place_image.append()
                place_location.append(location)
                place_detail.append(detail)

                time.sleep(3)
                
                # ปิด tab กลับหน้าเดิม
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
            except Exception as e:
                print(f"Error occurred : {e}")
            
            
        page_number += 1
        next_url = f"https://thai.tourismthailand.org/Search-result/attraction?destination_id=227&sort_by=datetime_updated_desc&page={page_number}&perpage=15&menu=attraction"
        driver.get(next_url)
        time.sleep(3)


    
    except Exception as e:
        print(f"Error occurred: {e}")
        break

driver.quit()

df_place = pd.DataFrame({"Name" : place_title, "Location" : place_location, "Details" : place_detail} )
df_place.to_csv("place.csv", index=False)
