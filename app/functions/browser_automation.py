from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from app.util.utility import getsavePath


def akshaya(subproject, browser, site_data, lead_data):
    try:
        save_path = getsavePath("./akshaya/", subproject)
        browser.get(site_data["url"])
        f_email = browser.find_element(By.ID, "user_email")
        f_email.send_keys(site_data["email"])
        f_password = browser.find_element(By.ID, "user_password")
        f_password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH, "//button[@type='submit']").click()
        f_Leads = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Leads")))
        # f_Leads = browser.find_element(By.LINK_TEXT, "Leads")
        f_Leads.click()
        f_addlead = browser.find_element(
            By.XPATH, "//a[@href='/broker/2150/leads/new']")
        f_addlead.click()
        f_firstname = browser.find_element(By.ID, "lead_first_name")
        f_firstname.send_keys(lead_data.get("first_name"))
        f_lastname = browser.find_element(By.ID, "lead_last_name")
        f_lastname.send_keys(lead_data.get("last_name"))
        f_mail = browser.find_element(
            By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        f_mail.click()
        f_mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        f_mail1.click()
        f_mail1.send_keys(lead_data.get("email"))
        f_mail1.send_keys(Keys.RETURN)
        f_phone = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        f_phone.click()
        f_phone.send_keys(lead_data.get("phone"))
        f_button2 = browser.find_element(
            By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        f_button2.click()
        f_project1 = browser.find_element(
            By.XPATH, '/html/body/div[4]/div/input')
        f_project1.send_keys(subproject)
        f_project1.send_keys(Keys.RETURN)

        browser.save_screenshot(save_path[0])
        browser.implicitly_wait(10)
        browser.save_screenshot(save_path[1])
        browser.close()
        return "success"
    except Exception as e:
        browser.close()
        return "failed"

# def aditiyaram(subproject,browser,site_data,lead_data):
# def alliance(subproject, browser, site_data, lead_data):
