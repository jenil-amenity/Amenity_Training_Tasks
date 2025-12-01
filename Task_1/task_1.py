#0 1 1 2 3 5 8 13 ...
class Task_1 :
    def fibonacci(n):
        j, k = 0, 1
        i=0
        a = []
        while i <= n :
            a.append(j)
            j, k = k, j + k
            i += 1
        print(a)

s = int(input("Enter a range: "))
Task_1.fibonacci(s)

        