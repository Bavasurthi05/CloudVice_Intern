# for i in range(1,101,1):
#     if i==50:
#         break
#     if i%5!=0:
#         print(i,end=' ')

# x=30
# y=50
# x,y=y,x
# print(x,y,end=' ')

# for i in range(2,101,2):
#     print(i,end=' ')

# x=54
# y=60
# print("Perimeter of rectangle =",2*(x+y))

# x=str(input("Enter your name"))
# y=int(input("Enter your age"))
# print("Hello",x)
# print("You are",y,"years")

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