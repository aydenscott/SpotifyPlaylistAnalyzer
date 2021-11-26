# SpotifyPlaylistTimeline
Python program that scrapes http://sortyourmusic.playlistmachinery.com/ and collects:
* Timeline histogram of the songs in the selected playlist
* Pie chart of length data from songs
* Prints the 10 most common artists in your playlists along with their occurance rate 

## Usage
In order to use this program, simply input your login details in to secrets.py (Spotify username and password). The main file pulls from secrets when it logs in.

## How It Works
This program relies on http://sortyourmusic.playlistmachinery.com/ which does most of the heavy lifting by finding all of the release dates of songs and putting them in a single table. On the program's side, it uses selenium and regular expressions to scrape the data. The main umbrella comes from finding all of the tags with 'td' and sorting through them. Since dates appear on each row in the same position, the program is able to have a for loop with an increment of 13 that spans all of the tags. This loop appends to a temporary list which will need to be cut by using regular expressions. This is because the website displays data in three forms: yyyy, yyyy-mm, and yyyy-mm-dd. To ensure that the plot can read it all, I decided to make all dates into the form yyyy which can easily be done by cutting the string(:4). Once this new list is created from the cut date formats, the program used matplotlib to make a histogram of the data which is displayed to the user and can be saved within matplotlib's GUI. 

Length and artist data piggyback heavily off of what was previously done to find the dates of the songs. The only major difference is that in the for loops the starting index (named first_hit) is different but still increments by 13. There are also some other differences, such as that the artist data utilizes the Collections library to count the artist occurance rate. Finally, the length data has a unique for loop that groups the length data into separate categories which will be needed for the pie chart. 

## Possible Improvements
* ~~Automatically finding the playlist length when given the name of the playlist (since the information is listed side by side but by inputing the playlist name, selenium is finding it by link text not by xpath. Therefore, I've been unable to find a concise way of taking the element found by link text and converting it to xpath whereby you can find the sibling element)~~
* Improving the Tkinter dropdown menu. It gets the job done by allowing the user to pick the playlist, closes itself, and feeds the choice into playlist_name which is used later in the program. However, it is quite unsightly so more work could be done in beautifying it for user readability.
* Get selenium headless mode to work without lists coming back empty.

## Future Uses
~~By changing the regular expressions, the program could quickly be changed to search for other types of data present on the page. For example, a pie chart could be created that sorts the length of the songs into various categories from the length data present on the page. And since the format of time is unique as \d:\d\d , little issues would arise with the regular expressions. Besides the regular expressions, the for loops should be able to remain as is and the plotting part of the program would only have to be minimally changed depending on the type of chart the user would like to plot~~.
