from actions import chrome_driver, findLatLong, sheet_data, foodGrab
from constants import resto, loc


driver = chrome_driver()
resto_list = foodGrab(loc, driver)

all_data, sheet = sheet_data()
n = len(all_data)

row = 2
for name in resto_list:
    if name != "":
        if "[Available for LONG-DISTANCE DELIVERY]" in name:
            name = name.replace("[Available for LONG-DISTANCE DELIVERY]", "").strip()

        lat, long = findLatLong(driver, name)
        sheet.insert_row([loc, name, lat, long], n + row)
        row += 1
