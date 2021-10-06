import sqlite3
import random as r
# from webAdapter import *


noosPointTableCreationSql = "CREATE TABLE IF NOT EXISTS noospoints (" \
                            "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                            "plankId TEXT," \
                            "Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP," \
                            "product TEXT DEFAULT 'Undefined'," \
                            "fillgrade TEXT," \
                            "calibrationjson TEXT," \
                            "rawSensorMatrix TEXT);"

plankTableCreationSql = "CREATE TABLE IF NOT EXISTS plankconfigurations (" \
                        "ID TEXT PRIMARY KEY," \
                        "product TEXT," \
                        "calibrationjson TEXT);"

con = sqlite3.connect('NoosData.db')
cur = con.cursor()

# execute necessary statements
cur.execute(noosPointTableCreationSql)
cur.execute(plankTableCreationSql)

# Thread Safe Datamanager
class TSDataManager:

    def __init__(self):
        self.connection = sqlite3.connect('NoosData.db')
        self.cursor = self.connection.cursor()

    def insertNoosPoint(self, noosPointObject):
        sql = f'INSERT INTO noospoints(plankId, product, fillgrade, calibrationjson, rawSensorMatrix) VALUES(?,?,?,?,?)'
        self.cursor.execute(sql, (noosPointObject.deviceEUI, "Undefined", f"[{int(r.random() * 100)},{int(r.random() * 100)}]", "None", str(noosPointObject.getMatrix())))
        self.connection.commit()

    def addPlankIfUnknown(self, noosPointObject):
        sql = f"INSERT OR IGNORE INTO plankconfigurations (ID, product, calibrationjson) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (noosPointObject.deviceEUI, "Undefined", "Undefined"))
        self.connection.commit()

    def getPlanks(self):
        self.cursor.execute("SELECT * FROM tasks")

        rows = self.cursor.fetchall()

        for row in rows:
            print(row)



# class DataManager:
#
#     @staticmethod
#     def insertNoosPoint(noosPointObject):
#         print("ID in dataManager insert:", get_ident())
#         sql = f'INSERT INTO noospoints(plankId, product, fillgrade, calibrationjson, rawSensorMatrix) VALUES(?,?,?,?,?)'
#         cur.execute(sql, (noosPointObject.deviceEUI, "Undefined", f"[{int(r.random() * 100)},{int(r.random() * 100)}]", "None", str(noosPointObject.getMatrix())))
#         con.commit()
#
#     @staticmethod
#     def addPlankIfUnknown(noosPointObject):
#         sql = f"INSERT OR IGNORE INTO plankconfigurations (ID, product, calibrationjson) VALUES (?, ?, ?)"
#         cur.execute(sql, (noosPointObject.deviceEUI, "Undefined", "Undefined"))
#         con.commit()




# if __name__ == '__main__':
#
#
#     # insert statement
#     for i in range(100):
#         sql = f'INSERT INTO noospoints(plankId, product, fillgrade, calibrationjson) VALUES(?,?,?,?)'
#         cur.execute(sql, ("TestID", "TestProduct", int(r.random()*100), "None"))
#         con.commit()








