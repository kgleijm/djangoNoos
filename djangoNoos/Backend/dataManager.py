import sqlite3
import random as r


noosPointTableCreationSql = "CREATE TABLE IF NOT EXISTS noospoints (" \
                            "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                            "plankId TEXT," \
                            "Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP," \
                            "product TEXT DEFAULT 'Undefined'," \
                            "rawSensorMatrix TEXT);"

plankTableCreationSql = "CREATE TABLE IF NOT EXISTS plankconfigurations (" \
                        "ID TEXT PRIMARY KEY," \
                        "IP TEXT," \
                        "product TEXT," \
                        "calibrationEmpty TEXT," \
                        "calibrationFull TEXT);"

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
        sql = f'INSERT INTO noospoints(plankId, product, rawSensorMatrix) VALUES(?,?,?)'
        self.cursor.execute(sql, (noosPointObject.deviceEUI, "Undefined", str(noosPointObject.getMatrix())))
        self.connection.commit()

    def addPlankIfUnknown(self, noosPointObject):

        # TODO update ip if needed

        sql = f"INSERT OR IGNORE INTO plankconfigurations (ID, IP, product, calibrationEmpty, calibrationFull) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (noosPointObject.deviceEUI, noosPointObject.ip, "Undefined", "[]", "[]"))
        self.connection.commit()

    def getPlanks(self):
        self.cursor.execute("SELECT * FROM plankconfigurations")

        rows = self.cursor.fetchall()

        for row in rows:
            print(row)

        return rows

    def getLatestSensorReadings(self):
        sql = """
        SELECT DISTINCT plankId, Max(Timestamp)
        FROM noospoints
        GROUP BY plankId
        ORDER BY plankId, Timestamp desc
        """

    def getIpByID(self, ID):
        sql = f"""
                SELECT DISTINCT ID, IP
                FROM plankconfigurations
                WHERE ID = "{ID}"
                """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            return row[1]
        return None

    def getAmountOfPointsByID(self, ID):
        sql = f"""SELECT COUNT(*)
                  FROM noospoints
                  WHERE plankId = "{ID}"
                  """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            # print("getAmountOfPointsByID", row[0])
            return row[0]
        return None










