Greetings!

Before launching this app, we need to initialize our MySQL database.

I used Denwer for DB deployment. To initialize the database, you should run init_sql.py file, which also refers to sql.txt file to receive table data from it.
Please note that this initializing script refers to DB "by default" - to "localhost" as "root" user with no password. To initialize as user with password - variables DBCFG and SQLALCHEMY_DATABASE_URI in config.py file should be changed accordingly.

Check the requirements.txt before running the app:
>>> pip install -r requirements.txt

To run app use:
>>> flask run

Site will be launched on local sever 127.0.0.1:5000
Minimal frontend design has been created for testing and task-checking.