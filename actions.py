from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Google sheet scopes
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)


def foodGrab(location, web_driver):
    web_driver.get("https://food.grab.com/ph/en/")
    wait(5)
    searchLocation(web_driver, location)
    loadMoreButton(web_driver)
    names_list = restroName(web_driver)
    return names_list


def sheet_data():
    sheet = client.open("Food Grab").worksheet("Sheet1")

    all_data = sheet.get_all_records()

    return all_data, sheet


def chrome_driver():
    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.binary_location = binary_location
    web_driver = webdriver.Chrome(executable_path=driver_location, chrome_options=options)
    web_driver.maximize_window()
    web_driver.implicitly_wait(10)
    return web_driver


def wait(t):
    time.sleep(t)


def loadMoreButton(driver):
    try:
        load_more_button = driver.find_element_by_css_selector("button.ant-btn.ant-btn-block")
        i = 0
        while i < 3:
            load_more_button.click()
            wait(10)
            i += 1

    except Exception as ex:
        print(ex)


def searchLocation(driver, location):
    search = driver.find_element_by_class_name("ant-input")
    search.send_keys(location)
    wait(5)
    search.send_keys(Keys.RETURN)
    wait(2)
    driver.find_element_by_css_selector('button.ant-btn.submitBtn___2roqB.ant-btn-primary').click()

    return 0


def restroName(driver):
    names_list = []
    for item in driver.find_elements_by_css_selector("h6.name___2epcT"):
        names_list.append(item.text)

    return names_list


def findLatLong(driver, name):
    latitude = "NA"
    longitude = "NA"
    try:
        driver.get("https://www.google.com/maps/")

        search = driver.find_element_by_class_name("tactile-searchbox-input")
        name = name + " manila"
        search.send_keys(name)
        wait(4)
        search.send_keys(Keys.RETURN)
        wait(4)
        current_url = driver.current_url
        coordinates = current_url.split("/")[6].replace("@", "").split(",")
        latitude = coordinates[0]
        longitude = coordinates[1]

        print(latitude, longitude)
    except Exception as ex:
        print(ex)

    return latitude, longitude
