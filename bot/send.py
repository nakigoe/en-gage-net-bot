from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.edge import service
import os
os.system("cls") #clear screen from previous sessions
import time

options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
my_service=service.Service(r'msedgedriver.exe')
options.page_load_strategy = 'eager' #do not wait for images to load
options.add_experimental_option("detach", True)

s = 30 #time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later»

driver = webdriver.Edge(service=my_service, options=options)
action = ActionChains(driver)
wait = WebDriverWait(driver,s)

text_file = open("cover-letter-ja.txt", "r")
message = text_file.read()
text_file.close()

username = "teachermaxim@gmail.com"
password = "Live12345"
login_page = "https://en-gage.net/user/login/"

search_link = "https://en-gage.net/user/search/?from=top&keyword=c%23&employ%5B%5D=1&employ%5B%5D=2&employ%5B%5D=3&employ%5B%5D=5&employ%5B%5D=7&salaryType=0&span=0&PK=B8EE9E&token=638360416b942&area=%5B%5D&job=100000_150000_200000_250000_300000_350000_400000_450000_500000_550000_600000_650000&areaText=&distanceIndex=3&wish_no=#/"

def click_all_jobs_on_the_page():
    try:
        test_links_presence = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="md_btn md_btn--round md_btn--white md_btn--big md_btn--apply"]')))
    except TimeoutException:
        return
    except StaleElementReferenceException:
        return
    if test_links_presence:
        job_links = driver.find_elements(By.XPATH, '//a[@class="md_btn md_btn--round md_btn--white md_btn--big md_btn--apply"]')
        for link in job_links:
            a = link.get_attribute('href')
            # Open a new window
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(a)
            try:
                # check if response is submitted to the server successfully:
                for i in range(5):
                    try:
                        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="md_btn md_btn--big js_modalX"]')))
                        driver.execute_script('arguments[0].click()', submit_button)
                        break
                    except TimeoutException:
                        continue
                    except StaleElementReferenceException:
                        continue
                else:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue
                
                # check if response is submitted to the server successfully:
                for i in range(5):
                    try:
                        ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="md_btn js_modalX"]')))
                        driver.execute_script('arguments[0].click()', ok_button)
                        break
                    except TimeoutException:
                        continue
                    except StaleElementReferenceException:
                        continue
                else:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue
                
                # check if response is submitted to the server successfully:
                for i in range(5):
                    try:
                        cover_letter_text = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@name="message"]')))
                        driver.execute_script('arguments[0].innerHTML = arguments[1]', cover_letter_text, message)
                        break
                    except TimeoutException:
                        continue
                    except StaleElementReferenceException:
                        continue
                else:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue
                
                # check if response is submitted to the server successfully:
                for i in range(5):
                    try:
                        cover_letter_submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="md_btn md_btn--big md_btn--submit"]')))
                        driver.execute_script("arguments[0].click()", cover_letter_submit_button)
                        break
                    except TimeoutException:
                        continue
                    except StaleElementReferenceException:
                        continue
                else:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                #wait until submitted to the server:
                wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="catch"]')))
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            
            except TimeoutException:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue
            
            except StaleElementReferenceException:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

def login():
    driver.get(login_page)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="login_id"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="login_password"]'))).send_keys(password)
    
    #make the login button active:
    inactive_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="md_btn md_btn--big md_btn--submit md_btn--disable"]')))
    driver.execute_script('arguments[0].setAttribute("class", "md_btn md_btn--big md_btn--submit")', inactive_button)
    wait.until(lambda d: 'md_btn--disable' not in inactive_button.get_attribute('class'))

    action.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="md_btn md_btn--big md_btn--submit"]')))).perform()
        
def main():
    login()
    time.sleep(2) #change to finding the loading completion indicatior
    
    #type in the manual query:
    driver.get(search_link)
    time.sleep(2) #change to finding the loading completion indicator
    while True:
        click_all_jobs_on_the_page()
        # Switch back to the first tab with search results
        driver.switch_to.window(driver.window_handles[0])

        #take in another hundred of results:
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="page page--next md_btn md_btn--white"]')))
        driver.execute_script("arguments[0].click()", next_page_button)
        time.sleep(2) #change to finding the loading completion indicator
        
    # Close the only tab, will also close the browser.
    driver.close()
    driver.quit()
main()
