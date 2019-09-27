import re

str = "Paragon OS3      \n\n\n4.5 out "
x = re.search("^(.*)\n.*", str)

print("The first white-space character is located in position:", x.start())
print(x.group(0).strip())
