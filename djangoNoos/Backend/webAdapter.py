import json
from threading import *
from socket import *




# The NoosAdapter is a threadWrapper responsible for listening on udp port 2311
# and passing generated NoosePoints objects to the database
# NoosPoints are collections of raw sensor data bound to a timestamp



# class representing data from Noosmessage
class NoosPoint:
    # init, turning raw json from noosplank to object
    def __init__(self, udpMessage):
        #print("Incoming:", udpMessage)

        self.ip = "None"
        self.deviceEUI = "None"
        self.sensorCount = 0
        self.matrix = [[]]
        self.sensorReadings = None

        try:
            self.ip = udpMessage[1][0]
            self.valueJson = json.loads(udpMessage[0].decode("utf-8"))
            self.deviceEUI = self.valueJson["msgDeviceEUI"]
            self.sensorCount = self.valueJson["msgSensorCount"]
            self.sensorReadings = self.valueJson["msgSensorReadings"]
        except:
            print("ERROR COULD NOT DECODE INCOMING UDP MESSAGE")

    def isValid(self):
        if self.sensorReadings is None:
            return False
        return True

    # hardcoded cleanup for testing purposes
    # def getCleanMatrix(self):
    #
    #     matrix = self.getMatrix()
    #
    #     for y in range(len(matrix)):
    #         for x in range(len(matrix[0])):
    #             # clamp values
    #             if matrix[y][x] < 30:
    #                 matrix[y][x] = 30
    #             if matrix[y][x] > 280:
    #                 matrix[y][x] = 280
    #     return matrix

    # return sensorvalues as 2d array

    def getMatrix(self):
        if self.sensorReadings is None:
            return[[]]
        raw = self.sensorReadings
        count = 0
        matrix = []
        rowList = []
        for reading in raw:
            # reverse row for actual data
            rowList.insert(0, reading)
            count += 1

            # split in bunches of eigth
            if count == 8:
                matrix.insert(0, rowList)
                count = 0
                rowList = []
        return matrix

    # get calibrated matrix based on calibration profile
    def getCalibratedMatrix(self, calibrationDict):
        pass
        # TODO write function

    # get sensors values as formatted string
    def getSensorValuesAsString(self):
        if self.sensorReadings is None:
            return ""
        raw = self.sensorReadings
        count = 0
        outp = ""
        row = ""
        for reading in raw:
            # reverse row for actual data
            row = f"{reading}," + row
            count += 1

            # split in bunches of eigth
            if count == 8:
                outp += row + "\n"
                count = 0
                row = ""
        return outp

    # get main informaition as human readable string
    def __str__(self):
        return f"Device: {self.deviceEUI}\nAt IP: {self.ip}\nReading {self.sensorCount} sensors\nRaw data:\n{self.getSensorValuesAsString()}\n"

# class wrapping Thread that listens for udp messages
class NoosAdapter(Thread):

    # Main loop on startup
    def run(self):
        print("Starting NoosAdapter.run()")
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.bind(('', 2311))


        # Mid file import to create manager on same thread as NoosAdapter loop
        from .dataManager import TSDataManager
        DataManager = TSDataManager()

        # keep listening
        while True:
            m = self.s.recvfrom(1024)
            n = NoosPoint(m)
            # print(n)

            if n.isValid():
                DataManager.insertNoosPoint(n)
                DataManager.addPlankIfUnknown(n)
            else:
                print("no valid point!")

    # initialization where thread gets started
    def __init__(self):
        super().__init__()
        self.start()
        print("noosAdapter INIT done")





