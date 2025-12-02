class pyramids:
    def rev_pyra(n):    
        for i in range(n, 0, -1):
            for j in range(0, i, +1):
                print('*',end=' ')
            print()
            
    def pyra(n):    
        for i in range(0, n+1, +1):
            for j in range(0, i, +1):
                print('*',end=' ')
            print()        

    def right_pyra(n):
        for i in range(0, n+1, +1):
            for s in range(5,i,-1):
                print(" ", end=" ")    
            for j in range(1, i+1, +1):
                print('*',end=' ')
            print()
            
    def half_triangle(n):
        for i in range(0, n+1, +1):
            for s in range(5,i,-1):
                print(" ", end=" ")    
            for j in range(1, i+1, +1):
                print('*',end=' ')
            for j in range(1, i, +1):
                print('*',end=' ')
            print()                

    def diamond(n):
        for i in range(1, n+1, +1):
            for s in range(n+1,i,-1):
                print(" ", end="")    
            for j in range(1, i+1, +1):
                print('*',end='')
            for j in range(1, i, +1):
                print('*',end='')
            print()
            
        for k in range(n-1, 0, -1):
            for s in range(n,k-1,-1):
                print(" ", end="")    
            for j in range(0, k, +1):
                print('*',end='')
            for j in range(1, k, +1):
                print('*',end='')
            print()
            
            
pyramids.rev_pyra(5)
pyramids.pyra(5)
pyramids.right_pyra(5)
pyramids.half_triangle(5)
n = int(input("Enter the number of rows >> "))
pyramids.diamond(n)
