first = ['Strings', 'Student', 'Computers']
second = ['Строка', 'Урбан', 'Компьютер']
first_result=(int(((len(a[1])-len(a[0]))**2)**0.5) for a in zip(first, second) if len(a[0])!=len(a[1]))
print(list(first_result))
second_result=(len(first[i])==len(second[i]) for i in range(len(first)))
print(list(second_result))
