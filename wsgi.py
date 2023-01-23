from main import app
from data_base import mysql_db

if __name__ == '__main__':
    mysql_db.db_start()
    app.run()