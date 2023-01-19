import pymysql
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


def db_start():
    try:
        global connection
        connection = pymysql.connect(
            host=DB_HOST,
            port=3306,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfuly connected...")

    except Exception as ex:
        print("Connection refused...")
        print(ex)


async def db_write_data(chat_id, prompt):
        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO `user` (`user_id`, `user_prompt`) VALUES (%s, %s)"
                cursor.execute(insert_query, (str(chat_id), str(prompt)))
                connection.commit()
                print("db commited")
        except Exception as ex:
            print("Connection refused...")
            print(ex)
