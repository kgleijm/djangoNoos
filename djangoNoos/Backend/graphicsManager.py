from PIL import Image, ImageDraw



class GraphicsManager:

    @staticmethod
    def SaveHeatMapFillGrade(matrix, name):
        # simplify matrix to sensor pairs
        simplifiedMatrix = [[0]*4]*5
        for y in range(len(matrix)):
            for x in range(0, len(matrix[0]), 2):
                # store average of sensor pair in designated location of simplified matrix
                simplifiedMatrix[y][int(x/2)] = int((matrix[y][x] + matrix[y][x+1])/2)
        for row in simplifiedMatrix:
            print(row)

        #start canvassing
        img = Image.new('RGB', (200, 250), color='white')
        d = ImageDraw.Draw(img)
        rect = [(10, 10), (10, 10)]
        d.rectangle(rect, fill="#b4ed9a", outline="black")



        img.save(name)

