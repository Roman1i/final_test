import animal
import counter


# Список параметров
def _help():
    print("-d  -  Display database")
    print("--add  -  Add new animal")
    print("--comshow 'id'  -  Show commands")
    print("--comset 'id'  -  Set new commands")
    print("--comadd 'id'  -  Add command")


# Вывод базы данных в консоль
def display_database(connection):
    with connection.cursor() as cursor:
        request = "SELECT * FROM union_table"
        cursor.execute(request)

        #columns = cursor.fetchone()
        #for name in columns:
        #    print(name, end=" ")

        rows = cursor.fetchall()
        for row in rows:
            for each in row:
                out = str(row.__getitem__(each))
                if each == 'Commands':
                    print(out + " " * (40 - len(out)), end=" ")
                else:
                    print(out + " " * (20 - len(out)), end=" ")

            print(" ")
        print("Selected...")


def add_new_animal(connection):
    with connection.cursor() as cursor:
        newanimal = animal.Animal()
        while newanimal.type is None:
            newanimal.type = choose_type(connection)
        while newanimal.animal is None:
            newanimal.animal = choose_animal(connection, newanimal.type)
        print("Введите имя:")
        newanimal.name = input()
        print("Введите список команд:")
        newanimal.comands = input()
        print("Введите дату YYYY-MM-DD:")
        newanimal.birthdate = input()

        request = "INSERT INTO `union_table` (`AnimalId`, `Animal`, `Name`, `Commands`, `BirthDate`) \
                   VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');".format\
                   (counter.Counter.add(connection), newanimal.animal, newanimal.name, newanimal.comands, newanimal.birthdate)
        cursor.execute(request)
        connection.commit()
        print("New data successfully added...")


# Меню выбора типа животного
def choose_type(connection):
    print("Выберите тип животного...")
    with connection.cursor() as cursor:
        request = "SELECT Type FROM `Животные`"
        cursor.execute(request)
        rows = cursor.fetchall()

        try:
            print("Введите номер из списка:")
            count = 0
            for row in rows:
                for element in row:
                    print("{0} - {1}".format(str(count+1), row.__getitem__(element)))
                    count += 1

            iters = int(input())
            while iters not in range(1, count + 1):
                print("Введите номер из списка!")
                iters = int(input())
            for i in range(iters):
                type = rows[i]
            return type['Type']
        except ValueError as er:
            print(er)
            pass


# Меню выбора животного
def choose_animal(connection, type):
    print("Выберите животное...")
    with connection.cursor() as cursor:
        request = "SELECT Animal FROM {0}".format(type)
        cursor.execute(request)
        rows = cursor.fetchall()

        try:
            print("Введите номер из списка:")
            count = 0
            animallist = []
            for row in rows:
                for element in row:
                    animal = str(row.__getitem__(element))
                    if animal not in animallist:
                        animallist.append(animal)
                        print("{0} - {1}".format(str(count + 1), animal))
                        count += 1

            iters = int(input())
            while iters not in range(1, count + 1):
                print("Введите номер из списка!")
                iters = int(input())
            for i in range(iters):
                anim = rows[i]
            return anim['Animal']
        except ValueError:
            # choose_animal(connection, type)
            pass


# Просмотр команд по AnimalId
def show_commands(connection, id):
    with connection.cursor() as cursor:
        request = "SELECT Commands FROM union_table WHERE AnimalId = {0}".format(id)
        cursor.execute(request)
        row = cursor.fetchone()
        print(row['Commands'])


# Пополнение списка крманд по id
def set_commands(connection, id):
    with connection.cursor() as cursor:
        print('Введите новые команды...')
        newCommands = input()
        request = "UPDATE `union_table` SET Commands='{0}' WHERE AnimalId = {1}".format(newCommands, id)
        cursor.execute(request)
        connection.commit()
        print('New commands has been set...')


# Добавление новых команд по id
def add_commands(connection, id):
    with connection.cursor() as cursor:
        selection = "SELECT Commands FROM union_table WHERE AnimalId = {0}".format(id)
        cursor.execute(selection)
        row = cursor.fetchone()
        commands = row['Commands']
        print("Текущий список команд: {0}".format(commands))
        print('Введите команды, который хотите добавить...')
        newCommands = input()
        request = "UPDATE `union_table` SET Commands='{0} {1} ' WHERE AnimalId = {2}".format(commands, newCommands, id)
        cursor.execute(request)
        connection.commit()
        print('Commands has been added...')
