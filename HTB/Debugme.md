Этот таск был посложнее. Первым делом надо поставить бряку, чтобы программа не выдала ошибку сразу же
![breakpoint](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/debugme/1.PNG)
<br><br>Дальше идем реверсить динамикой и замечаем прыжки, которые выводят программу на выход, следовательно нам надо обойти все 
эти прыжки, изменяя инструкции
![jnz](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/debugme/2.PNG)
![exit](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/debugme/3.PNG)
<br><br>В конце концов нам надо дойти до мэйна, в котором будет ассемблерный код
![_main](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/debugme/4.PNG)
![asm](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/debugme/5.PNG)
<br><br>Здесь опять мы видим прыжки, которые выводят программу на выход, что нас категорически не устраивает
![jump](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/debugme/6.PNG)
![exit](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/debugme/7.PNG)
<br><br>Когда пройдем почти весь код каких-то вычислений, то можем увидеть странный loop, который может насторожить
![loop](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/debugme/8.PNG)
Решение дал, надо только понять, что это за loop и как исправить этот несуразный момент
