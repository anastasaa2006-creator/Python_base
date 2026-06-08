test_cases = int(input())

for test_cases_idx in range(test_cases):
    n_d = input().split()
    n = int(n_d[0])
    d = int(n_d[1])
    num = input()
    
    for idx in range(n):
        if int(num[idx]) < d:
            print(num[:idx] + str(d) + num[idx:])
            break
    else:
        print(num + str(d))