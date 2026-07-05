import math


def read_zip_all():
    i = 0
    header = []
    zip_codes = []
    zip_data = []
    skip_line = False
    # http://notebook.gaslampmedia.com/wp-content/uploads/2013/08/zip_codes_states.csv
    for line in open('zip_codes_states.csv').read().split("\n"):
        skip_line = False
        m = line.strip().replace('"', '').split(",")
        i += 1
        if i == 1:
            for val in m:
                header.append(val)
        else:
            zip_data = []
            for idx in range(0, len(m)):
                if m[idx] == '':
                    skip_line = True
                    break
                if header[idx] == "latitude" or header[idx] == "longitude":
                    val = float(m[idx])
                else:
                    val = m[idx]
                zip_data.append(val)
            if not skip_line:
                zip_codes.append(zip_data)
    return zip_codes


def deg1(lat):
    degrees = int(abs(lat))
    minn = (abs(lat) - degrees) * 60
    minutes = int(minn)
    sec = (minn - minutes) * 60

    if lat >= 0:
        return f"{degrees:03d}°{minutes:02d}'{sec:05.2f}\"N"
    else:
        return f"{degrees:03d}°{minutes:02d}'{sec:05.2f}\"S"


print("\n")
print("TEST_DEG1")
test_deg1 = [42.673701, -42.673701, 0]
expected_deg1 = ['042°40\'25.32"N', '042°40\'25.32"S', '000°00\'00.00"N']
test_passed_cnt = 0
total_test_cnt = 0

for test_idx in range(len(test_deg1)):
    actual_deg1 = deg1(test_deg1[test_idx])
    total_test_cnt += 1
    print(
        f"Running test_deg1({test_deg1[test_idx]}), expected result is {expected_deg1[test_idx]}, actual result is {actual_deg1}")

    if expected_deg1[test_idx] == actual_deg1:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")

print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")


def deg2(long):
    degrees = int(abs(long))
    minn = (abs(long) - degrees) * 60
    minutes = int(minn)
    sec = (minn - minutes) * 60

    if long >= 0:
        return f"{degrees:03d}°{minutes:02d}'{sec:05.2f}\"E"
    else:
        return f"{degrees:03d}°{minutes:02d}'{sec:05.2f}\"W"


"""     
print("\n")
print("TEST_DEG2")
test_deg2 = [-73.608792, 73.608792, 0]
expected_deg2 = ['073°36\'31.65"W', '073°36\'31.65"E', '000°00\'00.00"E']
test_passed_cnt = 0
total_test_cnt = 0

for test_idx in range(len(test_deg2)):
    actual_deg2 = deg2(test_deg2[test_idx])
    total_test_cnt += 1
    print(f"Running test_deg2({test_deg2[test_idx]}), expected result is {expected_deg2[test_idx]}, actual result is {actual_deg2}")

    if expected_deg2[test_idx] == actual_deg2:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")

print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")
"""


def loc():
    try:
        code = int(input('Enter a ZIP Code to lookup => '))
        print(code)
    except ValueError as er:
        print(f'Ошибка: {type(er)}, {er}. Введите корректный ZIP-код могут быть только цифры')
        return
    found = False
    for i in range(len(zip_codes)):
        if (zip_codes[i][0] == str(code)):
            city = zip_codes[i][3]
            state = zip_codes[i][4]
            county = zip_codes[i][5]
            lat = deg1(zip_codes[i][1])
            long = deg2(zip_codes[i][2])

            print(f"ZIP CODE {code} is in {city}, {state}, {county} county, coordinates: ({lat}, {long})")
            found = True
            break
    if not found:
        print(f"ZIP Code {code} not found")


"""         
print("\n")
print("TEST_LOC")
test_loc = [
    (96921, "Barrigada", "GU", "Guam", "013°26'39.33\"N", "144°47'10.67\"E"),
    (12180, "Troy", "NY", "Rensselaer", "042°40'25.32\"N", "073°36'31.65\"W")
]
expected_loc = [
    f"ZIP CODE 96921 is in Barrigada, GU, Guam county, coordinates: (013°26'39.33\"N, 144°47'10.67\"E)",
    f"ZIP CODE 12180 is in Troy, NY, Rensselaer county, coordinates: (042°40'25.32\"N, 073°36'31.65\"W)"
]
test_passed_cnt = 0
total_test_cnt = 0

for test_idx in range(len(test_loc)):
    code = test_loc[test_idx][0]
    city = test_loc[test_idx][1]
    state = test_loc[test_idx][2]
    county = test_loc[test_idx][3]
    lat = test_loc[test_idx][4]
    long = test_loc[test_idx][5]

    actual_loc = f"ZIP CODE {code} is in {city}, {state}, {county} county, coordinates: ({lat}, {long})"
    total_test_cnt += 1
    print(f"Running test_loc({code}), expected result is {expected_loc[test_idx]}, actual result is {actual_loc}")

    if expected_loc[test_idx] == actual_loc:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")

print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")
"""


