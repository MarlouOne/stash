# n = int(input("Введите количество строк: "))

# for i in range(n):
#     for j in range(n - i - 1):
#         print(end=" ")
#     for j in range(i+1):
#         print("*", end=" ")
#     print()
    
    

# n = int(input("Введите количество строк: "))

# for i in range(n):
#     for j in range(n - i - 1):
#         print(end=" ")
#     for j in range(2*i+1):
#         if i == (n-1)//2 and j == i:
#             print(end=" ")
#         else:
#             print("*", end=" ")
#     print()

# for i in range(n-2,-1,-1):
#     for j in range(n - i - 1):
#         print(end=" ")
#     for j in range(2*i+1):
#         if i == (n-1)//2 and j == i:
#             print(end=" ")
#         else:
#             print("*", end=" ")
#     print()

n = int(input("Введите количество строк: "))

# Рисуем рамку
for i in range(n+2):
    for j in range(n+2):
        if i == 0 or i == n+1 or j == 0 or j == n+1:
            print("*", end=" ")
        else:
            print(end="  ")
    print()

# Рисуем свастику
for i in range(n):
    for j in range(n - i - 1):
        print(end=" ")
    for j in range(2*i+1):
        if i == (n-1)//2 and j == i:
            print(end=" ")
        else:
            print("*", end=" ")
    print()

for i in range(n-2,-1,-1):
    for j in range(n - i - 1):
        print(end=" ")
    for j in range(2*i+1):
        if i == (n-1)//2 and j == i:
            print(end=" ")
        else:
            print("*", end=" ")
    print()