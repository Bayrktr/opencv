"""
x = "8441emir322mk21dkj21wdkj23wkjn1d2kjh1dkbhj21dbhkj21d2hkjb1ed2hjb1dhjbwqhkdwqbhkjfhıw1fhkjbw1jkndw1"
i = 0

words = []
while i < len(x):
    i += 1
    words.append(x[i - 1])


for i in words:
    if i.isdigit():
        words.remove(i)


print("".join(words))

"""
import re

x = "1qdwdwqwqedwqdwqd87/841851emir"
m = re.findall("\D+", str(x))
print(m[0])
