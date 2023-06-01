import sys
import pymysql
import options
import counter

# Подключение к базе данных
try:
    mysql = pymysql.connect(
        host="localhost",
        port=3306,
        user="admin",
        password="admin",
        database="Домашние животные",
        cursorclass=pymysql.cursors.DictCursor
    )

    print("Successfully connected...")
    print("#" * 100)

    try:
        params = sys.argv  # Список входных параметров
        if len(params) == 1:
            options._help()
        if "--add" in params:
            options.add_new_animal(mysql)

        try:
            if "--comshow" or "--comset" or "--comadd" in params:

                if "--comshow" in params:
                    animalId = int(params[params.index("--comshow") + 1])
                    if counter.Counter.id_exists(mysql, animalId):
                        options.show_commands(mysql, animalId)

                if "--comset" in params:
                    animalId = int(params[params.index("--comset") + 1])
                    if counter.Counter.id_exists(mysql, animalId):
                        options.set_commands(mysql, animalId)

                if "--comadd" in params:
                    animalId = int(params[params.index("--comadd") + 1])
                    if counter.Counter.id_exists(mysql, animalId):
                        options.add_commands(mysql, animalId)
        except ValueError as er:
            print("Id must be int type...")

        if "-d" in params:
            options.display_database(mysql)

    finally:
        mysql.close()
except Exception as ex:
    print("Connection refused...")
    print(ex)