def zip():
    city = input('Enter a city name to lookup => ').strip().lower()
    print(city)
    state = input('Enter the state name to lookup => ').strip().lower()
    print(state)

    if not city or not state:
        print("Ошибка: city и state не могут быть пустыми")
        return

    city_table = ""
    state_table = ""

    zip_list = []
    for i in range(len(zip_codes)):
        if zip_codes[i][3].lower() == str(city) and zip_codes[i][4].lower() == str(state):
            zip_list.append(zip_codes[i][0])
            if len(zip_list) == 1:
                city_table = zip_codes[i][3]
                state_table = zip_codes[i][4]
    if zip_list:
        print(f"The following ZIP Code(s) found for {city_table}, {state_table} : {', '.join(zip_list)}")
    else:
        print(f"No ZIP Code found for {city}, {state}")


"""  
print("\n")
print("TEST_ZIP")
test_zip = [
    ("Troy", "NY", ["12179", "12180", "12181", "12182", "12183"])
]
expected_zip = [
    "The following ZIP Code(s) found for Troy, NY: 12179, 12180, 12181, 12182, 12183"
]
test_passed_cnt = 0
total_test_cnt = 0

for test_idx in range(len(test_zip)):
    city = test_zip[test_idx][0]
    state = test_zip[test_idx][1]
    zip_list = test_zip[test_idx][2]

    actual_zip = f"The following ZIP Code(s) found for {city}, {state}: {', '.join(zip_list)}"
    total_test_cnt += 1
    print(f"Running test_zip({city}, {state}), expected result is {expected_zip[test_idx]}, actual result is {actual_zip}")

    if expected_zip[test_idx] == actual_zip:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")

print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")
"""


def calc(lat1, lat2, long1, long2):
    lat1 = lat1 * math.pi / 180
    long1 = long1 * math.pi / 180
    lat2 = lat2 * math.pi / 180
    long2 = long2 * math.pi / 180

    dif_lat = lat2 - lat1
    dif_long = long2 - long1

    a = math.sin(dif_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dif_long / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    result = 3959.0 * c

    return result


"""   
print("\n")
print("TEST_CALC")
test_calc = [
    (42.673701, 40.922326, -73.608792, -72.637078),
    (40.7128, 34.0522, -74.0060, -118.2437)
]
expected_calc = [130.96, 2445.71]
test_passed_cnt = 0
total_test_cnt = 0

for test_idx in range(len(test_calc)):
    actual_calc = round(calc(*test_calc[test_idx]), 2)
    total_test_cnt += 1
    print(f"Running test_calc({test_calc[test_idx]}), expected result is {expected_calc[test_idx]}, actual result is {actual_calc}")

    if expected_calc[test_idx] == actual_calc:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")

print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")
"""


def dist():
    try:
        code1 = int(input('Enter the first ZIP Code => '))
        print(code1)
        code2 = int(input('Enter the second ZIP Code => '))
        print(code2)
    except ValueError as er:
        print(f'Ошибка: {type(er)}, {er}. Введите корректные ZIP-коды  могут быть только цифры')
        returnrnht

    found1 = False
    found2 = False
    for i in range(len(zip_codes)):
        if zip_codes[i][0] == str(code1):
            lat1 = zip_codes[i][1]
            long1 = zip_codes[i][2]
            found1 = True
        if zip_codes[i][0] == str(code2):
            lat2 = zip_codes[i][1]
            long2 = zip_codes[i][2]
            found2 = True

    if found1 and found2:
        dist = calc(lat1, lat2, long1, long2)
        print(f"The distance between {code1} and {code2} is {dist:.2f} miles")
    else:
        if not found1:
            print(f"ZIP Code {code1} not found")
        if not found2:
            print(f"ZIP Code {code2} not found")


"""
print("\n")
print("TEST_DIST")
test_dist = [
    (19465, 12180, 201.87)
]
expected_dist = [
    f"The distance between 19465 and 12180 is 201.87 miles"
]
test_passed_cnt = 0
total_test_cnt = 0

for test_idx in range(len(test_dist)):
    code1 = test_dist[test_idx][0]
    code2 = test_dist[test_idx][1]
    dist_val = test_dist[test_idx][2]

    actual_dist = f"The distance between {code1} and {code2} is {dist_val:.2f} miles"
    total_test_cnt += 1
    print(f"Running test_dist({code1}, {code2}), expected result is {expected_dist[test_idx]}, actual result is {actual_dist}")

    if expected_dist[test_idx] == actual_dist:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")

print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")
"""
zip_codes = read_zip_all()

while True:
    comm = input("Command ('loc', 'zip', 'dist', 'end') => ")
    comm = comm.strip().lower()
    print(comm)

    match comm:
        case 'loc':
            loc()
        case 'zip':
            zip()
        case 'dist':
            dist()
        case 'end':
            print('Done')
            break
        case _:
            print('Invalid command, ignoring')

