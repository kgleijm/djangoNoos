from PIL import Image, ImageDraw



class GraphicsManager:

    @staticmethod
    def SaveOffsetHeatmap(matrix, name):
        # start canvassing
        imageH = 50*len(matrix) +1
        imageW = 50*len(matrix[0]) +1
        heatmapcolors = ["#6FEB6F", "#B0F2B4", "#FFE15C", "#DE6C3F", "#BC412B"]
        img = Image.new('RGB', (imageW, imageH), color='white')
        d = ImageDraw.Draw(img)

        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                text = f"{matrix[y][x]}%"
                twentyPercentile = min(abs(5 - (matrix[y][x] + 10) // 20), 4)

                rect = [(x * 50, y * 50), ((x + 1) * 50, (y + 1) * 50)]
                if matrix[y][x] == -1:
                    d.rectangle(rect, fill="lightgray", outline="black")
                    d.text((x * 50 + 18, y * 50 + 20), "-%", fill="#000000")
                else:
                    d.rectangle(rect, fill=heatmapcolors[twentyPercentile], outline="black")
                    d.text((x * 50 + 18, y * 50 + 20), text, fill="#000000")

        img.save(name)

    @staticmethod
    def SaveHeatMapFillGrade(matrix, name):
        # simplify matrix to sensor pairs
        simplifiedMatrix = []

        # print("simplifiedMatrix before calculations")
        # for row in simplifiedMatrix:
        #     print(row)
        # print("\n")

        for y in range(len(matrix)):
            ls = []
            for x in range(0, len(matrix[0]), 2):
                # store average of sensor pair in designated location of simplified matrix
                # print(f"Location: x{int(x//2)}:y{y} = {int((matrix[y][x] + matrix[y][x+1])/2)}")
                average = int((matrix[y][x] + matrix[y][x+1])/2)
                ls.append(average)
            simplifiedMatrix.append(ls)

            print(f"simplifiedMatrix at iteration y:{y}")
            for row in simplifiedMatrix:
                print(row)
            print("\n")


        print("simplifiedMatrix after calculations")
        for row in simplifiedMatrix:
            print(row)
        print("\n")

        #start canvassing
        heatmapcolors = ["#6FEB6F", "#B0F2B4", "#FFE15C", "#DE6C3F", "#BC412B"]
        img = Image.new('RGB', (201, 251), color='white')
        d = ImageDraw.Draw(img)

        for y in range(5):
            for x in range(4):
                text = f"{simplifiedMatrix[y][x]}%"
                twentyPercentile = min(abs(5-(simplifiedMatrix[y][x]+10)//20), 4)

                rect = [(x*50, y*50), ((x+1)*50, (y+1)*50)]
                d.rectangle(rect, fill=heatmapcolors[twentyPercentile], outline="black")
                d.text((x*50+18, y*50+20), text, fill="#000000")



        img.save(name)

