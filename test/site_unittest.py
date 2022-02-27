# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--incognito")
        firefox_service = Service(self.driver)
        opt = Options()
        opt.add_argument ( "--incognito" )
        # opt.add_argument("--headless")
        self.browser = webdriver.Firefox ( 
            options = opt ,
            service = firefox_service
            )
    
        
        
        #self.chrome_options.add_argument("headless")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("http://10.106.197.37/manju/App1/")
        body = driver.find_element_by_tag_name("body")
        time.sleep(100)
        driver.get("http://10.106.197.37/manju/App2/#")
        driver.get("http://10.106.197.37/manju/App1/#")
        driver.get("http://10.106.197.37/manju/App2/#")

        driver.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(100)
        driver.find_element_by_id("quantity").click()
        time.sleep(1)
        Select(driver.find_element_by_id("quantity")).select_by_visible_text("10")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='CVV'])[1]/following::button[1]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//img").click()
        time.sleep(1)
        driver.find_element_by_id("quantity").click()
        time.sleep(1)
        Select(driver.find_element_by_id("quantity")).select_by_visible_text("10")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='CVV'])[1]/following::button[1]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//div[4]/div/a/img").click()
        time.sleep(1)
        driver.find_element_by_id("quantity").click()
        time.sleep(1)
        Select(driver.find_element_by_id("quantity")).select_by_visible_text("10")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='CVV'])[1]/following::button[1]").click()
        time.sleep(1)
        driver.find_element_by_link_text(u"Browse other products →").click()
        time.sleep(1)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Metal Camping Mug'])[1]/following::button[1]").click()
        time.sleep(1)
        driver.find_element_by_id("quantity").click()
        time.sleep(1)
        Select(driver.find_element_by_id("quantity")).select_by_visible_text("10")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        driver.find_element_by_id("credit_card_number").click()
        time.sleep(1)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='CVV'])[1]/following::button[1]").click()
        time.sleep(1)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    