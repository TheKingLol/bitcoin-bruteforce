# Database FAQ
Before we start, this part of the repository is made possible thanks to @Isaacdelly.
This database is a collection of text files containing all funded Bitcoin addresses downloaded from http://addresses.loyce.club/

The name of the text file is the date when the database was last updated in month_day_year format. The file will be updated every 3-6 months.

### How Many Addresses Does The Database Have?

The database currently holds `43,212,954 Bitcoin addresses`. This is the total number of Bitcoin addresses with a balance that exist in the blockchain at the time of uploading.

### Why Are There So Many Files?

There are multiple files because GitHub limits file uploads to 50 MB. The single file is too large, so it was split into multiple files each under 50 MB in order to be uploaded to GitHub.

### How to update database for myself?

There will come a time where I will discard this project for x reason or y reason.
If you want to update the database you will have to follow these instructions.

1. Clone this repo
2. Go to http://addresses.loyce.club/ and look on the right hand side for
- List of all funded Bitcoin addresses
(balance not shown, sorted in alphabetical order)
And download the latest
3. Go to database/latest, delete everything and replace it with your newly downloaded txt file from the website above
4. You're all done!

### How to update database for others too?
1. Fork and clone this repo
2. Clone this repo https://github.com/TheKingLol/python-file-splitter.git
3. Go to http://addresses.loyce.club/ and look on the right hand side for
- List of all funded Bitcoin addresses
(balance not shown, sorted in alphabetical order)
And download it
4. Put it in python file splitter and split it up to a maximum of 45mb each (For Github)
5. Go in the output file and copy all the files.
6. Go to database/latest and replace all the text files
7. Perform git push origin or use github desktop
