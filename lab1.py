from PIL import Image
import sys
import minQueue
import graph

speed = {
    "#F89412": 0.95,  # Open land
    "#FFC000": 0.5,  # Rough meadow
    "#FFFFFF": 0.8,  # Easy movement forest
    "#02D03C": 0.65,  # Slow run forest
    "#028828": 0.5,  # Walk forest
    "#054918": 0,  # Impassible vegetation
    "#0000FF": 0.33,  # Lake/Swamp/Marsh
    "#473303": 1,  # Paved road
    "#000000": 0.9,  # Footpath
    "#CD0065": 0  # Out of bounds
}


base_human_speed = 3
terrain_image = sys.argv[1]
elevation_file = sys.argv[2]
path_file = sys.argv[3]
season = sys.argv[4]
output_image_filename = sys.argv[5]


def convertRGBtoHex(r, g, b):
    return "#{}{}{}".format(hex(r).lstrip("0x").zfill(2), hex(g).lstrip("0x").zfill(2), hex(b).lstrip("0x").zfill(2))


def convertHextoRGB(c):
    c = c.lstrip("#")
    i = 0
    colour_array = []
    while i < 6:
        colour_array.append(int(c[i:i + 2], 16))
        i = i + 2
    return tuple(colour_array)


def distance(x1, y1, x2, y2):
    return (((x1 - x2) * 10.29) ** 2 + ((y1 - y2) * 7.55) ** 2 + (elevation[x1][y1] - elevation[x2][y2]) ** 2) ** 0.5


def time(x1, y1, x2, y2, destinationX, destinationY):
    #Calculating the total distance using Euclidean formula and dividing be speed to get time taken on that path.
    if speed[pixelHexColour[x1][y1].upper()] == 0:
        return "cant walk"
    if elevation[x1][y1] - elevation[x2][y2] > 0:
        return ((((x1 - x2) * 10.29) ** 2 + ((y1 - y2) * 7.55) ** 2 + (
                    elevation[x1][y1] - elevation[x2][y2]) ** 3) ** 0.5
                + (((x2 - destinationX) * 10.29) ** 2 + ((y2 - destinationY) * 7.55) ** 2 +
                   (elevation[x2][y2] - elevation[destinationX][destinationY]) ** 2) ** 0.5) / (
                           speed[pixelHexColour[x1][y1].upper()] * base_human_speed)

    return ((((x1 - x2) * 10.29) ** 2 + ((y1 - y2) * 7.55) ** 2 + (elevation[x1][y1] - elevation[x2][y2]) ** 2) ** 0.5
            + (((x2 - destinationX) * 10.29) ** 2 + ((y2 - destinationY) * 7.55) ** 2 +
            (elevation[x2][y2] - elevation[destinationX][destinationY]) ** 2) ** 0.5) / (speed[pixelHexColour[x1][y1].upper()] * base_human_speed)


def insertElementToQueue(x, y, x1, y1, destinationX, destinationY, visited, queue):
    if (x, y) in visited:
        return
    d = time(x1, y1, x, y, destinationX, destinationY)
    if d == "cant walk":
        return
    queue.insert((x, y), (x1, y1), d)


def adjacent_land(x, y, X, Y, pixel_colour):
    if (x + 1 < X and pixel_colour[x + 1][y].upper() != "#0000FF" and pixel_colour[x + 1][y].upper() != "#A5F2F3") or \
            (x + 1 < X and y - 1 >= 0 and pixel_colour[x + 1][y - 1].upper() != "#0000FF" and pixel_colour[x + 1][y - 1].upper() != "#A5F2F3") or \
            (x + 1 < X and y + 1 < Y and pixel_colour[x + 1][y + 1].upper() != "#0000FF" and pixel_colour[x + 1][y + 1].upper() != "#A5F2F3") or \
            (y - 1 >= 0 and pixel_colour[x][y - 1].upper() != "#0000FF" and pixel_colour[x][y - 1].upper() != "#A5F2F3") or \
            (y + 1 < Y and pixel_colour[x][y + 1].upper() != "#0000FF" and pixel_colour[x][y + 1].upper() != "#A5F2F3") or \
            (x - 1 >= 0 and pixel_colour[x - 1][y].upper() != "#0000FF" and pixel_colour[x - 1][y].upper() != "#A5F2F3") or \
            (x - 1 >= 0 and y + 1 < Y and pixel_colour[x - 1][y + 1].upper() != "#0000FF" and pixel_colour[x - 1][y + 1].upper() != "#A5F2F3") or \
            (x - 1 >= 0 and y - 1 >= 0 and pixel_colour[x - 1][y - 1].upper() != "#0000FF" and pixel_colour[x - 1][y - 1].upper() != "#A5F2F3"):
        return True
    return False


def convert_water_to_ice(x, y, X, Y, img, pixel_colour):
    x1 = x - 6 if x - 6 >= 0 else 0
    x2 = x + 6 if x + 6 < X else X - 1
    y1 = y - 6 if y - 6 >= 0 else 0
    y2 = y + 6 if y + 6 < Y else Y - 1
    yt = y1
    while x1 <= x2:
        y1 = yt
        while y1 <= y2:
            if pixel_colour[x1][y1].upper() == "#0000FF":
                img.putpixel((x1, y1), convertHextoRGB("#A5F2F3"))
                pixelHexColour[x1][y1] = "#A5F2F3"
            y1 = y1 + 1
        x1 = x1 + 1


