n = int(input())
array = input().split()

for i in range(n):
    array[i] = int(array[i])

total_sum = sum(array)

if total_sum != 0:
    print("YES")
    print(1)
    print(1, n)
else:
    idx = -1
    for i in range(n):
        if array[i] != 0:
            idx = i
            break
    
    if idx != -1:
        print("YES")
        print(2)
        print(1, idx + 1)
        print(idx + 2, n)
    else:
        print("NO")