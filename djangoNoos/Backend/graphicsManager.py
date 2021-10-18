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
        heatmapcolors = ["#6FEB6F", "#B0F2B4", "#FFE15C", "#DE6C3F", "#BC412B"]
        img = Image.new('RGB', (201, 251), color='white')
        d = ImageDraw.Draw(img)

        for y in range(5):
            for x in range(4):
                text = f"{simplifiedMatrix[y][x]}%"
                twentyPercentile = min(abs(5-(simplifiedMatrix[y][x]+10)//20),4)

                rect = [(x*50, y*50), ((x+1)*50, (y+1)*50)]
                d.rectangle(rect, fill=heatmapcolors[twentyPercentile], outline="black")
                d.text((x*50+18, y*50+20), text, fill="#000000")



        img.save(name)

