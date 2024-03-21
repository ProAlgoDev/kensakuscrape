import os
import time
from datetime import  datetime 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import urllib

from openpyxl import load_workbook, Workbook
import re
from libs.start_web_driver import start_driver
from libs.check_last_information import check_last_lawyer_information, update_last_lawyer_information
from CONSTANT import SHORT_WAIT_TIME, MID_WAIT_TIME, LONG_WAIT_TIME, KENSAKU



data_result_directory = os.path.join('result_data')
os.makedirs(data_result_directory, exist_ok=True)


class Kensaku():

    def __init__(self):

        super().__init__()
        self.site_link = 'https://kensaku.shiho-shoshi.or.jp/search/member.php'
        self.new_data = []
        self.last_info = ''
        self.last_number = 0

    def _start_driver(self):
        driver = start_driver()

        return driver

    
    def get_information(self):
        
        driver = self._start_driver()
        driver.get(self.site_link)
        
        try:
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.ID, 'kojin'))
            )
        except Exception as e:
            driver.quit()
            print('access error...')

        page = 0
        while True:

            table = driver.find_element(By.ID, 'kojin')
            table_trs = table.find_elements(By.TAG_NAME, 'tr') 
            page += 1

            self.last_number = 0

            for idx, tr_item in enumerate(table_trs):
                if idx == 0 or idx == 1:
                    continue
                

                current_item_information = tr_item.find_element(By.CSS_SELECTOR, 'td.font_m10').text

                lines = current_item_information.split('\n')
                postal_code_pattern = r'〒(\d{3}-\d{4})'
                postal_code = re.search(postal_code_pattern, lines[0]).group(1)
                address = lines[1]
                phone = lines[2].split('：')[1].strip()
                
                office_name = tr_item.find_elements(By.TAG_NAME, 'td')[5].text
                
                result = check_last_lawyer_information(site_name=KENSAKU, last_info=postal_code)
                
                if (idx == 2) and (page == 1):
                    self.last_info = postal_code

                if not result:
                    break
                
                self.get_new_information(office_name=office_name, postal_code=postal_code, address=address, phone=phone)
                self.last_number = idx

            if self.last_number  == len(table_trs) - 1 :
                pagination  = driver.find_element(By.CSS_SELECTOR, 'div.pagination.pagebottom')
                next_tag = pagination.find_element(By.XPATH, "//a[contains(@title, 'next page')]")
                next_tag.click()
            else:
                break

        self.save_new_data()

        update_last_lawyer_information(site_name=KENSAKU, last_info=self.last_info)

        driver.quit()
        time.sleep(5*60)


    def get_new_information(self, office_name, postal_code,  address, phone):
        print( office_name, postal_code,  address, phone)
        fax = ''
        email = ''
        register_number = ''
        self.new_data.append(['司法書士', office_name, postal_code,  address, phone, fax, email, register_number])



    def save_new_data(self):
        if len(self.new_data) == 0:
            return
        wb = Workbook()
        sheet = wb.worksheets[0]
        sheet.append(["業種", "事務所名", "郵便番号", "住所", "電話番号", "FAX番号", "メールアドレス", "登録番号"])


        for row in self.new_data:
            sheet.append(row)


        dt_now = datetime.now()
        now_time=dt_now.strftime('%Y%m%d%H%M%S')

        result_data_file_name= KENSAKU +"_result_data_" + now_time + ".xlsx"                        

        result_data_file = os.path.join(data_result_directory, result_data_file_name)
                    
        wb.save(result_data_file)
