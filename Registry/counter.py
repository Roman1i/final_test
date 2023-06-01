class Counter:

    @classmethod
    def add(cls, connection):
        return max(cls.ids(connection)) + 1

    @classmethod
    def id_exists(cls, connection, id):
        if id in Counter.ids(connection):
            return True
        else:
            raise Exception("There`s no such id as '{0}'...".format(id))

    @classmethod
    def ids(cls, connection):
        with connection.cursor() as cursor:
            request = "SELECT AnimalId FROM union_table"
            cursor.execute(request)
            rows = cursor.fetchall()
            ids = []
            for id in rows:
                ids.append(id['AnimalId'])
            return ids



