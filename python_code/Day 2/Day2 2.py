thisdict={
    "Raju":78,
    "Priya":52,
    "Ragul":95,
    "Swathi":35,
    "Arun":69
}
maxvalue=0
for x in thisdict:
    if thisdict[x]>maxvalue:
        maxvalue=thisdict[x];
print("Topper =",maxvalue)