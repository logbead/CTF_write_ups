Так, первый средний таск.
<br>Все, в принципе не сложно. Скачиваем elf файл, закидываем в "elf parser" т видим, что есть anti-debug на ptrace.
![ptrace](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bombslanded/1.PNG)
<br>Будем решать через edb. Запускаем и методом проб и ошибок понимаем, что anti-debug является второй вызываемой функцией с точки входа, а hlt не позволяет выполнить
следующие действия, так как функцию мы будем nop'ать
![anti-debug](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bombslanded/2.PNG)
<br>Дальше у нас будут прыжки в нужные функцие, которые необходимо будет выполнить, если проигнорить отмеченный 
пыржок, то у нас будет сравнение с X. Это будет неправильно, так как наша программа имеет ложные прыжки, 
проверки и изменяется по ходу выполнения. Следовательно, мы должны перепрыгнуть данную проверку на адрес 0х8048а13
![first_jmp](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bombslanded/3.PNG)
<br>Немного покопавшись, я увидел, что вызывается еах, в котором находится адрес функции, которая отвечает
за ввод пароля в строку.
![еах](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bombslanded/4.PNG)
<br>После ввода, я выяснил, что будет сравнение строки по определенному количчеству символов
![strncmp](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bombslanded/5.PNG)
<br>И последнее, что необходимо понять, так это то, что нам будут даваться определенные символы, которые будут ксориться. На картинке мы видим цикл (1) (в котором проиходит хор),
введенный мною значение "ablalalabla" (2) и сравнение с самим флагом (3).
![flag](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bombslanded/6.PNG)
<br>Таск несложный, как я и говорил, но требует немного времени
