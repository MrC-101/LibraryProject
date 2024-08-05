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
An instance of a sample SQLite database with almost 700 books, 70+ authors and 45+ publishers is provided, to get you started.

Some screenshots
![2024-08-05_123530](https://github.com/user-attachments/assets/2a1f3ea7-9a62-457f-9392-3e6fdc19023e)

![2024-08-05_123716](https://github.com/user-attachments/assets/ef0de9d2-63cc-4f97-9078-bc68953d9570)

![355055332-1d389ced-0e4b-4d12-a13b-ff8dc369b998](https://github.com/user-attachments/assets/891312a3-7ae2-4d3e-a49f-a91af9183bcc)

![2024-08-05_123449](https://github.com/user-attachments/assets/4538a653-7aaa-4d24-b833-8d83123ce3bc)

![2024-08-05_123400](https://github.com/user-attachments/assets/a0b1c325-f33e-46ca-956b-0053c8c2abf0)
