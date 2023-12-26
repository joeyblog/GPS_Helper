import gps_helper


while True:
    inp = input("\n[-] Enter coordinates (lat, lon): ")

    if inp.lower() == 'exit':
        break

    try:
        lat, lon = gps_helper.parse(inp.strip())
        gps_helper.teleport(lat, lon)
    except Exception as e:
        print(f"Error: {e}")
