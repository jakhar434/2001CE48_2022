def factorial(x):
    if(x ==1 or x==0):
        return 1
    return x*factorial(x-1)
    

x=int(input("Enter the number whose factorial is to be found: "))
print(factorial(x))
