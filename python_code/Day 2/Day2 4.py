class student:
    def __init__(self,name,age,mark):
        self.name=name
        self.age=age
        self.mark=mark
    def display(self):
        print("Name: ",self.name)
        print("Age: ",self.age)
        print("Mark", self.mark)

s1=student("Raju",23,56)
s2=student("Arun",85,67)
s3=student("Priya",19,97)

s1.display()
s2.display()
s3.display()