def convert_land_to_mud(x, y, X, Y, img, pixel_colour):
    x1 = x - 15 if x - 15 >= 0 else 0
    x2 = x + 15 if x + 15 < X else X - 1
    y1 = y - 15 if y - 15 >= 0 else 0
    y2 = y + 15 if y + 15 < Y else Y - 1
    yt = y1
    while x1 <= x2:
        y1 = yt
        while y1 <= y2:
            if pixel_colour[x1][y1].upper() != "#0000FF" and elevation[y1][x1] - elevation[y][x] < 1:
                # pixelAccessImage[x1, y1] = convertHextoRGB("#A9844F")
                img.putpixel((x1, y1), convertHextoRGB("#A9844F"))
                pixelHexColour[x1][y1] = "#A9844F"
            y1 = y1 + 1
        x1 = x1 + 1


elevation = []
with open(elevation_file) as f:
    for line in f.readlines():
        arr = line.split()
        arr = arr[:395]
        arr = list(map(float, arr))
        elevation.append(arr)

img = Image.open(terrain_image)

pixelAccessImage = img.load()

X, Y = img.size
pixelHexColour = []
for x in range(X):
    temp = []
    for y in range(Y):
        r, g, b, a = pixelAccessImage[x, y]
        temp.append(convertRGBtoHex(r, g, b))
    pixelHexColour.append(temp)


if season.lower() == "fall":
    speed["#FFFFFF"] = 0.65

if season.lower() == "winter":
    for x in range(X):
        for y in range(Y):
            if ((pixelHexColour[x][y].upper() == "#0000FF") or pixelHexColour[x][y].upper() == "#A5F2F3")\
                    and adjacent_land(x, y, X, Y, pixelHexColour):
                convert_water_to_ice(x, y, X, Y, img, pixelHexColour)
    speed["#A5F2F3"] = 0.8

if season.lower() == "spring":
    for x in range(X):
        for y in range(Y):
            if (pixelHexColour[x][y].upper() == "#0000FF") \
                    and adjacent_land(x, y, X, Y, pixelHexColour):
                convert_land_to_mud(x, y, X, Y, img, pixelHexColour)
    speed["#A9844F"] = 0.6


# img.save(output_image_filename)
# sys.exit()


path = []
with open(path_file) as f:
    for line in f.readlines():
        arr = list(map(int, line.split()))
        path.append(arr)

i = 1

g = graph.Graph()
dist = 0
while i < len(path):
    visited = set()
    min_queue = minQueue.MinQueue()
    g = graph.Graph()
    startX, startY = path[i - 1]
    tempX, tempY = startX, startY
    destinationX, destinationY = path[i]
    while tempX != destinationX or tempY != destinationY:
        if (tempX, tempY) in visited:
            tempX, tempY, previousTempX, previousTempY = min_queue.pop()
            g.add_edge((tempX, tempY), (previousTempX, previousTempY))
            continue
        if tempX - 1 >= 0:
            insertElementToQueue(tempX - 1, tempY, tempX, tempY, destinationX, destinationY, visited, min_queue)
            if tempY - 1 >= 0:
                insertElementToQueue(tempX - 1, tempY - 1, tempX, tempY, destinationX, destinationY, visited, min_queue)
            if tempY + 1 < Y:
                insertElementToQueue(tempX - 1, tempY + 1, tempX, tempY, destinationX, destinationY, visited, min_queue)
        if tempX + 1 <= X:
            insertElementToQueue(tempX + 1, tempY, tempX, tempY, destinationX, destinationY, visited, min_queue)
            if tempY - 1 >= 0:
                insertElementToQueue(tempX + 1, tempY - 1, tempX, tempY, destinationX, destinationY, visited, min_queue)
            if tempY + 1 < Y:
                insertElementToQueue(tempX + 1, tempY + 1, tempX, tempY, destinationX, destinationY, visited, min_queue)
        if tempY - 1 >= 0:
            insertElementToQueue(tempX, tempY - 1, tempX, tempY, destinationX, destinationY, visited, min_queue)
        if tempY + 1 < Y:
            insertElementToQueue(tempX, tempY + 1, tempX, tempY, destinationX, destinationY, visited, min_queue)
        visited.add((tempX, tempY))
        tempX, tempY, previousTempX, previousTempY = min_queue.pop()
        g.add_edge((tempX, tempY), (previousTempX, previousTempY))
    start = g.get_node((startX, startY)).get_name()
    end = g.get_node((destinationX, destinationY))
    while end.get_name() != start:
        img.putpixel(end.get_name(), (255, 0, 0))
        previous_end = end
        end = end.get_connected_node()
        x1, y1 = previous_end.get_name()
        x2, y2 = end.get_name()
        dist = dist + distance(x1, y1, x2, y2)
    i = i + 1

print("Total distance travelled is : {}".format(dist))
img.save(output_image_filename)
img.show()
