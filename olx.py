import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from xlsxwriter import Workbook
from credentials import Email, Password, Driver_path, Path

class Olx:
    def __init__(self, total_numbers=40, ):
        self.username = Email
        self.password = Password
        self.path = Path
        self.driver = webdriver.Chrome(Driver_path)

        self.number_count = total_numbers # count of numbers you want you save
        self.driver.get('https://www.olx.com.pk/')

        self.log_in()
        time.sleep(2)

        self.load_all_adds()
        time.sleep(2)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.all_links = soup.find_all('li', class_='EIR5N')
        time.sleep(2)

        self.write_numbers_to_excel_file()
        self.driver.close()

    def write_numbers_to_excel_file(self):
        workbook = Workbook('numbers.xlsx')
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0, 'Mobile Numbers')
        row += 1

        for link in self.all_links:
            try:
                self.driver.get('https://www.olx.com.pk' + str(link.a['href']))
                time.sleep(5)
                show_number = self.driver.find_element_by_xpath('//div[contains(text(), "Show number")]')
                parent_class = show_number.find_element_by_xpath("./..").get_attribute('class')
                show_number.click()

                time.sleep(3)
                parent = self.driver.find_element_by_class_name(parent_class)
                number = parent.find_elements_by_css_selector("*")[1].text
                worksheet.write(row, 0, number)
                row += 1
                time.sleep(2)
            except Exception as e:
                print(e)
                continue
        workbook.close()

    def load_all_adds(self):
        try:
            if self.number_count < 20:
                loop = 1
            else:
                loop = int(self.number_count / 20)
            for val in range(loop):
                load_more = self.driver.find_element_by_xpath("//span[.='load more']")
                time.sleep(2)
                load_more.click()
                time.sleep(3)
        except Exception:
            pass

    def log_in(self):
        try:
            log_in = self.driver.find_element_by_xpath('//span[contains(text(), "Login")]')
            log_in.click()
            time.sleep(2)
        except Exception:
            print('Unable to find login button')
        else:
            try:
                login_by_email = self.driver.find_element_by_xpath("//span[.='Continue with Email']")
                login_by_email.click()
                time.sleep(3)
                email_field = self.driver.find_element_by_name('email')
                email_field.send_keys(self.username)
                email_field.submit()
                time.sleep(5)
                pswd_field = self.driver.find_element_by_name('password')
                pswd_field.send_keys(self.password)
                pswd_field.submit()

            except Exception:
                print('Some exception occurred while trying to find username or password field')


if __name__ == '__main__':
    olx = Olx()
