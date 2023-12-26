import folium
import streamlit as st
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import gps_helper as gps
import re

st.set_page_config(
    page_title="GPS Helper",
    page_icon=":world_map:️",
    layout="wide",
)

if 'lat' not in st.session_state:
    st.session_state.lat = "35.6812362"
if 'lon' not in st.session_state:
    st.session_state.lon = "139.7649361"
if 'msg' not in st.session_state:
    st.session_state.msg = ""
if 'coord' not in st.session_state:
    st.session_state.coord = ""

def send_tp():
    lat = st.session_state.lat
    lon = st.session_state.lon
    gps.teleport(lat, lon)
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(st.session_state.coord, language='en')
    address = location.raw['address']
    address_str = address.get('country', '')
    if(address.get("city") and address.get("country")):
        address_str = address.get('city', '') + ", " + address.get('country', '')
    print(address_str)
    st.session_state.msg = f"Teleported to {address_str} ({lat}, {lon})"
    
    #st.session_state.last_coord =st.session_state.coord
    st.session_state.coord = ""

def update():
    pattern = r'[^0-9,.-]'
    st.session_state.coord = re.sub(pattern, '', st.session_state.coord)
    st.session_state.lat, st.session_state.lon = gps.parse(st.session_state.coord)
    st.session_state.msg = ""
    if("last_coord" in st.session_state):
        if(st.session_state.last_coord):
            calc()

def calc():
    st.session_state.msg = ""
    last_lat, last_lon = gps.parse(st.session_state.last_coord)
    distance = gps.calc_distance(st.session_state.lat, st.session_state.lon, last_lat, last_lon)
    cooldown = gps.calculate_cooldown(distance/1000)
    distance_str = f"{cooldown}min ("
    if(distance > 1000):
        distance_str += '{:.2f}'.format(distance / 1000) + "km)"
    else:
        distance_str += '{:.0f}'.format(distance) + "m)"
    
    st.session_state.distance = distance_str

def save():
    st.session_state.msg = ""
    st.session_state.last_coord =st.session_state.coord

st.title('GPS Teleport Helper')

st.text_input(label="Coordinate", placeholder="input coordinate here", on_change=update, key='coord')
col1, col2, col3 = st.columns([1,1,2])
with col1:
    st.button("Teleport", on_click=send_tp)
with col2:
    st.button("Save as Caught", on_click=save)
with col3:
    if("last_coord" in st.session_state):
        if(st.session_state.last_coord):
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse(st.session_state.last_coord, language='en')
            address = location.raw['address']
            address_str = address.get('country', '')
            if(address.get("city") and address.get("country")):
                address_str = address.get('city', '') + ", " + address.get('country', '')
            st.write(f"Last caught at: {address_str} ({st.session_state.last_coord})")
if("last_coord" in st.session_state):
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        if(st.session_state.last_coord):
            st.button("Calculate Cooldown", on_click=calc)
    with col3:
        if("distance" in st.session_state):
            st.write(f"Cooldown: {st.session_state.distance}")
    
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12)
folium.Marker(
    [st.session_state.lat, st.session_state.lon]
).add_to(m)
if(st.session_state.msg):
    st.success(st.session_state.msg)
st_data = st_folium(m, width=500, height=500)

#st.write(st.session_state.lat+", "+ st.session_state.lon)


    





