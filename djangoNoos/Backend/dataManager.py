import copy
import json
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

    def updateIPifNeeded(self, noosPointObject):
        sql = f"""
            UPDATE plankconfigurations
            SET IP = '{noosPointObject.ip}'
            WHERE ID = '{noosPointObject.deviceEUI}'
        """

    def addPlankIfUnknown(self, noosPointObject):
        sql = f"INSERT OR IGNORE INTO plankconfigurations (ID, IP, product, calibrationEmpty, calibrationFull) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (noosPointObject.deviceEUI, noosPointObject.ip, "Undefined", "[]", "[]"))
        self.connection.commit()

    def getPlanks(self):
        self.cursor.execute("SELECT ID FROM plankconfigurations")
        rows = self.cursor.fetchall()
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

    def getLastNMatricesByID(self, n, ID):
        sql = f"""
            SELECT rawSensorMatrix, "Timestamp" as t FROM noospoints
            WHERE plankId = '{ID}'
            ORDER BY t DESC 
            LIMIT {n}
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        output = []
        for row in rows:
            # print(row[0][:30], " ||| ", row[1])
            rowAsString = row[0]
            aslist = json.loads(rowAsString)
            output.append(aslist)

        return output

    def getEmptyCalibrationMatrix(self, ID):
        sql = f"""
                    SELECT calibrationEmpty FROM plankconfigurations
                    WHERE ID = '{ID}'
                """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        try:
            return json.loads(str(rows[0][0]))
        except:
            return None

    def getFullCalibrationMatrix(self, ID):
        sql = f"""
                    SELECT calibrationFull FROM plankconfigurations
                    WHERE ID = '{ID}'
                """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        try:
            return json.loads(str(rows[0][0]))
        except:
            return None

    def setEmptyCalibrationForID(self, matrix, ID):
        sql = f"""
            UPDATE plankconfigurations
            SET calibrationEmpty = '{str(matrix)}'
            WHERE ID = '{ID}'
        """
        self.cursor.execute(sql)
        self.connection.commit()

    def setFullCalibrationForID(self, matrix, ID):
        sql = f"""
            UPDATE plankconfigurations
            SET calibrationFull = '{str(matrix)}'
            WHERE ID = '{ID}'
                """
        self.cursor.execute(sql)
        self.connection.commit()

    def getMatrixAsPercentagesFromID(self, ID):
        fullCalibrationMatrix = self.getFullCalibrationMatrix(ID)
        emptyCalibrationMatrix = self.getEmptyCalibrationMatrix(ID)
        targetMatrix = self.getLastNMatricesByID(1, ID)[0]

        percentageMatrix = copy.deepcopy(fullCalibrationMatrix)
        for y in range(len(fullCalibrationMatrix)):
            for x in range(len(fullCalibrationMatrix[0])):
                # calculate percentage from lasts sensor reading against calibration values
                calibrationDifference = abs(fullCalibrationMatrix[y][x] - emptyCalibrationMatrix[y][x])
                targetDifference = targetMatrix[y][x] - emptyCalibrationMatrix[y][x]
                absolutePercentage = int(abs((targetDifference/(calibrationDifference+0.1)) * 100))  # calculate percentage and clean up to int
                percentageMatrix[y][x] = max(min(absolutePercentage, 100), 0)  # clamp percentage
        return percentageMatrix


        #print("Percentage: ", percentageMatrix)


