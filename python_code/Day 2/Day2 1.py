def factorial(n):
    fact=1
    for i in range(1,n+1):
        fact=fact*i
    return fact

n=int(input("Enter a number: "))
if(n<0):
    print("Factorial is not defined for negative numbers")
else:
    print("Factorial =",factorial(n))