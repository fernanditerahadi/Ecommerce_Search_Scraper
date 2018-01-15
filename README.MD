== Tokopedia Search Scraper ==

This simple application will scrape the result of your search query from http://www.tokopedia.com,
extract the product information, and store them in a database file called 'Tokopedia.sqlite'.

You may need to install DB Browser for SQLite in your system to open the 'Tokopedia.sqlite'
file. DB Browser for SQLite (free) could be downloaded through the following link http://sqlitebrowser.org

== How to Run the Application ? ==  

1. Download all the files found in the 'Standalone Application (Windows)' folder and
  move them to a designated location in your system.
2. Execute tokoscrap.exe

Unfortunately, the standalone application will only work on Windows. For MAC OSX user,
please execute the 'tokoscrap.py' file found in the 'Source Code' folder using Python Shell
installed in your system. Please do note that once the program is executed,
it will create a “Tokopedia.sqlite” file in the same folder. To view the retrieved data,
please open the “Tokopedia.sqlite” file. To see the sample result and the
relational schema of the "Tokopedia.sqlite", please navigate to the
'Sample Result' folder.

List of retrieved information :
-Product id
-Product department id
-Product department name
-Product condition
-Product price
-Product discount percentage
-Product view count
-Product review count
-Product sold count
-Product successful transaction count
-Product reject count
-Product rating
-Product label
-Product badge
-Product url
-Store id
-Store name
-Store location
-Store url
-Store gold status

November 2017

