from random import randint
import re

task = int(input("Введите номер задачи, которую вы хотите проверить (22,24,1,2)\n"))
if task not in [22,24,1,2]:
    print("Вы ввели значение {0}, такой задачи не было в домашнем задании".format(task))
else:
    if task == 22:
        print ("Решение задачи 22:")
        n1 = int(input("Введите количество элементов первого множества\n"))
        print ("Теперь заполним множество.")
        q1 = []
        for i in range(n1):
            q1.append(int(input("Введите {0}е число\n".format(i+1))))
        n2 = int(input("Введите количество элементов второго множества\n"))
        print ("Теперь заполним множество.")
        q2 = []
        for i in range(n2):
            q2.append(int(input("Введите {0}е число\n".format(i+1))))

        def findIntersection(q1,q2):
            #избавляемся от повторов (самый быстрый способ)
            q1 = list(set(q1))
            q2 = list(set(q2))
            #выбираем множество с самым меньшим количеством элементов
            if len(q1) < len(q2):
                rs = q1
            else:
                rs = q2
                q2 = q1
            #выкидываем значения, которые не встречаются в большем множестве
            for i,elem in enumerate(rs):
                if elem not in q2:
                    rs.pop(i)
            return sorted(rs)
    
        print("Выдаем значения пересечения множеств:")
        inter = findIntersection(q1,q2)
        if len(inter) > 0:
            for elem in inter:
                print(elem)
            else:
                print ("Нет пересечений")
    elif task == 24:
        #генерируем грядку
        q = int(input("Введите количество кустов\n"));
        if q < 3:
            print("Нам трудно будет найти ДВУХ соседей у куста, если кустов всего {q}".format(q))
        else:
            maxberries = int(input("Введите максимальное количество ягод на кусте\n"));
            gardenbed = {}
            for i in range(q):
                gardenbed[i] = randint(0,maxberries)
            print ("Грядка: {0}".format({"Номер куста {0}".format(k):"{0} ягод".format(v) for k,v in gardenbed.items()}))
                
            def findBerriesNum(bed:dict,plantnum:int):
                l = len(bed.keys())
                if plantnum == 0:
                    return sum((bed[l-1],bed[0],bed[1]))
                elif plantnum == l-1:
                    return sum((bed[l-2],bed[l-1],bed[0]))
                else:
                    return sum((bed[plantnum-1],bed[plantnum],bed[plantnum+1]))
            
            def findPlant(bed:dict):
                m = 0
                rs = None
                for k in bed.keys():
                    num = findBerriesNum(gardenbed,k)
                    if num > m:
                        m = num
                        rs = k
                return (rs,m)
            
            plant, berries = findPlant(gardenbed)
            print("Чтобы собрать максимальное количество ягод, собирающий модуль нужно поставить у куста №{0}, соберем {1} ягод".format(plant,berries))
    elif task == 1:
        n = int(input("Введите, пожалуйста, целое число\n"))
        def getStringValue(num:int,notation:int):
            if notation > 10:
                raise NotImplementedError("Сорян, это в платной версии")
            else:
                rs = []
                while num > 0:
                    rs.insert(0,num%notation)
                    num = num//notation
                return "".join(map(str,rs))
        bnum = getStringValue(n,2)
        octnum = getStringValue(n,8)

        assert "0b" + bnum ==bin(n)
        assert "0o" + octnum ==oct(n)
        print("Значение числа в двоичной системе = {0}, в восьмеричной системе = {1}, с oct и bin сравнили, все ок".format(bnum,octnum))
    elif task == 2:
        p1 = input("Введите, пожалуйста, первый многочлен (используйте, пожалуйста, переменную 'x' и целые коэффициенты и показатели степени)\nПример полинома: 2x^2 + 4x + 5 = 0\n")
        p2 = input("Введите, пожалуйста, второй многочлен (используйте, пожалуйста, переменную 'x' и целые коэффициенты и показатели степени)\nПример полинома: 2x^2 + 4x + 5 = 0\n")

        def parsePolinomial(p:str):
            rs = {}
            regex =  r'[+-^]?\w+(?:\.\w+)?'
            monos = re.findall(regex,p.replace(" ",''))
            monos.pop()
            for i,mono in enumerate(monos):
                coef = 1
                power = 1
                if "x" in mono:
                    if mono == "x" or mono == "+x":
                        coef = 1
                    elif mono == "-x":
                        coef = -1
                    else:
                        coef = int(mono[:-1])
                    if i < len(monos) and "^" in monos[i+1]:
                        power = int(monos[i+1][1:])
                elif "^" in mono:
                    continue
                else:
                    coef = int(mono)
                    power = 0
                if power in rs:
                    rs[power] = rs[power] + coef
                else:
                    rs[power] = coef
            return rs           
        

        parsed1 = parsePolinomial(p1)
        parsed2 = parsePolinomial(p2)

        rs = {}
        for k,v in parsed1.items():
            if k in parsed2:
                s = v + parsed2[k]
                if s > 0:
                    rs[k] = s
            else:
                rs[k] = v
        for k,v in parsed2.items():
            if k not in parsed1:
                rs[k] = v
        print("+".join(["{0}{1}{2}".format("{0}".format(v if v > 1 else ""),"x" if k == 1 else "x^" if k != 0 else "",k if k > 1 else "") for k,v in rs.items()]))


                            
                        
                    
