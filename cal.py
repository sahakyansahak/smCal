import time
import RPi.GPIO as GPIO
import math
from sympy import *

L1 = 13
L2 = 19
L3 = 26
L4 = 16
L5 = 20 
L6 = 21

C1 = 24
C2 = 18
C3 = 23
C4 = 22
C5 = 27
C6 = 17
C7 = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(L5, GPIO.OUT)
GPIO.setup(L6, GPIO.OUT)


GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

x = Symbol("x")
y = Symbol("y")
z = Symbol("z")

keypad = [
["0","1","4","7","f()",">","<"],
["del","2","5","8","^","ln","sin"],
["//","//","//","//","sqrt","log","cos"],
[".","3","6","9", "x", "y","tan"],
["+","-","*","/","(","z","ctg"],
["=","modul","pi","kot",")","dz","aj"]]

kys = [">", "<", ".", "x", "y", "z", "(", "/", "*", "-", "+", "=", ")"]
ky_sin = ["sin", "cos", "tan", "ctg", "sqrt", "ln"]


def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        GPIO.output(line, GPIO.LOW)
        return (characters[0])
    if(GPIO.input(C2) == 1):
        GPIO.output(line, GPIO.LOW)
        return(characters[1])
    if(GPIO.input(C3) == 1):
        GPIO.output(line, GPIO.LOW)
        return(characters[2])
    if(GPIO.input(C4) == 1):
        GPIO.output(line, GPIO.LOW)
        return(characters[3])
    if(GPIO.input(C5) == 1):
        GPIO.output(line, GPIO.LOW)
        return(characters[4])
    if(GPIO.input(C6) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[5]
    if(GPIO.input(C7) == 1):
        GPIO.output(line, GPIO.LOW)
        return characters[6]
    GPIO.output(line, GPIO.LOW)
    return None
    

def send_line():
    if(readLine(L1, keypad[0])):
        return readLine(L1, keypad[0])
    if(readLine(L2, keypad[1])):
        return readLine(L2, keypad[1])
    if(readLine(L3, keypad[2])):
        return readLine(L3, keypad[2])
    if(readLine(L4, keypad[3])):
        return readLine(L4, keypad[3])
    if(readLine(L5, keypad[4])):
        return readLine(L5, keypad[4])
    if(readLine(L6, keypad[5])):
        return readLine(L6, keypad[5])
    else:
        return False


def mysin(a):
    return round(math.sin(math.radians(a)), 5)


def mycos(a):
    return round(math.cos(math.radians(a)), 5)


def mytan(a):
    return round(math.tan(math.radians(a)), 5)


def myctg(a):
    return round(math.tan(a) ** -1, 5)


def make_control(a):
    b = []
    z = 0
    l = ""
    k = ["+", "-", "*", "/", "=", '', "(" , "n", "t", "o", "s", "<", ">"]
    for i in range(len(a)):
        if(a[i] == "x" or a[i] == "y" or a[i] == "z"):
            if(a[i-1] not in k):
                if i - 1 > -1 and i not in b:
                    b.append(i)
            try:
                if(a[i+1] not in k and a[i+1] != ")" and i + 1 not in b):
                    b.append(i+1)
            except:
                pass
        elif(a[i] == "(" or a[i] == "s" or a[i] == "c" or a[i] == "t"):
            if(a[i-1] not in k and i not in b):
                if i - 1 > -1 :
                    b.append(i)

        try:
            if a[i] == ")" and a[i+1].isdigit():
                 b.append(i+1)
        except:
            pass
                
    a = list(a)
    for i in b:
        a.insert(i+z,"*")
        z+=1
    for i in a:
        l += i
    return l


def solve_pr(a):
    final_result = ""
    a = make_control(a)
    if("=" in a and a.count("=") == 1):
        if((len(a.split("=")) > 1 and (a.split("=")[1] == "")) and "x" not in a and "y" not in a and "z" not in a):
            final_result = str(eval(a[:len(a) - 1] + a[len(a):]))
        elif((len(a.split("=")) > 1 and (a.split("=")[1] != "")) and "x" not in a and "y" not in a and "z" not in a):        
            a1 = a.replace("sin", "mysin").replace("cos", "mycos").replace("tan", "mytan").replace("ctg", "myctg").split("=")[0]
            a2 = a.replace("sin", "mysin").replace("cos", "mycos").replace("tan", "mytan").replace("ctg", "myctg").split("=")[1]
            final_result = str(eval(a1) == eval(a2))
        elif((len(a.split(">")) > 1 and (a.split(">")[1] != "")) and "x" not in a and "y" not in a and "z" not in a):        
            a1 = a.replace("sin", "mysin").replace("cos", "mycos").replace("tan", "mytan").replace("ctg", "myctg").split("=")[0]
            a2 = a.replace("sin", "mysin").replace("cos", "mycos").replace("tan", "mytan").replace("ctg", "myctg").split("=")[1]
            final_result = str(eval(a1) > eval(a2))
        elif((len(a.split("<")) > 1 and (a.split("<")[1] != "")) and "x" not in a and "y" not in a and "z" not in a):        
            a1 = a.replace("sin", "mysin").replace("cos", "mycos").replace("tan", "mytan").replace("ctg", "myctg").split("=")[0]
            a2 = a.replace("sin", "mysin").replace("cos", "mycos").replace("tan", "mytan").replace("ctg", "myctg").split("=")[1]
            final_result = str(eval(a1) < eval(a2))
        elif("x" in a and "y" not in a and "z" not in a and (len(a.split("=")) > 1 and (a.split("=")[1] != ""))):
            results = solve(Eq(sympify(a.split("=")[0]), sympify(a.split("=")[1])), x)
            for i in results:
                final_result += str(i) + "  "
        elif("x" not in a and "y" in a and "z" not in a and (len(a.split("=")) > 1 and (a.split("=")[1] != ""))):
            results = solve(Eq(sympify(a.split("=")[0]), sympify(a.split("=")[1])), y)
            for i in results:
                final_result += str(i) + "  "
        elif("x" not in a and "y" not in a and "z" in a and (len(a.split("=")) > 1 and (a.split("=")[1] != ""))):
            results = solve(Eq(sympify(a.split("=")[0]), sympify(a.split("=")[1])), z)
            for i in results:
                final_result += str(i) + "  "

    elif("=" not in a):
        if("x" not in a and "y" not in a and "z" not in a):
            final_result = str(eval(a.replace("sin", "mysin").replace("cos", "mycos").replace("tan", "mytan").replace("ctg", "myctg")))

        elif (">" in a or ">=" in a or "<=" in a or "<" in a):
            if(("x" in a and "y" not in a and "z" not in a) or ("x" not in a and "y" in a and "z" not in a) or ("x" not in a and "y" not in a and "z" in a)):
                final_result = solve(sympify(a))

    print(final_result)



final_string = ""
pos = 0

try:
    print("STARTED")
    while True:
        final_key = ""
        if(send_line()):
            old_key = send_line()
            time.sleep(0.2)
            if(send_line() == old_key):
                time.sleep(0.3)
                if(send_line() == old_key):
                    if(send_line() == ">"):
                        final_key = ">="
                    if(send_line() == "<"):
                        final_key = "<="
                    if(send_line() == "sin"):
                        final_key = "asin"
                    if(send_line() == "cos"):
                        final_key = "acos"
                    if(send_line() == "tan"):
                        final_key = "atan"
                    if(send_line() == "ctg"):
                        final_key = "actg"
                    if(send_line() == "f()"):
                        final_key = "p()"
                    if(send_line() == "="):
                        solve_pr(final_string.strip())
                        final_string = ""
                        pos = 0
            else:
                final_key = old_key
                print(final_key)
            if((final_key) and (final_key.isdigit() or final_key in kys)):
                final_string = final_string[:pos] + final_key + final_string[pos:]
                pos += 1
                print(final_string + "                " + str(pos))
            if(final_key == "del"):
                #final_string = final_string[:pos - 1] + final_string[pos:]
                #pos -= 1
                if(pos > 0):
                    try:
                        if(final_string[pos - 2] in ["n", "s", "g"]):
                            final_string = final_string[:pos - 1] + final_string[pos:]
                            final_string = final_string[:pos - 2] + final_string[pos - 1 :]
                            final_string = final_string[:pos - 3] + final_string[pos - 2 :]
                            final_string = final_string[:pos - 4] + final_string[pos - 3 :]
                            pos -= 4
                        elif(final_string[pos - 2] in ["t", "a"]):
                            final_string = final_string[:pos - 1] + final_string[pos:]
                            final_string = final_string[:pos - 2] + final_string[pos - 1 :]
                            final_string = final_string[:pos - 3] + final_string[pos - 2 :]
                            final_string = final_string[:pos - 4] + final_string[pos - 3 :]
                            final_string = final_string[:pos - 5] + final_string[pos - 4 :]
                            pos -= 5
                        else:
                            final_string = final_string[:pos - 1] + final_string[pos:]
                            pos -= 1
                    except:
                        final_string = final_string[:pos - 1] + final_string[pos:]
                        pos -= 1
                print(final_string + "                " + str(pos))
            if((final_key) and final_key in ky_sin):
                final_string = final_string[:pos] + final_key + "()" + final_string[pos:]
                pos += len(final_key) + 1
                print(final_string + "                " + str(pos))
            if(final_key == "dz"):
                if(pos > 0):
                    try:
                        if(final_string[pos - 2] in ["n", "s", "g"]):
                            pos -= 4
                        elif(final_string[pos - 2] in ["t", "a"]):
                            pos -= 5
                        else:
                            pos -= 1
                    except:
                        pos -= 1
                print(final_string + "                " + str(pos))
            if(final_key == "aj"):
                if(len(final_string) > pos):
                    try:
                        if(final_string[pos] in ["s", "c", "t"] and final_string[pos + 1] != "q"):
                            pos += 4
                        elif(final_string[pos] in ["a", "s"]):
                            pos += 5
                        else:
                            pos += 1
                    except:
                        pos += 1
                print(final_string + "                " + str(pos))
except KeyboardInterrupt:
    print("\nApplication stopped!")
