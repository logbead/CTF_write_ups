При открытии таска, не долго думая, сразу же зашел в строки и увидел, что программа написана на питоне, 
соответственно необходимо воспользоваться распаковщиком Pyinstaller, который я нашел где-то в интернете.
![pyinstaller](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Maze/Python.PNG)

<br><br>
При распакоуке я заметил, что pyinstaller не смог разархивировать PYZ-файлы и просит использовать Python3.8. <br>Без проблем
![Decompress](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Maze/2.PNG)

<br><br>
В папке с распакованными файлами видим "maze.pyc". Pyc-файлы по-сути являются обфусцированным питоновским кодом. 
Но нет никаких проблем их деобфусцировать с помощью decompyle3 и вывести их в *.py
![pyc](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Maze/3.PNG)
<br><br>
![decompyle3](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Maze/4.PNG)

<br><br>
Код maze.py представлен ниже и можем увидеть вызов библиотеки obf_path при вводе "Y0u_St1ll_1N_4_M4z3", если вводим 
что-то другое, то у нас распаковывается файл и программа пишет, что у нас есть второй лабиринт. Естественно он не работает и жизнь хуйня с этими всеми файлами. Сидишь с ними, 
как дурачок с фантиками
```python
import sys, obf_path
ZIPFILE = "enc_maze.zip"
print("Look who comes to me :)")
print()
inp = input("Now There are two paths from here. Which path will u choose? => ")
if inp == "Y0u_St1ll_1N_4_M4z3":
    obf_path.obfuscate_route()
else:
    print("Unfortunately, this path leads to a dead end.")
    sys.exit(0)
import pyzipper

def decrypt(file_path, word):
    with pyzipper.AESZipFile(file_path, "r", compression=(pyzipper.ZIP_LZMA), encryption=(pyzipper.WZ_AES)) as extracted_zip:
        try:
            extracted_zip.extractall(pwd=word)
        except RuntimeError as ex:
            try:
                try:
                    print(ex)
                finally:
                    ex = None
                    del ex

            finally:
                ex = None
                del ex


decrypt(ZIPFILE, "Y0u_Ar3_W4lkiNG_t0_Y0uR_D34TH".encode())
with open("maze", "rb") as file:
    content = file.read()
data = bytearray(content)
data = [x for x in data]
key = [0] * len(data)
for i in range(0, len(data), 10):
    data[i] = (data[i] + 80) % 256

for i in range(0, len(data), 10):
    data[i] = (data[i] ^ key[i % len(key)]) % 256

with open("dec_maze", "wb") as f:
    for b in data:
        f.write(bytes([b]))
```
В папке PYZ есть файл obf_path.pyc. Соответственно делаем те же самые действия и получаем код
```python
def obfuscate_route():
    from marshal import loads
    exec(loads(b'\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00@\x00\x00\x00s(\x00\x00\x00d\x00d\x01l\x00Z\x00d\x00d\x01l\x01Z\x01e\x02e\x00\xa0\x03e\x01\xa0\x03d\x02\xa1\x01\xa1\x01\x83\x01\x01\x00d\x01S\x00)\x03\xe9\x00\x00\x00\x00Ns4\x03\x00\x00\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x02\xf6x\x9c\xedV[o\xd30\x14\xfe+^_\xd6\x02+Kz\xdf\x18\x9a\xe0\x01\x8d\x07@\x82\xa7)R\xe5\xc4\'\xa9\xb7\xd4\x8elgk#~<\xc7\x8e=\xba\xb6\x13\x9ax\xe9C#\xc5\xf9\xce\xfd\xf8\xf3q\xd5\xf9\\A\x91J\xad\xe7\xf8\x1c*\xbc\xea\x1cB\x17\xff\x84\x9d\xcbC\xe8\xe2\xc8\xe6\x91\xcd}l\xc2\n\xb2n))\xd3\xdd\xb4\x93\xac`\x90\xac\xce\xcf\xff\xf3\x1do\xca\xd7\x9b\x82\xc6\n\xd3M\x05\x0bKTZt\xbb\xab\x8b\xac.z\xd2\xc5V\x17/q\x19X\x83m7\xb26\xb0\xe0\x0e\x97!ksG\xb3\x90p\x04\xad\x86\xfa\xdeh\x14,\x13\x16\xf2L-\x1aZ\xc7\xd1\xbd\xf5R\xbf 1V7JV\xd3P\xc4\x17r\xfa\xf1\xae\xde\x01,"|\x074\xda\xb6\x9f\xdf\xb5\x19]\'\xe9\x8e&\xb3\x9a\x89]\xa6>:\x0eY\xf4o_w\xf2\xfa\xba\n\xc2\x06\xa7>8\xf6\x05a\x93\x8c\xdc\xba\xe5,1\x81;/\x8b \xe3w\xb2\xa1\xc7\x1d\xbch\xc9\xb6-X j\xa9S/\x10\n\xfb66\xb0\x96|\x7f\x84\xcd\x87K\xb2\x9a\xa5~8"\xb4\xceX;\x15{#\xe2\xd7\x92\xe7\xa6\xf0\xa7E=\x0c\xc7P\x98m\xcf\xfb\xb7^\xeb\xcc\xa8=I]\x02T\x8d\xa5zI\x1b\xe8W\xa2\xb0\xc2\xa0_\xad\x9b\xb3\x9bBH\xc5EA\xcc\x02H\xa5dZ\xc2\x92<Jqj\xc8\x92\xde\x03\xe1\x860\xaeiU\x01U\x97\xcdU&E\xae\xa406\x82\nF(c\n\xb4\xb6"zr\xed\xd2\x18Uc.j\x16\xc4H\x82fY\xd6\x86K\xd1o\xbe~\xbfG\x07jN5)\xa4d$\xad\r\xb9!E\x8d\x19\x9c\x9e\xd4D/d]2"\xe4#F\x9aZ\t\x82\xf5\x96\xbe;x\xe0\xb2\xd6.\xb5\xdf[\xacR\x8e0jyl7\xcf\xaf\xedxx\xfcc\x03\xb7\x9c\x06\xb19C,\xbe \x9f\'\'d-k\x92\xb9\xca\xa03Z\x81+(\xd3\xbcF\xc9\x00s%\x91\xb4(5\x96\x14\xb3\xc0\x9dr\xcb\xd0\x9a,\xa0\xacl\xf8\x05\xf1\x07\x11o\x1eD\xe3n\xa5\xd0\x00\xac\xdb\xbc\xed%"\x97\x8ap\xc2\x05QT\x14\xd0\x1d\xe0!^$\x82\xe0\x83\n\xc6\x85\xe9\x0e\xe2wQ<B\xd7\xe6\xfd\' \x9f\xa9\x82\xbc.O\xf0q=)Y\x1bh9Y\x80\x02K\xb9\x90\x86h\x9aC\xbf\xd7N[K\x8c\xd4\x1e\r\xf4:\xc0\xa1\xe1KP\xdb=\x06#U\xc5C\xc0\x1b\x14\x8f\x0b0\xd9#\xb3\x97%\xcaj\xa5@\x989\xe3\n2#\xd5\xfa6\x11\\0X\xcds^B\x98\xb7\n\x07\xca\x84L\xb0\xe2\x01\x8f\x11k\xf3\xd4\xcc\x9d\xe4"`Y\xc1\x13V@YH\xe5\x92\x07\x83e\x11\xcf\xd0M\xbbjG\xff\xef.v\x14>j\x92I\x86\x94)/N?,Q.\xe1c\xb8M\xe1\xd5o\x9e\x07\xdbK\xec<2\xc7\x97\xf0\xd2\xd4\x7f\x87\x9e\xc5\xe9\x96\xbe\xfdz\xefh\xbcO\xdb^p\xb27\xf0y\x01\xffk\x9b\xe7.t\x14\xac\x9d^\xef\xf8\x87\xe3\xf8\xf7\xed@a\xe7\x0f\xdc9\x01G\x00\x00(\xe3\xdf}\x13\x01@\xad\x00\x01\x8f\x06\xf7\x05\x00\x00\x85k\x89\xbe\xb1\xc4g\xfb\x02\x00\x00\x00\x00\x04YZ)\x04\xda\x04zlib\xda\x04lzma\xda\x04exec\xda\ndecompress\xa9\x00r\x06\x00\x00\x00r\x06\x00\x00\x00\xda\x07coduter\xda\x08<module>\x01\x00\x00\x00s\x02\x00\x00\x00\x10\x01'))
```

<br><br>
За следующий шаг хочу выразить большую благодарность [этому райтапу](https://pugachev.io/2024/03/22/maze-by-hack-the-box/), иначе я бы хуй че сделал и в жизни не догадался до такого.
<br>
Смысл в том, что программа выглядит в виде исполняемых байтов, но автор задался вопросом, как вернуть программе исходный вид
Я добавлю программу в файлы, посмотрите на райтап и на программу, чтобы понять где и что измененно ([ПРОГРАММА](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Maze/py_comp.py))

<br><br>
После распаковки видно, что код запакован с использованием библиотек zlib, lzma. Мы не пальцем деланные и возвращаем программе исходный код:
```python
import zlib, lzma

# Сжатые данные
data = b'\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x02\xf6x\x9c\xedV[o\xd30\x14\xfe+^_\xd6\x02+Kz\xdf\x18\x9a\xe0\x01\x8d\x07@\x82\xa7)R\xe5\xc4\'\xa9\xb7\xd4\x8elgk#~<\xc7\x8e=\xba\xb6\x13\x9ax\xe9C#\xc5\xf9\xce\xfd\xf8\xf3q\xd5\xf9\\A\x91J\xad\xe7\xf8\x1c*\xbc\xea\x1cB\x17\xff\x84\x9d\xcbC\xe8\xe2\xc8\xe6\x91\xcd}l\xc2\n\xb2n))\xd3\xdd\xb4\x93\xac`\x90\xac\xce\xcf\xff\xf3\x1do\xca\xd7\x9b\x82\xc6\n\xd3M\x05\x0bKTZt\xbb\xab\x8b\xac.z\xd2\xc5V\x17/q\x19X\x83m7\xb26\xb0\xe0\x0e\x97!ksG\xb3\x90p\x04\xad\x86\xfa\xdeh\x14,\x13\x16\xf2L-\x1aZ\xc7\xd1\xbd\xf5R\xbf 1V7JV\xd3P\xc4\x17r\xfa\xf1\xae\xde\x01,"|\x074\xda\xb6\x9f\xdf\xb5\x19]\'\xe9\x8e&\xb3\x9a\x89]\xa6>:\x0eY\xf4o_w\xf2\xfa\xba\n\xc2\x06\xa7>8\xf6\x05a\x93\x8c\xdc\xba\xe5,1\x81;/\x8b \xe3w\xb2\xa1\xc7\x1d\xbch\xc9\xb6-X j\xa9S/\x10\n\xfb66\xb0\x96|\x7f\x84\xcd\x87K\xb2\x9a\xa5~8"\xb4\xceX;\x15{#\xe2\xd7\x92\xe7\xa6\xf0\xa7E=\x0c\xc7P\x98m\xcf\xfb\xb7^\xeb\xcc\xa8=I]\x02T\x8d\xa5zI\x1b\xe8W\xa2\xb0\xc2\xa0_\xad\x9b\xb3\x9bBH\xc5EA\xcc\x02H\xa5dZ\xc2\x92<Jqj\xc8\x92\xde\x03\xe1\x860\xaeiU\x01U\x97\xcdU&E\xae\xa406\x82\nF(c\n\xb4\xb6"zr\xed\xd2\x18Uc.j\x16\xc4H\x82fY\xd6\x86K\xd1o\xbe~\xbfG\x07jN5)\xa4d$\xad\r\xb9!E\x8d\x19\x9c\x9e\xd4D/d]2"\xe4#F\x9aZ\t\x82\xf5\x96\xbe;x\xe0\xb2\xd6.\xb5\xdf[\xacR\x8e0jyl7\xcf\xaf\xedxx\xfcc\x03\xb7\x9c\x06\xb19C,\xbe \x9f\'\'d-k\x92\xb9\xca\xa03Z\x81+(\xd3\xbcF\xc9\x00s%\x91\xb4(5\x96\x14\xb3\xc0\x9dr\xcb\xd0\x9a,\xa0\xacl\xf8\x05\xf1\x07\x11o\x1eD\xe3n\xa5\xd0\x00\xac\xdb\xbc\xed%"\x97\x8ap\xc2\x05QT\x14\xd0\x1d\xe0!^$\x82\xe0\x83\n\xc6\x85\xe9\x0e\xe2wQ<B\xd7\xe6\xfd\' \x9f\xa9\x82\xbc.O\xf0q=)Y\x1bh9Y\x80\x02K\xb9\x90\x86h\x9aC\xbf\xd7N[K\x8c\xd4\x1e\r\xf4:\xc0\xa1\xe1KP\xdb=\x06#U\xc5C\xc0\x1b\x14\x8f\x0b0\xd9#\xb3\x97%\xcaj\xa5@\x989\xe3\n2#\xd5\xfa6\x11\\0X\xcds^B\x98\xb7\n\x07\xca\x84L\xb0\xe2\x01\x8f\x11k\xf3\xd4\xcc\x9d\xe4"`Y\xc1\x13V@YH\xe5\x92\x07\x83e\x11\xcf\xd0M\xbbjG\xff\xef.v\x14>j\x92I\x86\x94)/N?,Q.\xe1c\xb8M\xe1\xd5o\x9e\x07\xdbK\xec<2\xc7\x97\xf0\xd2\xd4\x7f\x87\x9e\xc5\xe9\x96\xbe\xfdz\xefh\xbcO\xdb^p\xb27\xf0y\x01\xffk\x9b\xe7.t\x14\xac\x9d^\xef\xf8\x87\xe3\xf8\xf7\xed@a\xe7\x0f\xdc9\x01G\x00\x00(\xe3\xdf}\x13\x01@\xad\x00\x01\x8f\x06\xf7\x05\x00\x00\x85k\x89\xbe\xb1\xc4g\xfb\x02\x00\x00\x00\x00\x04YZ' 

# Декомпрессия
decompressed = zlib.decompress(lzma.decompress(data))

# Печатаем результат
print(decompressed.decode('utf-8'))
```
<br><br>
После всей этой невероятной магии мы получаем очередную байтовую хуйню, но я просто закинул это все говно [снова сюда](https://github.com/logbead/CTF_write_ups/blob/main/HTB/pictures/Maze/py_comp.py).
После этого у нас получился самый исходный код этой программы: 
```python
import os, sys
from time import sleep
path = sys.argv[0]
current_directory = os.getcwd()
index_file = "maze.png"
if ".py" in path:
    print("Ignoring the problem won't make it disappear;")
    print("confronting and addressing it is the true path to resolution.")
    sys.exit(0)
if not os.path.exists(os.path.join(current_directory, index_file)):
    print("Ok that's good but I guess that u should now return from the previous path")
    sys.exit(0)
index = open(index_file, "rb").read()
seed = index[4817] + index[2624] + index[2640] + index[2720]
print("\n\nG00d!! you could escape the obfuscated path")
print("take this it may help you: ")
sleep(2)
print(f"\nseed({seed})\nfor i in range(300):\n    randint(32,125)\n")
print("Be Careful!!!! the route from here is not safe.")
sys.exit(0)
```
Соответственно там был намек на решение в виде
```
seed(x)
for i in range(300):
    randint(32,125)
```
Я посмотрел программу maze.py, увидел, 
что там есть переменная key и понял, что надо с этим работать. Изменил эту переменную
```
key = []
random.seed(x)
for i in range(300):
    key.append(random.randint(32,125))
```
И в конце концов получил работающий файл с архива, который можно было использовать и работать с ним в IdaPro
