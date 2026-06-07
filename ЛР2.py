import math

def interaction(num):
    print(num)
    return float(num)

print("TEST_INTERACTION:")
test_interaction = [8, 10, 20, 0, 1]
excepted_interaction = [8.0, 10.0, 20.0, 0.0, 1.0]
test_passed_cnt = 0
total_test_cnt = 0
for test_idx in range(len(test_interaction)):
    actual_interaction = interaction(test_interaction[test_idx])
    total_test_cnt += 1
    print(f"Running test_interaction({test_interaction[test_idx]}), expected result is {excepted_interaction[test_idx]},"
            f"actual result is {actual_interaction}")
    if excepted_interaction[test_idx] == actual_interaction:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")
print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")


def calc_x(d1,theta1):
    """
    calc_x(10,0)
    0.0
    calc_x(5,45)
    5.0
    calc_x(10,89)
    573.0
    calc_x(10,30)
    5.7735
    calc_x(10,60)
    17.32
    """
    return d1 * math.tan(theta1 * math.pi/180)

import doctest
doctest.testmod()


def calc_L1(x,d1):
    return math.sqrt(x**2+d1**2)

print("\n")
print("TEST_CALC_L1")
test_calc_L1 = [[3,4], [5,12], [6,8], [0,5], [1,1], [5,0], [0,0]]
excepted_calc_L1 = [5.0, 13.0, 10.0, 5.0, 1.4142135623730950488016887242097, 5.0, 0.0]
test_passed_cnt = 0
total_test_cnt = 0
for test_idx in range(len(test_calc_L1)):
    actual_calc_L1 = calc_L1(test_calc_L1[test_idx][0], test_calc_L1[test_idx][1])
    total_test_cnt += 1
    print(f"Running test_calc_L1({test_calc_L1[test_idx]}), expected result is {excepted_calc_L1[test_idx]},"
            f"actual result is {actual_calc_L1}")
    if excepted_calc_L1[test_idx] == actual_calc_L1:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")
print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")

def calc_L2(h,x,d2):
    return math.sqrt((h-x)**2 + (d2/3)**2)

print("\n")
print("TEST_CALC_L2")
test_calc_L2 = [[50,6.5743, 10], [50,23.094, 10],[20,5,9], [30,10,12], [100,50,30], [5,2,0], [0,0,3]]
excepted_calc_L2 = [43.553444543469935646783066790224, 27.111693918143718802865293841224, 15.297058540778354490084672327068, 20.396078054371139320112896436091, 50.990195135927848300282241090228, 3.0, 1.0]
test_passed_cnt = 0
total_test_cnt = 0
for test_idx in range(len(test_calc_L2)):
    actual_calc_L2 = calc_L2(test_calc_L2[test_idx][0], test_calc_L2[test_idx][1], test_calc_L2[test_idx][2])
    total_test_cnt += 1
    print(f"Running test_calc_L2({test_calc_L2[test_idx]}), expected result is {excepted_calc_L2[test_idx]},"
            f"actual result is {actual_calc_L2}")
    if excepted_calc_L2[test_idx] == actual_calc_L2:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")
print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")
    
def calc_t(v_sand,L1,n,L2): 
    return (1/(v_sand*5280/3))*(L1+n*L2)*3600

print("\n")
print("TEST_CALC_T")
test_calc_t = [[5, 10.36, 2, 43.55], [10, 10.36, 2, 43.55],[2.5, 10.36, 2, 43.55], [5, 20.72, 2, 43.55], [5, 0, 2, 43.55], [1, 100, 5, 50], [100, 1, 1, 1]]
excepted_calc_t = [39.87, 19.935, 79.74, 44.10818181818181, 35.631818181818176, 715.90909090909090909090909090909, 0.04090909090909090909090909090909]
test_passed_cnt = 0
total_test_cnt = 0
for test_idx in range(len(test_calc_t)):
    actual_calc_t = calc_t(test_calc_t[test_idx][0], test_calc_t[test_idx][1], test_calc_t[test_idx][2], test_calc_t[test_idx][3])
    total_test_cnt += 1
    print(f"Running test_calc_t({test_calc_t[test_idx]}), expected result is {excepted_calc_t[test_idx]},"
            f"actual result is {actual_calc_t}")
    if excepted_calc_t[test_idx] == actual_calc_t:
        print("Test passed")
        test_passed_cnt += 1
    else:
        print("Test failed")
print(f"{total_test_cnt} test executed, {test_passed_cnt} tests passed successfully!")
    
    


def main():
    d1 = interaction(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => "))
    d2 = interaction(input("Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => "))
    h = interaction(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => "))
    v_sand = interaction(input("Введите скорость движения спасателя по песку, v_sand (мили в час) => "))
    n = interaction(input("Введите коэффициент замедления спасателя при движении в воде, n => "))
    theta1 = interaction(input("Введите направление движения спасателя по песку, theta1 (градусы) => "))


    x = calc_x(d1,theta1)
    L1 = calc_L1(x,d1)
    L2 = calc_L2(h,x,d2)
    t = calc_t(v_sand,L1,n,L2)
    print(f"Если спасатель начнёт движение под углом theta1, равным {theta1:.0f} градусам, он достигнет утопающего через {t:.1f} секунды")

print("\n")
main()