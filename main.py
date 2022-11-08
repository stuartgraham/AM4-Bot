from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from os import environ as osenv
from tempfile import mkdtemp
from random import uniform, randint
import logging
from sys import stdout
from pprint import pprint

# Constants and env vars
USERNAME : str = osenv.get('USERNAME')
PASSWORD : str = osenv.get('PASSWORD')
AM4_URL : str = 'https://www.airlinemanager.com/#login'
BUY_FUEL: int = 500
BUY_CO2: int = 140


# Logging config
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=stdout)


class AM4Bot():     
    def __init__(self, local_mode=False):
        self.local_mode = local_mode
        self.driver = self.web_bot()

    # Configure chomedriver parameters
    def web_bot(self):
        if self.local_mode:
            options = webdriver.ChromeOptions()
        else:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1280x1696')
            options.add_argument('--single-process')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-dev-tools')
            options.add_argument('--no-zygote')
            options.add_argument(f'--user-data-dir={mkdtemp()}')
            options.add_argument(f'--data-path={mkdtemp()}')
            options.add_argument(f'--disk-cache-dir={mkdtemp()}')
            options.add_argument('--remote-debugging-port=9222')
        return webdriver.Chrome(options=options)

    # Login process - will enter necessary credentials for logging into AM4
    def login(self):
        try:
            logging.info(f'LOAD: Loading {AM4_URL}')
            self.driver.get(AM4_URL)
            random_sleep(2,4)

            # Find username bar and enter it
            logging.info(f'TYPE: username {USERNAME}')
            email_in = self.driver.find_element(By.XPATH, '//*[@id="lEmail"]')
            email_in.send_keys(USERNAME)
            random_sleep(1,2)
            
            # Find password bar and enter it
            logging.info(f'TYPE: password *****')
            pw_in = self.driver.find_element(By.XPATH, '//*[@id="lPass"]')
            pw_in.send_keys(PASSWORD)
            random_sleep(1,2)

            # Click login button
            logging.info(f'CLICK: Click login button')
            login_btn = self.driver.find_element(By.XPATH, '//*[@id="btnLogin"]')
            login_btn.click() 
            random_sleep(20,30)

        except:
            logging.error(f'LOGIN: Failed to login')
            self.driver.close()
            random_sleep(1800, 3600)

    # Verifies if the account is logged in
    def verify_logged_in(self):
        # Tests for account value to ensure logged in
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        with open("output1.html", "w") as file:
            file.write(str(soup))
        account_balance = soup.find('span', attrs={'id': 'headerAccount'}).text
        ic(account_balance)
        sleep(1800)
        if account_balance:
            logging.info(f'LOGIN: Successfully logged in')
            return True
        else:
            logging.info(f'LOGIN: Not logged in')
            return False


    # Buys max fuel for BUY_FUEL and below
    def fuel_check(self):
        try:
            # Click fuel button
            logging.info(f'CLICK: Open fuel')
            fuel_btn = self.driver.find_element(By.XPATH, '//*[@data-original-title="Fuel & co2"]')
            fuel_btn.click()
            random_sleep(2,10)
            
            # Get fuel capacity
            fuel_remaining_capacity = self.driver.find_element(By.XPATH, "//*[@id=\"remCapacity\"]").text
            fuel_remaining_capacity = int(''.join(x for x in fuel_remaining_capacity if x.isdigit()))
            logging.info(f'INFO: fuel remaining {fuel_remaining_capacity}')
            random_sleep(2,10)
            
            if fuel_remaining_capacity == 0:
                logging.info(f'FUEL: maximum fuel in tank')
            
            else:
                # Read fuel price
                fuel_price = self.driver.find_element(By.XPATH, "//*[@id=\"fuelMain\"]/div/div[1]/span[2]/b").text
                fuel_price = int(''.join(x for x in fuel_price if x.isdigit()))
                logging.info(f'FUEL: fuel price {fuel_price}')
                random_sleep(2,10)

                if fuel_price <= BUY_FUEL:
                    # Find amount to purchase bar end enter max fuel amount to buy 
                    fuel_amount = self.driver.find_element(By.XPATH, '//*[@id="amountInput"]')
                    fuel_amount.send_keys(999999999)
                    logging.info(f'FUEL: buy max fuel')
                    random_sleep(2,10)
                    
                    # Click fuel purchase button
                    fuel_buy = self.driver.find_element(By.XPATH, '//button[normalize-space()="Purchase"]')
                    fuel_buy.click()
                    logging.info(f'CLICK: purchase fuel')
                    random_sleep(2,10)

                else:
                    logging.info(f'FUEL: fuel price is above {BUY_FUEL}')
                
            # Close fuel panel
            fuel_close_btn = self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span')
            fuel_close_btn.click()
            logging.info(f'CLICK: close fuel')
            random_sleep(2,10)
        
        except:
            logging.error(f'FUEL: Unable to buy fuel')
    
    # Buys max fuel for BUY_CO2 and below
    def co2_check(self):
        try:
            # Click fuel button
            logging.info(f'CLICK: Open fuel')
            fuel_btn = self.driver.find_element(By.XPATH, '//*[@data-original-title="Fuel & co2"]')
            fuel_btn.click()
            random_sleep(2,10)
            

            # Click CO2 button
            logging.info(f'CLICK: CO2 Button')
            co2_btn = self.driver.find_element(By.XPATH, '//*[@id="popBtn2"]')
            co2_btn.click()
            random_sleep(2,10)
            
            # Get fuel capacity
            co2_remaining_capacity = self.driver.find_element(By.XPATH, "//*[@id=\"remCapacity\"]").text
            co2_remaining_capacity = int(''.join(x for x in co2_remaining_capacity if x.isdigit()))
            logging.info(f'INFO: co2 remaining {co2_remaining_capacity}')
            random_sleep(2,10)

            if co2_remaining_capacity == 0:
                logging.info(f'CO2: maximum co2 in tank')
            
            else:
                # Get CO2 price
                co2_price = self.driver.find_element(By.XPATH, "//*[@id=\"co2Main\"]/div/div[2]/span[2]/b").text
                co2_price = int(''.join(x for x in co2_price if x.isdigit()))
                random_sleep(2,10)

                if co2_price <= BUY_CO2:
                    # Find amount to purchase bar end enter max fuel amount to buy 
                    co2_amount = self.driver.find_element(By.XPATH, '//*[@id="amountInput"]')
                    co2_amount.send_keys(999999999)
                    logging.info(f'CO2: buy max co2')
                    random_sleep(2,10)
                    
                    # Click fuel purchase button
                    co2_buy = self.driver.find_element(By.XPATH, '//button[normalize-space()="Purchase"]')
                    co2_buy.click()
                    logging.info(f'CLICK: purchase co2')
                    random_sleep(2,10)

                else:
                    logging.info(f'CO2: co2 price is above {BUY_CO2}')
            
            # Close fuel panel
            fuel_close_btn = self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span')
            fuel_close_btn.click()
            logging.info(f'CLICK: close fuel')
            random_sleep(2,10)
        
        except:
            logging.error(f'CO2: Unable to buy co2')

    def eco_friendly_campaign(self):
        try:
            # Click Finance button
            finance_btn = self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[3]/div[5]')
            finance_btn.click()
            sleep(6)
            
            # Click Marketing button
            market_btn = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div[1]/button[2]')
            market_btn.click()
            sleep(4)
            
            # Click new campagin button
            new_camp_btn = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div[2]/div/div[1]/div[2]/button')
            new_camp_btn.click()
            
            # This part try buy campaign
            
            # Click on Eco-friendly button
            new_eco_friendly_btn = self.driver.find_element(By.XPATH, '//*[@id="campaign-1"]/table/tbody/tr[2]')
            new_eco_friendly_btn.click()
            random_sleep(2,10)
            
            # Click on start Eco-friendly campaign
            new_eco_f_start_btn = self.driver.find_element(By.XPATH, '//*[@id="marketingStart"]/table/tbody/tr/td[3]/button')
            new_eco_f_start_btn.click()
            random_sleep(2,10)
            
            print("Bought: Eco Friendly Campaign")
            
            # Close Finance panel
            fin_close_btn = self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span')
            fin_close_btn.click()
            random_sleep(2,10)
        
        except:
            # Close Finance panel
            fin_close_btn = self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span')
            fin_close_btn.click()
            random_sleep(2,10)

    def increase_rep_campaign(self):
        try:
            # Click Finance button
            finance_btn = self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[3]/div[5]')
            finance_btn.click()
            sleep(6)
            
            # Click Marketing button
            market_btn = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div[1]/button[2]')
            market_btn.click()
            sleep(4)
            
            # Click new campagin button
            new_camp_btn = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div[2]/div/div[1]/div[2]/button')
            new_camp_btn.click()
            
            # Click on Increase airline reputation button
            new_increse_btn = self.driver.find_element(By.XPATH, '//*[@id="campaign-1"]/table/tbody/tr[1]')
            new_increse_btn.click()
            
            # Wait until Start campaign panel is loaded
            random_sleep(2,10)
            
            # Click on hour of campaign button
            control_btn = self.driver.find_element(By.XPATH, '//*[@id="dSelector"]')
            control_btn.click()
            random_sleep(2,10)
            
            # Click on 24h of campaign button
            control_btn = self.driver.find_element(By.XPATH, '//*[@id="dSelector"]/option[6]')
            control_btn.click()
            random_sleep(2,10)
            
            # Click on start Eco-friendly campaign
            new_increase_start_btn = self.driver.find_element(By.XPATH, '//*[@id="c4Btn"]')
            new_increase_start_btn.click()
            random_sleep(2,10)
            
            print("Bought: Increase Reputation Campaign")
            
            # Close Finance panel
            fin_close_btn = self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span')
            fin_close_btn.click()
            random_sleep(2,10)
            
        except:
            # Close Finance panel
            fin_close_btn = self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span')
            fin_close_btn.click()
            random_sleep(2,10)

    def depart_all(self):
        try:
            # check for Depart button
            depart_button = self.driver.find_element(By.XPATH, '//button[normalize-space()="Depart"]')
            depart_button.click()
            logging.info(f'CLICK: depart button')
            random_sleep(10,20)
            logging.info(f'DEPARTED: departed planes')

        except:
            logging.info(f'DEPARTED: could not depart any planes')

        try:
            # check for Depart button
            depart_button = self.driver.find_element(By.XPATH, '//button[normalize-space()="Inflight"]')
            depart_button.click()
            depart_button = self.driver.find_element(By.XPATH, '//button[normalize-space()="Landed"]')
            depart_button.click()
            depart_button = self.driver.find_element(By.XPATH, '//button[normalize-space()="Depart"]')
            depart_button.click()
            logging.info(f'CLICK: depart button')
            random_sleep(10,20)

        except:
            logging.info(f'DEPARTED: could not depart any planes')


    def current_time(self):
        return datetime.now().time().strftime("%d/%m/%Y %H:%M:%S")

