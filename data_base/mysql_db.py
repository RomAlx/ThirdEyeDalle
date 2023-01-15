import pymysql
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


def db_start():
    try:
        global connection
        connection = pymysql.connect(
            host=DB_HOST,
            port=3306,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfuly connected...")

    except Exception as ex:
        print("Connection refused...")
        print(ex)


async def db_write_data(message):

        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO `user` (`user_id`, `user_prompt`) VALUES (%s, %s)"
                cursor.execute(insert_query, (str(message.chat.id), str(message.text)))
                connection.commit()
                print("db commited")
        except Exception as ex:
            print("Connection refused...")
            print(ex)
