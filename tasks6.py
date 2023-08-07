from random import randint
from decimal import Decimal
import re

task = int(input("Введите номер задачи, которую вы хотите проверить (30,32) или доп. задачи (1,2,3)\n"))
if task not in [30,32,1,2,3]:
    print("Вы ввели значение {0}, такой задачи не было в домашнем задании".format(task))
else:
    if task == 30:
        print ("Решение задачи 30:")
        n = int(input("Введите количество элементов прогрессии\n"))
        a1 = Decimal(input("Введите первый элемент прогрессии\n"))
        d = Decimal(input("Введите разность\n"))

        def create_prog(n, a1, d):
            rs = []
            for i in range(n):
                rs.append(float(a1 + i*d))
            return rs
        
        print ("Все члены арифметической прогрессии:\n{0}".format(create_prog(n,a1,d)))
    elif task == 32:
        arr = [randint(-100,100) for _ in range(10)]
        print ("Рандомно создали список:\n{0}".format(arr));
        m1 = int(input("Введите минимальное значение\n"));
        m2 = int(input("Введите максимальное значение\n"));
        
        def filt(array, min_value, max_value): 
            return [k for k, value in enumerate(array) 
                    if value < max_value and value > min_value]
        print("Индексы значений, которые мы ищем:\n{0}".format(filt(arr,m1,m2)))
    elif task == 1:
        s = input("Введите, пожалуйста, арифметическое выражение\n")
        def parse(exp):
            #print("parse exp:{0}".format(exp))
            reg1 = r"\((.+?)\)"
            reg_template = r"(-?\d+(?:\.\d+)?)\s*\{}\s*(-?\d+(?:\.\d+)?)"
            oper_priority = ["*","/","+","-"]
            operations = {
                "*": lambda x,y: str(Decimal(x)*Decimal(y)),
                "/": lambda x,y: str(Decimal(x)/Decimal(y)),
                "+": lambda x,y: str(Decimal(x)+Decimal(y)),
                "-": lambda x,y: str(Decimal(x)-Decimal(y))
            }
            search = re.search(r"\((.+?)\)",exp)
            if search:
                return parse(exp.replace(search.group(0),parse(search.group(1))))
            for oper in oper_priority:
                search = re.search(r"(-?\d+(?:\.\d+)?)\s*\{}\s*(-?\d+(?:\.\d+)?)".format(oper),exp)
                if search:
                    return parse(exp.replace(search.group(0),operations[oper](*search.groups())))
            return exp
        
        print("Результат операции: {0}".format(parse(s)))
    elif task == 2:
        
        def show_field(f):
            print("[*] [1] [2] [3]")
            for i,row in enumerate(f):
                p = ["[ ]" if v == "" else "[{0}]".format(v) for v in row]
                p.insert(0,"[{0}]".format(i+1))
                print (*p)
        
        def test_field(f):
            def tell_winner():
                if x_count == 3:
                    print("Вы победили!")
                    return True
                if o_count == 3:
                    print("Вы проиграли!")
                    return True
                return False
            #проверяем построчно
            x_count = 0
            o_count = 0
            for i in range(3):
                for j in range(3):
                    if f[i][j] == "x":
                        x_count += 1
                    if f[i][j] == "o":
                        o_count += 1
                    if tell_winner():
                        return True
            #проверяем по столбцам
            x_count = 0
            o_count = 0
            for i in range(3):
                for j in range(3):
                    if f[j][i] == "x":
                        x_count += 1
                    if f[j][i] == "o":
                        o_count += 1
                    if tell_winner():
                        return True
            #проверяем диагонали
            x_count = 0
            o_count = 0
            for i in range(3):
                if f[i][i] == "x":
                    x_count += 1
                if f[i][i] == "o":
                    o_count += 1
                if tell_winner():
                    return True
            x_count = 0
            o_count = 0
            for i in range(3):
                if f[len(f)-1-i][i] == "x":
                    x_count += 1
                if f[len(f)-1-i][i] == "o":
                    o_count += 1
                if tell_winner():
                    return True

        def game():
            field = [["","",""],["","",""],["","",""]]
            print ("Начинаем нашу игру (вы играете крестиками):")
            show_field(field)
            while True:
                turn = input("Введите пару чисел, обозначающую ячейку, в которую вы хотите поставить крестик. Пример: 1,2\n")
                turn = tuple((int(i)-1 for i in turn.split(",")))
                if len(turn) != 2:
                    print("Неверный формат команды, попробуйте еще")
                elif turn[0] < 0 or turn[1] < 0 or turn[0] > 2 or turn[1] > 2:
                    print("Нет ячейки с такими индексами, попробуйте еще")
                elif field[turn[0]][turn[1]] != "":
                    print("Такая ячейка уже занята, попробуйте еще")
                else:
                    #ход игрока
                    field[turn[0]][turn[1]] = "x"
                    print ("Ваш ход:")
                    show_field(field)
                    if test_field(field):
                        break
                    #ход AI-дурака
                    while True:
                        ai_x = randint(0,2)
                        ai_y = randint(0,2)
                        if field[ai_x][ai_y] == "":
                            field[ai_x][ai_y] = "o"
                            print("Ход вашего соперника:")
                            show_field(field)
                            break
                        if test_field(field):
                            break

        game()

    elif task == 3:                
        print("Введите данные (Enter/Paste, пустая строка чтобы сохранить)\n")
        contents = []
        def getResults(contents):
            while True:
                try:
                    line = input()
                    if line == "":
                        break
                except EOFError:
                    break
                contents.append(line)
            teams = {}
            for i,row in enumerate(contents):
                if i == 0:
                    games_num = int(row)
                else:
                    data = row.split(";")
                    for team in (data[0],data[2]):
                        if team not in teams:
                            teams[team] = {"games":0,"win":0,"draw":0,"lose":0,"score":0}
                    teams[data[0]]["games"] += 1
                    teams[data[2]]["games"] += 1
                    if int(data[1]) > int(data[3]):
                        teams[data[0]]["win"] += 1
                        teams[data[2]]["lose"] += 1
                    elif int(data[1]) < int(data[3]):
                        teams[data[2]]["win"] += 1
                        teams[data[0]]["lose"] += 1
                    else:
                        teams[data[2]]["draw"] += 1
                        teams[data[0]]["draw"] += 1

            for k,v in teams.items():
                print("{0}:{1}".format(k," ".join([str(x) for x in v.values()])))

        getResults(contents)
     

                        
                    
