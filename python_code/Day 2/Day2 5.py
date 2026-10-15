def cnt_freq(numbers):
    freq={}
    for num in numbers:
        if num in freq:
            freq[num]+=1
        else:
            freq[num]=1
    return freq

numbers=[1,3,1,2,5,2,2,3,1,4,5,6]
print(cnt_freq(numbers))