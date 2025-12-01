#0 1 1 2 3 5 8 13 ...
import time
class Task_1 :
    def fibonacci(n):
        j, k = 0, 1
        i=0
        while i <= n :
            print(j)
            j, k = k, j + k
            i += 1

s = int(input("Enter a range: "))
start = time.time()
Task_1.fibonacci(s)
print("\nExecution Time >> ",time.time() - start)

        