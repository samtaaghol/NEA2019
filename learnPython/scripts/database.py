import pymysql


class Database():

    """
    General database class works for multiple databases and databases with multiple tables.

    Assumes when a row is inserted every column will receive a new value.
    """

    def __init__(self, host, user, password, db, charset, cursorclass, primary_key = "username"):

        self.table_columns = []

        self.connection = pymysql.connect(host = host,
                                     user = user,
                                     password = password,
                                     db = db,
                                     charset = charset,
                                     cursorclass = cursorclass)

        self.primary_key = primary_key

    def setTable(self, table):

        self.table_columns = []

        try:
            with self.connection.cursor() as cursor:

                cursor.execute("SHOW columns FROM " + table)

                for dictionary in cursor.fetchall():

                    self.table_columns.append(dictionary['Field'])
        except:
            print("incorrect table name.")

    def insertRow(self, table, *args):

        self.setTable(table)

        if len(args) != len(self.table_columns):
            return False

        try:
            with self.connection.cursor() as cursor:

                sql = "INSERT INTO `" + table + "`("

                for column in self.table_columns:

                    sql += "`" + column + "`,"

                sql = sql[:-1] + ") VALUES ("

                for column in self.table_columns:

                    sql += "%s,"

                sql = sql[:-1] + ")"

                print(sql)

                cursor.execute(sql, args)

            self.connection.commit()

        except pymysql.err.IntegrityError:
            print('Wrong')

    def getDetails(self, table, key_value):

        self.setTable(table)

        try:
            with self.connection.cursor() as cursor:

                columns_to_return = ""

                for column in self.table_columns:

                    if column != self.primary_key:

                        columns_to_return += "`" + column + "`,"

                sql = "SELECT " + columns_to_return[:-1] + " FROM `" + table + "` WHERE `" + self.primary_key + "` = '" + key_value + "'"

                cursor.execute(sql)

                details = []

                return cursor.fetchone()

            self.connection.commit()

        except pymysql.err.IntegrityError:

            print('Wrong')

    def increment(self, table, key):

        try:
            with self.connection.cursor() as cursor:

                print("key : " + key)

                sql = "UPDATE " + table + " SET score = score + 1 WHERE username = '" + key + "'"

                print(sql)

                cursor.execute(sql)

                self.connection.commit()


        except pymysql.err.IntegrityError:

            print('Wrong')

    def custom_query(self, sql):

        try:
            with self.connection.cursor() as cursor:

                cursor.execute(sql)

                self.connection.commit()

                return cursor.fetchall()


        except pymysql.err.IntegrityError:

            print('Wrong')