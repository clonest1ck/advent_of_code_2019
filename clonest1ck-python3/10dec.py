import math

asteroids = dict()
x = 0
y = 0

f = open("10dec-input2", 'r')
for line in f:
    x = 0
    for point in line:
        if point == "#":
            asteroids[(x, y)] = point
        x += 1
    y += 1

def getDeltas(center, point):
    (ax, ay) = center
    (sx, sy) = point

    dx = ax - sx
    dy = ay - sy

    x = dx
    y = dy

    if dx < 0:
        x = 0 - dx
    if dy < 0:
        y = 0 - dy

    multiple = math.gcd(x, y)
    dx = dx / multiple
    dy = dy / multiple

    return (dx, dy, multiple)

f.close()
visible = []
adjusted_location = dict()
for asteroid in asteroids:
    adjusted_location[asteroid] = []
    deltas = []
    for stone in asteroids:
        if stone == asteroid:
            continue

        (dx, dy, multiple) = getDeltas(asteroid, stone)
        if (dx, dy) not in deltas:
            deltas.append((dx, dy))
        adjusted_location[asteroid].append((dx, dy, multiple))
    visible.append((len(deltas), asteroid))

def getFirst(a):
    x, y = a
    return x

visible.sort(key=getFirst, reverse=True)
print("Part 1: %d" % visible[0][0])

locations = adjusted_location[visible[0][1]]
deltas = dict()
for loc in locations:
    (x, y, multiple) = loc
    if (x,y) not in deltas:
        deltas[(x, y)] = []
    deltas[(x, y)].append(multiple)

def pointsort(a):
    x, y = a
    x = float(x)
    y = float(y)
    if y != 0:
        return math.atan(x/y)
    if x > 0:
        return math.pi
    else:
        return 0
order = list(deltas.keys())
order.sort(key=pointsort, reverse=True)

start = order.index((0, 1))
count = 0
last_destroyed = (0,0,0)
while count < 200:
    delta = order[start]
    if len(deltas[delta]) != 0:
        closest = min(deltas[delta])
        deltas[delta].remove(closest)
        (x, y) = delta
        last_destroyed = (x, y, closest)
        (cx, cy) = visible[0][1]
        (dx, dy, m) = last_destroyed
        x = cx + (dx * m)
        y = cy + (dy * m)
        print("(%d, %d)" % (x, y))
        count += 1
    start += 1
    if not start < len(deltas):
        start = 0

(cx, cy) = visible[0][1]
(dx, dy, m) = last_destroyed
x = cx + (dx * m)
y = cy + (dy * m)
ret = 100 * x + y
print("(%d, %d)" % (x, y))
print("Part 2: %d" % ret)
