(In progress...)
A Library Web Application being written in Python, using Flask framework for the backend and SQLAlchemy to manage the underlying database. This is a home project, undertaken mainly in order to learn Python and Flask as a beginner, along with some Database magic in the mix. Currently it uses Author, Publisher and Book as main tables related to each other, and support for multiple Users will be added soon. It assumes a many to many relationship between Book and Author tables (an author can write many books and a book can have more than one co-authors), a many to many relationship between Author and Publisher tables (an author can publish via many publishers and a publisher publishes many authors) and a one to many relationship between Book and Publisher (on the basis of different ISBN number for the same title published from multiple publishers, hence while the title remains the same we have different records)

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

Also before you add a book title, you'll need to add the author if he/she is not already in the database. Same goes for publisher if you want to add a publisher to the title (not mandatory). 
An instance of a sample SQLite database with 700+ books, 70+ authors and 45+ publishers is provided, to get you started.
