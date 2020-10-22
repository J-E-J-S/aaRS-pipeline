#!/usr/bin/env python

import sys

data = sys.argv
new=data[1:]


for number in range(len(new)):
    new[number] = new[number].replace(',', '').replace('[', '').replace(']', '')

print (new)
print(type(new))
