from actions import chrome_driver, wait, searchLocation, loadMoreButton, restroName, findAddress, sheet_data
from constants import resto


def foodGrab(location, web_driver):
    web_driver.get("https://food.grab.com/ph/en/")
    wait(5)
    searchLocation(web_driver, location)
    loadMoreButton(web_driver)
    names_list = restroName(web_driver)
    return names_list


loc = "Marriott Hotel Manila - 2 Resorts Dr., Pasay City, Metro Manila, NCR, 1309, Philippines"
# foodGrab(location=loc)

driver = chrome_driver()

resto_list = foodGrab(loc, driver)
all_data, sheet = sheet_data()
n = len(all_data)
row = 2
for name in resto_list:
    if name != "":
        if "[Available for LONG-DISTANCE DELIVERY]" in name:
            name = name.replace("[Available for LONG-DISTANCE DELIVERY]", "").strip()

        lat, long = findAddress(driver, name)
        sheet.insert_row([loc, name, lat, long], n + row)
        row += 1
