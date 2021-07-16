import os, time, sys, re
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Set up browser and adblocker
source = r"http://sortyourmusic.playlistmachinery.com/"
path_to_extension = r'C:\Users\tscot\OneDrive\Documents\OneDrive\Desktop\1.35.2_0'  # Loads adblocker for selenium
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)
driver = webdriver.Chrome(options=chrome_options)
driver.create_options()
driver.get(source)
driver.maximize_window()
driver.implicitly_wait(5)
username = os.environ.get("invest_username")  # Change to own username and password
password = os.environ.get("spot_password")

# Log in
driver.find_element_by_id("go").click()
driver.find_element_by_id("login-username").send_keys(username)
driver.find_element_by_id("login-password").send_keys(password)
driver.find_element_by_id("login-button").click()

# Navigate to desired playlist
playlist_name = "Liked Songs"  # Change to your playlist
playlist_length = 1426  # Change depending on your length, 100% a way to do this automatically but can't w/o xpath
driver.find_element_by_link_text(playlist_name).click()
time.sleep(2)

# Scroll to bottom
count = playlist_length // 200 + 1  # The website loading is unpredictable but this should create a buffer
while count != 0:
    driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL + Keys.END)
    time.sleep(4)
    count -= 1

# Scrape table data
tags = driver.find_elements_by_tag_name('td')
dateformat = re.compile(r"\d\d\d\d-\d\d-\d\d|\d\d\d\d-\d\d")  # Date format of yyyy-mm-dd and yyyy-mm
for index, value in enumerate(tags):
    if dateformat.search(value.text) is not None: # Finds the first hit of a date to start the for loop for all dates
        first_instance = index
        break
    else:
        continue

try:
    first_instance
except NameError:
    print("The program was unable to find first_instance, program will now exit")
    sys.exit()

years_templist = []  # Need to create a temporary list as a new list will be created later
for i in range(int(first_instance), len(tags), 13):
    date = tags[i]
    years_templist.append(date.text)
driver.quit()

# Use regular expressions to trim date format (yyyy-mm-dd)
years_list = []
for year in years_templist:
    if dateformat.match(year):
        cut_year = str(year)[:4]  # Cuts out the mm-dd out of yyyy-mm-dd / yyyy-mm
        years_list.append(int(cut_year))
        continue
    else: # If it doesn't get matched by the regex, then that means it is already in yyyy format
        years_list.append(int(year))
        continue

if len(years_list) != playlist_length:
    print("Something has gone wrong, the length of years_list is %d while the user-input playlist_length is %d" %
          (len(years_list), playlist_length))
    print(years_list)
    sys.exit()

# Use matplotlib to make a chart directly
ordered_list = sorted(years_list)

plt.hist(ordered_list, color='#01247d')
plt.title('Timeline of %s' % playlist_name)
plt.xlabel('Year')
plt.ylabel('Number of Songs')
plt.show()
