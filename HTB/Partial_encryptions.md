Для начала нам необходимо зайти в функцию main. Попробовав провести статический анализ, я пришел к выводу, что это бесполезно и стоит провести динамический анализ
![main с функциями](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/partial_encryption/Func_in_main.PNG)
Немного покопавшись, я опознал функции проверки наличия аргументов, проверки введеных аргументов и функцию с флагом


Для начала нам необходимо зайти в функцию проверки введенного нами аргумента (в моем случае "proverka") и изменить вот эту хуету (спасибо моему корешу), отмеченную красной стрелкой на jl
![proverka](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/partial_encryption/jl.PNG)


После проверки пиздуем в следующую функцию, где по моим словам будет флаг, там я тоже пошаманил и дал названия вызовам, которые нас должны интересовать
![tut_flag](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/partial_encryption/here_will_be_flag.PNG)


Заходим в вызов адреса и видим там HTB{}
![HTB{}](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/partial_encryption/here_will_be_flag.PNG)


Дальше интереснее, но флаг палить не буду, сами дальше найдете
![Second_part](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/partial_encryption/second_part.PNG)
