import math

def interaction(num):
    print(num)
    return float(num)


def calc_x(d1,theta1):

    return d1 * math.tan(theta1 * math.pi/180)


def calc_L1(x,d1):
    return math.sqrt(x**2+d1**2)

def calc_L2(h,x,d2):
    return math.sqrt((h-x)**2 + (d2/3)**2)

def calc_t(v_sand,L1,n,L2): 
    return (1/(v_sand*5280/3))*(L1+n*L2)*3600


def main():
    d1 = interaction(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => "))
    d2 = interaction(input("Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => "))
    h = interaction(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => "))
    v_sand = interaction(input("Введите скорость движения спасателя по песку, v_sand (мили в час) => "))
    n = interaction(input("Введите коэффициент замедления спасателя при движении в воде, n => "))

    t_best = 10000
    theta1_best = 0
    theta1 = 1

    while theta1 <= 90:
        #print(f"\n theta1 = {theta1}")
        x = calc_x(d1,theta1)
        L1 = calc_L1(x,d1)
        L2 = calc_L2(h,x,d2)
        t = calc_t(v_sand,L1,n,L2)
        if t_best > t:
            t_best = t
            theta1_best = theta1
            #print(f"при theta1 = {theta1:.1f} t_best = {t_best:.1f} ")
        
        theta1 += 0.1
        
        
    print(f"Если спасатель начнёт движение под углом theta1, равным {theta1_best:.1f} градусам, он достигнет утопающего через {t_best:.1f} секунды")

print("\n")
main()