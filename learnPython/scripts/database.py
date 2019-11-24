import pymysql

class Database():
    def __init__(self,host,user,password,db,charset,cursorclass):

        self.connection = pymysql.connect(host = host,
                                     user = user,
                                     password = password,
                                     db = db,
                                     charset = charset,
                                     cursorclass = cursorclass)

    def insertRow(self,username,passwordHash,email,salt):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`usernames`,`passwords`,`emails`,`salt`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (username, passwordHash, email, salt))

            self.connection.commit()
        except pymysql.err.IntegrityError:
            print('Wrong')

    def deleteRow(self,email):

        try:
            with self.connection.cursor() as cursor:

                sql = "DELETE FROM `users` WHERE `emails` = " + email + ";"
                cursor.execute(sql)
            self.connection.commit()

        except pymysql.err.IntegrityError:
            print('Wrong')

    def getDetails(self,username):
        try:
            with self.connection.cursor() as cursor:

                sql = "SELECT `passwords` FROM `users` WHERE `usernames` = %s "
                cursor.execute(sql, username)
                for row in cursor:
                    #print(row['passwords'])
                    passwordHash = row['passwords']
                sql = "SELECT `salt` FROM `users` WHERE `usernames` = %s "
                cursor.execute(sql, username)
                for row in cursor:
                    salt = row['salt']
                try:
                    return passwordHash, salt

                except UnboundLocalError:

                    return False


            self.connection.commit()

        except pymysql.err.IntegrityError:
            print('Wrong')

#username = 'samtaaghol'
#password = 'password123'
#email = "staaghol123@hotmail123.com"
#emailQuery = "'staaghol123@hotmail123.com'"
#usernameQuery = "'samtaaghol'"

db = Database('localhost','root','rootpassword','database','utf8mb4', pymysql.cursors.DictCursor)
usernameQuery = "taaghols"
#db.insertRow(passwords,usernames,emails)
#db.deleteRow(emailQuery)
#db.getDetails(usernameQuery)