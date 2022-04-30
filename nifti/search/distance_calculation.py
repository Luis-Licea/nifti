#for distance calculation
import haversine as hs
from haversine import Unit
from geopy.geocoders import Nominatim

#Ameen
#Call this everytime the user tries to enter an address,
#and have a popup saying: "Address Invalid, try using a different address format. Include the City."
def check_address_valid(address):
    try:
        #Address Format: Number Street, City
        nifti_locator_app = Nominatim(user_agent="nifti_web_app")
        location = nifti_locator_app.geocode(address)
        print("Location:", location)
        if(location != None):
            return True
        else:
            return False
    except Exception as e:
        return False
#Ameen
#django Q these into post
def get_coords_by_addr(address):
    try:
        nifti_locator_app = Nominatim(user_agent="nifti_web_app")
        location = nifti_locator_app.geocode(address)
        #format to include up to 10 decimal points
        lat = float("{:.10f}".format(location.latitude))
        long = float("{:.10f}".format(location.longitude))
        #print(f"lat: {lat}\nlong: {long}")
        return (lat, long)
    except Exception as e:
        print("Invalid Address: " + address)
        print("Using (1,1) as lat, long.")
        return (1.0, 1.0)

#Ameen
def get_distance_between_coords(src_lat, src_long, dest_lat, dest_long):
    #params must be float type
    return hs.haversine((src_lat,src_long),(dest_lat,dest_long), unit=Unit.MILES)