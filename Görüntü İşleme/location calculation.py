import math

def distance(lat1,lat2,lon1,lon2):

    radius = 6371000 # m

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def calculate_coordinates(initial_lat, initial_lon, slope, distance_meters):
  # slope değişkeni uçağın gidiş yönü  -+servodan alacağımız açı
    # Convert latitude and longitude to radians
    initial_lat_rad = math.radians(initial_lat)
    initial_lon_rad = math.radians(initial_lon)

    # Convert distance from meters to radians
    distance_rad = distance_meters / 6371000.0  # 6371000.0 is the Earth's radius in meters

    # Calculate new latitude
    new_lat_rad = math.asin(math.sin(initial_lat_rad) * math.cos(distance_rad) +
                            math.cos(initial_lat_rad) * math.sin(distance_rad) * math.cos(math.radians(slope)))

    # Calculate new longitude
    new_lon_rad = initial_lon_rad + math.atan2(math.sin(math.radians(slope)) * math.sin(distance_rad) * math.cos(initial_lat_rad),
                                               math.cos(distance_rad) - math.sin(initial_lat_rad) * math.sin(new_lat_rad))

    # Convert back to degrees
    new_lat = math.degrees(new_lat_rad)
    new_lon = math.degrees(new_lon_rad)

    return new_lat, new_lon


# Kullanım örneği
initial_coordinates = (38.6532469, 35.5671591)  # Başlangıç koordinatları 0.000000,0.000000
slope = 135 # Eğim Kuzeye göre
distance_meters = 246 # Uzaklık  metre

new_coordinates = calculate_coordinates(initial_coordinates[0], initial_coordinates[1], slope, distance_meters)
#                                       İha konum X             İha Konum Y            gpsangle()  distanceX

print(f"Yeni koordinatlar: {new_coordinates[0]}, {new_coordinates[1]}")

# distance(40.6266707,40.6266707 ,29.1451836,29.1461277)