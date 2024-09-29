string = input("Введите свой массив через пробел: \n")
array = string.split(" ")
array = set(array)
print(array, sep=" ")