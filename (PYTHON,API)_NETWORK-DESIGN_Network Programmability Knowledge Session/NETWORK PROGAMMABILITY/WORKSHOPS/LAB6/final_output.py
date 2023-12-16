import os
from my_apic_em_functions import *
from path_trace import doPathTrace
from get_colors import color

os.system("cls")

def doChoose():
    print(color.GREEN+"CISCO APIC-EM:"+color.END)
    print(color.CYAN+"*Type 'clear' to clear all."+color.END)
    print(color.YELLOW+"""
    [1] SHOW TICKET
    [2] SHOW HOSTS
    [3] SHOW NETWORK DEVICES
    [4] DO PATH TRACE
          """+color.END)
    numChoose = raw_input("CHOOSE: ")
    if numChoose == "clear":
        os.system('cls')
        doChoose()
    try:
        numChoose = int(numChoose)
    except:
        print(color.RED+"Warning: Please input a number"+color.END)
        doChoose()
    if numChoose == 1:
        print(color.BOLD+"TICKET: " + get_ticket()+color.END)
    elif numChoose == 2:
        print(color.BOLD+"LIST OF HOSTS:"+color.END)
        print_hosts()
    elif numChoose == 3:
        print(color.BOLD+"LIST OF NETWORK DEVICES:"+color.END)
        print_devices()
    elif numChoose == 4:
        doPathTrace()
    else:
        print(color.RED+"Pick only between 1 to 3."+color.END)
        doChoose()

    doChoose()

doChoose()
