# SpotifyPlaylistTimeline
Python program that scrapes http://sortyourmusic.playlistmachinery.com/ and collects all of the dates of your playlists' songs. The program then uses matplotlib to plot a histogram of the data which is displayed to the user. 

## Usage
In order to use this program, the user must:
* Alter variables username and password to their own Spotify credentials
* Alter variable playlist_name to the name of the playlist they would like to scrape
* Alter variable playlist_length to the length of songs in the chosen playlist

## How It Works
This program relies on http://sortyourmusic.playlistmachinery.com/ which does most of the heavy lifting by finding all of the release dates of songs and putting them in a single table. On the program's side, it uses selenium and regular expressions to scrape the data. The main umbrella comes from finding all of the tags with 'td' and sorting through them. Since dates appear on each row in the same position, the program is able to have a for loop with an indentation of 13 that spans all of the tags. This loop appends to a temporary list which will need to be cut by using regular expressions. This is because the website displays data in three forms: yyyy, yyyy-mm, and yyyy-mm-dd. To ensure that the plot can read it all, I decided to make all dates into the form yyyy which can easily be done by cutting the string(:4). Once this new list is created from the cut date formats, the program used matplotlib to make a histogram of the data which is displayed to the user and can be saved within matplotlib's GUI. 

## Possible Improvements
* Automatically finding the playlist length when given the name of the playlist (since the information is listed side by side but by inputing the playlist name, selenium is finding it by link text not by xpath. Therefore, I've been unable to find a concise way of taking the element found by link text and converting it to xpath whereby you can find the sibling element)
* Display data in a more informative way by altering the amount of bins, the ticks on the x-axis, or other graph-related changes to enhance readability (This one is very important but as I have little experience plotting such large histograms (the playlist I was using had ~1400 songs) I was unable to strike a balance between readability and precision)

## Future Uses
By changing the regular expressions, the program could quickly be changed to search for other types of data present on the page. For example, a pie chart could be created that sorts the length of the songs into various categories from the length data present on the page. And since the format of time is unique as \d:\d\d , little issues would arise with the regular expressions. Besides the regular expressions, the for loops should be able to remain as is and the plotting part of the program would only have to be minimally changed depending on the type of chart the user would like to plot.  
