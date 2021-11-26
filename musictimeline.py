import time, re
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from collections import Counter
from tkinter import *
import tkinter as tk
from secrets import username, password

# Set up browser and adblocker
source = r"http://sortyourmusic.playlistmachinery.com/"
path_to_extension = r'C:\Users\Ayden\AppData\Local\Programs\Python\Python39\1.35.2_0'  # Loads adblocker for selenium
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)
driver = webdriver.Chrome(options=chrome_options)
driver.create_options()
driver.get(source)

# I tried to run Selenium in headless mode but webPlaylists would inconsistently come back empty. I wanted to run it
# in headless to make it more user-friendly so that all the user had to do was pay attention to the command window,
# perhaps there's a way to fix headless mode

driver.minimize_window()

# Log in
driver.find_element_by_id("go").click()
driver.find_element_by_id("login-username").send_keys(username)
driver.find_element_by_id("login-password").send_keys(password)
driver.find_element_by_id("login-button").click()
print("STATUS: Logged in")

# Navigate to desired playlist
time.sleep(7)  # This can probably be lower but had previous problems with webPlaylists being empty
webPlaylists = driver.find_elements_by_class_name("hoverable")
if not webPlaylists:  # In place in the off chance webPlaylists cannot be found
    print("The program was unable to find the playlists, this is a common bug. Try rerunning the program. If that "
          "does not resolve the issue, add the issue to the GitHub Repo")
# This playlist is created to retrieve the correct playlists since selenium returns web elements instead of text
playlists = [i.text for i in webPlaylists]


# Creating Drop Down Menu
def postselection(choice):
    global playlist_name
    playlist_name = choice
    root.destroy()  # Close menu after user chooses playlist


root = Tk()
selected = StringVar()
selected.set(playlists[0])
root.geometry("400x400")
root.title("Please select a playlist from the dropdown")
drop = OptionMenu(root, selected, *playlists, command=postselection)
tk.Label(root, text="Choose a playlist from the dropdown menu")
drop.pack()
root.mainloop()

driver.find_element_by_link_text(playlist_name).click()
print("STATUS: Playlist found! Loading webpage")
time.sleep(1.5)

# Scroll to bottom
reached_page_end = False
last_height = driver.execute_script("return document.body.scrollHeight")

while not reached_page_end:
    driver.find_element_by_xpath('//body').send_keys(Keys.END)
    time.sleep(2.5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if last_height == new_height:
        reached_page_end = True
    else:
        last_height = new_height

# Scrape table data
print("STATUS: Scraping table data")
tags = driver.find_elements_by_tag_name('td')
dateformat = re.compile(r"\d\d\d\d-\d\d-\d\d|\d\d\d\d-\d\d")  # Date format of yyyy-mm-dd and yyyy-mm
for index, value in enumerate(tags):
    if dateformat.search(value.text) is not None:  # Finds the first hit of a date to start the for loop for all dates
        first_hit = index
        break
    else:
        continue

years_templist = []  # Need to create a temporary list as a new list will be created later
for i in range(int(first_hit), len(tags), 13):  # Ignore first_hit can be undefined, that's garbage it's fine
    date = tags[i]
    years_templist.append(date.text)

# Use regular expressions to trim date format
years_list = []
for year in years_templist:
    if dateformat.match(year):
        cut_year = str(year)[:4]  # Cuts out the mm-dd out of yyyy-mm-dd / yyyy-mm
        years_list.append(int(cut_year))
        continue
    else:  # If it doesn't get matched by the regex, then that means it is already in yyyy format
        years_list.append(int(year))
        continue

# Collect artist data
print("STATUS: Scraping and compiling artist data")
artist_list = []
for i in range(first_hit - 1, len(tags), 13):
    artist = tags[i]
    artist_list.append(artist.text)

# Collect length data
print("STATUS: Scraping and compiling length data")
length_list = []
lowcount, middlecount, highcount = 0, 0, 0
for i in range(first_hit + 6, len(tags), 13):
    length = tags[i]
    adjLength = length.text.replace(":", ".")  # Time comes in as d:dd, need to change to float d.dd
    if float(adjLength) <= 3:
        lowcount += 1
    elif float(adjLength) >= 4:
        highcount += 1
    else:
        middlecount += 1
length_list = [lowcount, middlecount, highcount]


# Use matplotlib to make a chart directly
def better_labels(values):  # https://stackoverflow.com/questions/6170246/how-do-i-use-matplotlib-autopct
    def my_autopct(pct):  # Shows the actual amount of each slice in addition to percent
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

    return my_autopct


driver.quit()  # I don't know why but having this earlier breaks the program
figure, axis = plt.subplots(1, 2)
plt.subplot(1, 2, 1)  # Histogram of song release dates
plt.hist(years_list, color='#01247d')
plt.title('Timeline of %s' % playlist_name)
plt.xlabel('Year')
plt.ylabel('Number of Songs')

plt.subplot(1, 2, 2)  # Pie chart of song lengths
labels = 'Below 3 Minutes', 'Between 3 and 4 Minutes', 'Greater than 4 Minutes'
plt.pie(length_list, labels=labels, autopct=better_labels(length_list))
plt.title('Length of Songs in %s' % playlist_name)
plt.subplots_adjust(wspace=0.5)
# Prints out the 10 most common artists and the number of their songs
print("Most frequent artists in %s:\n" % playlist_name + str(Counter(artist_list).most_common(10)))
plt.show()