# Will sleep for a random period of time between start and end secs
def random_sleep(start, end) -> None:
    sleep(uniform(start, end))

# Will provide a bi-hourly minute slot for running
def random_slot(current_minute):
    if current_minute == 0:
        return randint(0,25)
    if current_minute == 30:
        return randint(30,55)

# Provides a random time slot in the 30 minute window
def await_time_slot():
    time_slot = -1
    while True:
        if datetime.now().minute == 0:
            time_slot = random_slot(0)
        if datetime.now().minute == 30:
            time_slot = random_slot(30)
        
        if time_slot > 0:
            logging.info(f'TIMESLOT: time slot set to {time_slot}')
        
        if datetime.now().minute == time_slot:
            logging.info(f'TIMESLOT: time slot open')
            return
        else:
            sleep(60)


def main(local_mode=False):
    pass
    #sleep(120)
    #bot = AM4Bot(local_mode=local_mode)
    #bot.login()
    #bot.verify_logged_in()
    # while True:
    #     if bot.verify_logged_in():
    #         logging.info(f'AWAIT: Waiting on next time slot')
    #         await_time_slot()
    #         bot.fuel_check()
    #         bot.co2_check()
    #         # marketting
    #         bot.depart_all()
    #         bot.fuel_check()
    #         bot.co2_check()
    #     else:
    #         bot.login()


if __name__ == "__main__":
    main()