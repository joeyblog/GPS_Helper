import subprocess
import math

def teleport(lat, lon):
    print(f"teleport to {lat}, {lon}")
    cmd = f"adb shell am start-foreground-service -a theappninjas.gpsjoystick.TELEPORT --ef lat {lat} --ef lng {lon}"
    subprocess.run(cmd, shell=True)  

#coord : "34.665713,135.519930"
def parse(coord):
    coord = coord.split(",")
    lat = coord[0]
    lon = coord[1]
    return lat, lon

EARTH_RADIUS = 6371000

def calc_distance(lat1, lon1, lat2, lon2):
    #convert to rad
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))

    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c

    return distance

def calculate_cooldown(distance_km):
    if distance_km <= 1:
        return 1
    elif distance_km <= 2:
        return 2
    elif distance_km <= 4:
        return 4
    elif distance_km <= 10:
        return 8
    elif distance_km <= 12:
        return 9
    elif distance_km <= 15:
        return 11
    elif distance_km <= 20:
        return 13
    elif distance_km <= 25:
        return 15
    elif distance_km <= 30:
        return 18
    elif distance_km <= 40:
        return 22
    elif distance_km <= 45:
        return 23
    elif distance_km <= 60:
        return 25
    elif distance_km <= 80:
        return 27
    elif distance_km <= 100:
        return 30
    elif distance_km <= 125:
        return 33
    elif distance_km <= 140:
        return 34
    elif distance_km <= 150:
        return 36
    elif distance_km <= 180:
        return 39
    elif distance_km <= 200:
        return 42
    elif distance_km <= 250:
        return 46
    elif distance_km <= 300:
        return 50
    elif distance_km <= 350:
        return 53
    elif distance_km <= 400:
        return 56
    elif distance_km <= 500:
        return 64
    elif distance_km <= 600:
        return 72
    elif distance_km <= 750:
        return 82
    elif distance_km <= 800:
        return 86
    elif distance_km <= 900:
        return 93
    elif distance_km <= 950:
        return 97
    elif distance_km <= 1000:
        return 100
    elif distance_km <= 1150:
        return 111
    elif distance_km <= 1200:
        return 115
    elif distance_km <= 1250:
        return 118
    else:
        return 120
