n=int(input("Enter a number"))
if n<=1:
    print("not a prime")
else:
    for i in range(2,n):
        if n%i==0:
            print("Not a prime")
            break
    else:
        print("Prime")