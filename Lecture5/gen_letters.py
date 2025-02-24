import string;

print("".join(string.ascii_uppercase[:26] + string.ascii_lowercase[:26] + "0123456789")[:64])

