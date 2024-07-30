A Library Web Application written in Python.
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

