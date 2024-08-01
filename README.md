(In progress...)
A Library Web Application written in Python. It assumes a many to many relationship between Book and Author tables, 
a many to many relationship between Author and Publisher tables and a one to many relationship between Book and 
Publisher (on the basis of different ISBN number for the same title published from multiple publishers, hence while 
the title remains the same we have different records)

To use the application you will need to create a .env file in the root directory where the .flaskenv file is too. 
In that .env file you will store your DATABASE_URL and your APP_SECRET_KEY variables.

<code>example for Postgresql
DATABASE_URL='postgresql://user:password@localhost:5432/library_db'
APP_SECR_KEY="tUBswo%s3!Vp#ux$dX#BQKCtPi9HtNviZngCmkroB9YAVqNjm5pyV"</code>

<code>example for MySQL
DATABASE_URL = 'mysql+pymysql://user:password@localhost:3306/library_db'
APP_SECR_KEY="tUBswo%s3!Vp#ux$dX#BQKCtPi9HtNviZngCmkroB9YAVqNjm5pyV"</code>

<code>example for SQLite
DATABASE_URL = 'sqlite:///library_db'
APP_SECR_KEY="tUBswo%s3!Vp#ux$dX#BQKCtPi9HtNviZngCmkroB9YAVqNjm5pyV"</code>

