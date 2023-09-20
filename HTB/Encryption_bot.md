Таск несложный, но, как мне кажется, решить его статическим анализом невозможно, но я постараюсь объяснить.
<br>Запустив файл в иде мы видим кучу функций, но большая часть из них бесполезна. <br>Так как таск я решил, мы пойдем только по необходимым функциям и без воды.
![funcs](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Encryption_bot/1.PNG)

<br>Пойдем по порядку. Нумерацию функций, по которым мы почапаем, я закоментировал.
<br>В первой функции мы видим проверку количества символов в строке. Она равна 27. Следовательно, мы должны вводить 27 символов.
![strlen](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Encryption_bot/2.PNG)

<br>Вторая функция имеет подфункцию. Сама функция выбирает крайний символ из строки.
![2](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Encryption_bot/3.PNG)
А подфункция переводит символ в двоичный код, сохраняя количество чисел в двоичной системе(8)
![10101010](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Encryption_bot/4.PNG)

<br>После этого всего, программа разбивает двоичный код по 6 разрядов.
![101010](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Encryption_bot/5.PNG)
Далее в функции sub_13AB идет перевод в десятичную систему счисления 6-ти разрядных чисел
![sub_13AB](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Encryption_bot/6.PNG)
<br>И в конце идет подставление полученного значения по индексу в строке
![alphabet](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Encryption_bot/7.PNG)

<br><br>В итоге, что мы имеем... программа сначала проверяет на количество символов, которые мы вводим, затем переводит данную строку в двоичный код по 8 разрядов и шифрует данный код по 6 разрядов.
<br>Пишем программу
<br><br>
```python
a = 'RSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQabcdefghijklmnopqrstuvwxyz'
b = '9W8TLp4k7t0vJW7n3VvMCpWq9WzT3C8pZ9Wz'
d=0
res=''
f=[]
l=''
x=list(a)
y=list(b)
for i in range (0,len(y)):
    c=y[i]
    if c in x:
        d=x.index(c)
        e=str(format(d,'b'))
        while len(e)<6:
            e='0'+e
        l += e
l=[l[i:i+8] for i in range(0, len(l), 8)]
for i in range (0, len(l)):
    d=l[i]
    d=int(d, base=2)
    d=chr(d)
    res+=d
print(res)
```
