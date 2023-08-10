from random import randint
import os.path
import json

task = int(input("Введите номер задачи, которую вы хотите проверить (34,36) или доп. задачи (1)\n"))
if task not in [34,36,1,2,3]:
    print("Вы ввели значение {0}, такой задачи не было в домашнем задании".format(task))
else:
    if task == 34:
        def count_vowels(s):
            counter = 0
            vowels = "ёуеыаоэяию"
            for c in s:
                if c in vowels:
                    counter +=1
            return counter
        
        poem = input("Введите, пожалуйста, стихотворение Винни-Пуха\n")
        def test_poem(poem):        
            counter = None
            for phrase in poem.split(" "):
                if counter is None:
                    counter = count_vowels(phrase)
                if counter != count_vowels(phrase):
                    return "Пам парам"
            return "Парам пам-пам"
        print(test_poem(poem))
    elif task == 36:
        def get_operation():
            d={}
            s_oper = input("Введите, пожалуйста, лямбда функцию от двух переменных\n")
            exec(f"f={s_oper}",d)
            return d["f"]
        
        def get_operation_table(operation,num_rows=6,num_columns=6):
            rs = []
            for i in range(num_rows):
                rs.append([])
                for j in range(num_columns):
                    rs[i].append(operation(i+1,j+1))
            return rs
        
        def show_table(table):
            for row in table:
                print(*row)

        f = get_operation()
        print("Получили следующую таблицу:")
        show_table(get_operation_table(f))
    elif task == 1:
        base = None
        if os.path.isfile("base.json"):
            try:
                base = json.load(open("base.json","r"))
            except:
                pass
        if base is None:
            base = {"illnesses":{},"symptoms":{},"diagnosys":[]}
            base["illnesses"]["Шизофрения"] = [
                "Вы слышите звучание собственных мыслей?",
                "Вы слышите галлюцинаторные голоса?",
                "У вас есть устойчивые бредовые идеи?"
            ]
            base["illnesses"]["Депрессия"] = [
                "У вас подавленое настроение, не зависящее от обстоятельств, в течение длительного времени?",
                "Вы потеряли интерес или удовольствие от ранее приятной деятельности?",
                "Вы сталкиваетесь с выраженной утомляемостью, упадком сил?"
            ]
            base["illnesses"]["Умственная отсталость"] = [
                "У вас недоразвита эмоционально-волевая сфера?",
                "Вы страдаете энурезом?",
                "Ваше сенсорное развитие значительно острает по срокам формирования?"] 
        flag = False
        while True:
            if not flag:
                print ("Нажмите /start чтобы начать /stop, если вы не хотите знать правду, /help - получить помощь, y/n - для ответа на вопросы")
                flag = True
            command = input()
            if command == "/start":
                if len(base["diagnosys"]) > 0:
                    print ("О, вы у нас уже не в первый раз, ложитесь на кушеточку")
                    print ("На прошлом сеансе вы ответили положительно на следующие вопросы: ")
                    for symptom,value in base["symptoms"].items():
                        if value == True:
                            print (symptom)
                    print ("И я поставил вам следующие диагнозы:")
                    for diagnosys in base["diagnosys"]:
                        print (diagnosys)
                    print ("Посмотрим, изменилось ли что-то...")
                else:
                    print ("О, вы у нас первый раз, но я уверен, что вы здесь не случайно")
            if command == "/stop":
                print ("Куда же вы? Подождите! Эй, санитары, хватай его!!!!")
                break
            if command =="/help":
                print ("/ask - начать диагностику")
                print ("/diag - получить диагноз")
            if command == "/ask":
                print ("Отвечайте y/n на каждый вопрос")
                for illness in base["illnesses"]:
                    counter = 0
                    for question in base["illnesses"][illness]:
                        rs = input(f"{question} (y/n)") == "y"
                        if rs:
                            base["symptoms"][question] = rs
                            counter +=1
                    if counter >=2:
                        base["diagnosys"].append(illness)
                json.dump(base,open("base.json","w+"))
            if command == "/diag":
                if len(base["diagnosys"]) > 0:
                    print ("К счастью, вы больны, вот ваши диагнозы:")
                    for d in base["diagnosys"]:
                        print (d)
                else:
                    print ("К сожалению, вы здоровый человек")

     

                        
                    
