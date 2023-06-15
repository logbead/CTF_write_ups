Короче, это один из самых всратых тасков на данный момент. Объясню 2 способа. Первый - мой способ, второй - нормальный.
<br>Первым делом я закинул в Иду, чтобы посмотреть его код, но увидел расширение .NET, после чего я посмотрел в Калюхе, что из себя представляет файл.
![File_checking](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bypass/0.PNG)

<br>Начнем с моего способа. <br>Я закинул файл в OLLYDBG и запустил отладку
![Старт Программы](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bypass/1.PNG)

<br>После этого я ввел данные и остановил программу
![Ввод данных и остановка программы](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bypass/2.PNG)

<br>Перешел по адресу введенных данных
![Дамп введенных данных](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bypass/3.PNG)

<br>И просто просматривал хексы в надежде увидеть флаг. Я его нашел, он там появляется несколько раз и в разных кодировках (то есть в ascii будет так убого все высвечиваться, как на картинке, но флаг можно будет
увидеть и выше, но в unicode один раз виден флаг, зато более отчетливо. В душе не чаю, зачем это говорю)
![Смотр hex'oв](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/bypass/4.PNG)
