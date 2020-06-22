    ### SCOOTER 1.0 ###

#Assembled With:

	#Python 3.8.3
	#cx_Freeze 6.1

#Caveat
	
	# Due to complications with cx_Freeze and my installation of Python, I’m now 
    # using an older version of Python (3.7.7) which I installed with Homebrew. 
    # For that reason, running the script using Python 3.8 might produce slightly 
    # different results. It should still be perfectly functional either way.

	# This code is deceptively long due to other complications with tkinter 
    # itself. I experimented with using combinations of classes, methods, 
    # and nested if statements but found that those would not run properly 
    # with the way tkinter is setup. The main three issues are as follows: 

	#     1) A tkinter window and its components must be in the same statement. 
    #       That is that that you cannot separate them with if statements or 
    #       hide widgets inside a function.

	#     2) Certain tkinter components can’t be used in a function/method 
    #       at all. The main one that can’t be used as a command, much to my 
    #       dismay, is Combobox. Those are the pretty dropdown boxes.

	#     3) You cannot, to my knowledge and experimentation, define a variable
    #       using the attributes from an object. This makes classes not 
    #       particularly useful in this case.

	# That being said, I am open to any suggestions/fixes to these issues. 
    # Scooter is still very much a work in progress, as far as I’m concerned.
      
    # If you read through all of this script you’ll find a staggering amount of
    # redundancy! 

    # I hope this documentation will help you understand the architecture of 
    # this script without too much trouble.

### DESCRIPTION: ###

    # Scooter is a new alternative to the Splitter we’ve all come to know 
    # and love! It allows complete control over the split you’re generating
    # by showing immediate tallies of how many orders each Logi would get if 
    # they had slightly different letters. To put it simply: if Splitter 1.01 is
    # a self-driving car and splitting manually is driving stick, Scooter is 
    # like driving your first automatic. 

### HOW TO: ###

    # 1) Run splitter query as normal, either through PopSQL or the Snowflake
    # entry point.
    # 2) Export the results as a CSV file.
    # 3) Boot up Scooter 1.0.
    # 4) Hit “Choose file” and select the split you just exported.
    # 5) Enter the number of Logi’s and hit “Initialize”.
    # 6) Three windows will pop up. The left one, “Scooter 1.0”, is where you
    #   select each Logi’s letters. The right one, “Handlebars”, has a list of 
    #   each Metro’s order tally for easy reference. The third is a terminal 
    #   which will display any error messages. Please copy and paste those in a 
    #   DM to me if you run into any debilitating errors! 
    # 7) Choose each Logi’s letters using the dropdown menus and hit 
    #    “Generate when you’re done. Best practice is to start from the bottom and 
    #    work your way up. After each Logi has letters, it becomes very easy to scoot
    #    the results to your liking!
    # 8) A final window, “Scooted”, will pop up with your completed split. 
    #    The text in the window is editable so it’s easiest to type everybody’s 
    #    names and the day’s schedule here so that you can just copy and paste 
    #    the split into Slack when it’s done. 

### FLOW: ###

    # >User boots up Scooter 

    # > root window (“Initializing Scooter”) appears, with a file name 
    #       Text box (filedisplay), a button (fileopen, “Choose file”), 
    #       a Combobox (firstchoice), and a second button (initialize)
    # > User hits fileopen to choose their file, which then starts the 
    #       function filechooser():

    #         >filechooser() opens a file selection menu 
    #           (filename = filedialog.askopenfilename), where the User selects 
    #           their csv file 
    #         > User’s csv file is read using the csv.reader(open()) function
    #         > results from csv file are split into three lists: 
    #           metro_list, order_list, order_list_str (duplicate of order_list 
    #           but in str format)
    #         > filelocation (the text for Text: file display) is set to filename

    #         > numbers_list is generated using a list comprehension based 
    #           on the length of metro_list
    #         > numbered_metro_list  is formed by combining numbers_list 
    #           and metro_list with a list comprehension
    #         > helpertext is formed by combining numbered_metro_list 
    #           and order_list with a list comprehension

    # > User returns to the root window (“Initializing Scooter”) and 
    #       selects the number of Logi’s (firstchoice) 
    # > User confirms selection by hitting “Generate” button, 
    #       which starts the function logi_numerizer():

    #       > logi_numerizer() then sets all input/ordertotal variables to 
    #           global, meaning that any changes made inside of this function 
    #           are universal

    #       > logi_numerizer() opens helper window (“Handlebars”), with a for 
    #           loop to insert the text from helpertext (the list that was a 
    #           combination of numbered_metro_list and order_list_str), 
    #           then disables the text window so user may not type in it
    
    #       > logi_numerizer() opens one of twelve versions of the 
    #           branch window (“Scooter 1.0”), based on the results of 
    #           firstchoice.get() (the “Initialize” button) 

    # > branch window consists of the following:
        
    #    (firstchoice.get() # of logi rows consisting of ):

    #       label_x (Logi’s #) | option_x (dropdown menu which affects input_x 
    #       and starts function select_x/select_xp) | display_x label 
    #       (order tally, value is set by function in option_x)

    #       final row with a button (“generate”) in the  right corner

    # > User selects options using option_x dropdown menus
    # > any time a dropdown menu is used, select_x() / select_x() 
    #       and scoot_x() / scoot_xp() are started:
        
    #           > select_x() calculates the order tally (text in display_x) 
    #               by finding sum of the range of numbers from the index 
    #               number of the current value of input_x to the current value
    #               of input_y (the next dropdown menu) and converting it to 
    #               a string which it then sets as ordertotal_x

    #           > scoot_x() does the same but is triggered when the dropdown menu 
    #               below is changed (I.e. if you changed option_four it would 
    #               trigger scoot3 so that the order tally will automatically 
    #               adjust either way) 

    #           >select/scoot_xp are copies of the same functions that use the 
    #               index number of the last dropdown menu (which is named 
    #               label/option/input/display_last) instead of the next number 
    #               value’s (I.e. instead of checking for the sum of the 
    #               range of order tallies from input_three to input_four, 
    #               it checks for the sum for input_three to input_last) 

    #           > the p is for “penultimate”, isn’t that fun?

    # > Once User is done scooting, they hit the “Generate” button, 
    #       which starts finisher():
        
    #           > finisher() opens a final window, (result, “Scooted”)

    #           > finisher() declares a string variable named split and 
    #               inserts the selected metro for each logi (found by 
    #               using the index number to return the metro from input_x but 
    #               from metro_list so it doesn’t have the number) and the order 
    #               tallies (using ordertotal_x(get)) into a prewritten 
    #               blank split 

    #           > finisher() closes the branch and helper windows

    # > fin

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import csv


def select1(event):
    ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))

def select1p(event):
    ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_last.get())])))    

def scoot1(var, indx, mode):
    ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))

def scoot1p(var, indx, mode):
    ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_last.get())])))


def select2(event):
    ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())])))

def select2p(event):
    ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_last.get())])))    

def scoot2(var, indx, mode):
    ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())])))

def scoot2p(var, indx, mode):
    ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_last.get())])))


def select3(event):
    ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))

def select3p(event):
    ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_last.get())])))    

def scoot3(var, indx, mode):
    ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))

def scoot3p(var, indx, mode):
    ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_last.get())])))


def select4(event):
    ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())])))

def select4p(event):
    ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_last.get())])))    

def scoot4(var, indx, mode):
    ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())])))

def scoot4p(var, indx, mode):
    ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_last.get())])))


def select5(event):
    ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))

def select5p(event):
    ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_last.get())])))    

def scoot5(var, indx, mode):
    ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))

def scoot5p(var, indx, mode):
    ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_last.get())])))


def select6(event):
    ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))

def select6p(event):
    ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_last.get())])))    

def scoot6(var, indx, mode):
    ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))

def scoot6p(var, indx, mode):
    ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_last.get())])))


def select7(event):
    ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))

def select7p(event):
    ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_last.get())])))    

def scoot7(var, indx, mode):
    ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))

def scoot7p(var, indx, mode):
    ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_last.get())])))


def select8(event):
    ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))

def select8p(event):
    ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_last.get())])))    

def scoot8(var, indx, mode):
    ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))

def scoot8p(var, indx, mode):
    ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_last.get())])))


def select9(event):
    ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))

def select9p(event):
    ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_last.get())])))    

def scoot9(var, indx, mode):
    ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))

def scoot9p(var, indx, mode):
    ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_last.get())])))


def select10(event):
    ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))

def select10p(event):
    ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_last.get())])))    

def scoot10(var, indx, mode):
    ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))

def scoot10p(var, indx, mode):
    ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_last.get())])))


def select11(event):
    ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))

def select11p(event):
    ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_last.get())])))    

def scoot11(var, indx, mode):
    ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))

def scoot11p(var, indx, mode):
    ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_last.get())])))


def select12(event):
    ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))

def select12p(event):
    ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_last.get())])))    

def scoot12(var, indx, mode):
    ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))

def scoot12p(var, indx, mode):
    ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_last.get())])))


def selectlast(event):
    ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))


root = tk.Tk()
root.title('\N{fire} Initializing Scooter 1.0 \N{fire}')
root.geometry('280x60')

listofoptions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

def filechooser():
    global filelocation
    global numbers_list
    global numbered_metro_list
    global metro_list
    global order_list
    global filename
    global numbered_master_list
    global helpertext

    filename = fd.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"), ("all files","*.*")))
    filelocation.set(filename)
    csvfile = csv.reader(open(filename))
    metro_list = []
    order_list = []
    order_list_str = []
    next(csvfile)
    for row in csvfile:
        order = row[1]
        metro = row[0]

        metro_list.append(metro)
        order_list.append(int(order))
        order_list_str.append(order)

    filedisplay.configure(state='normal')
    filedisplay.delete(1.0, tk.END)
    filedisplay.insert(1.0, filename)
    filedisplay.configure(state='disabled')

    numbers_list = list(str(i) for i in [i + 1 for i in (range(len(metro_list)))])
    numbered_metro_list = [numbers + '. ' + words for numbers, words in zip(numbers_list, metro_list)]
    helpertext = [metros + ' ' + orders for metros, orders in zip(numbered_metro_list, order_list_str)]


filelocation = tk.StringVar()
filelocation.set('File Location')
fileopen = tk.Button(root, text='Choose file', command=filechooser, state='normal')
filedisplay = tk.Text(root, width=24, height=1, wrap='none')
filedisplay.insert(1.0, filelocation.get())
filedisplay.configure(state='disabled')


def logi_numerizer():
    #global numberoflogis
    global input_last
    global ordertotal_last
    global input_one
    global ordertotal_one
    global input_two
    global ordertotal_two
    global input_three
    global ordertotal_three
    global input_four
    global ordertotal_four
    global input_five
    global ordertotal_five
    global input_six
    global ordertotal_six
    global input_seven
    global ordertotal_seven
    global input_eight
    global ordertotal_eight
    global input_nine
    global ordertotal_nine
    global input_ten
    global ordertotal_ten
    global input_eleven
    global ordertotal_eleven
    global input_twelve
    global ordertotal_twelve
    global input_thirteen
    global ordertotal_thirteen

    helper = tk.Tk()
    helper.geometry('225x400+425+100')
    helper.title('\U0001F916 Handlebars \U0001F916')
    helperdisplay = tk.Text(helper)

    for values in helpertext:
        helperdisplay.insert(tk.END, values + '\n')

    helperdisplay.config(state='disabled')
    helperdisplay.pack()

    if firstchoice.get() == '1':
        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x60')

        root.destroy()

        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')
        
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[0])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)

        label_last = tk.Label(branch, text='1')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)
    
        label_last.grid(row=0, column=0, padx=5)
        option_last.grid(row=0, column=1, padx=5)
        display_last.grid(row=0, column=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() +'''
----------------------------------------''')
            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=1, rowspan=2, column=2)

    if firstchoice.get() == '2':
        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x120')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1p)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)

        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')
        
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot1p)

        label_last = tk.Label(branch, text='2')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)
    
        label_last.grid(row=1, column=0, padx=5)
        option_last.grid(row=1, column=1, padx=5)
        display_last.grid(row=1, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')
            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()            

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=2, rowspan=2, column=2)

    if  firstchoice.get() == '3':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x120')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2p)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')
        
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot2p)

        label_last = tk.Label(branch, text='3')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)
    
        label_last.grid(row=2, column=0, padx=5)
        option_last.grid(row=2, column=1, padx=5)
        display_last.grid(row=2, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=4, rowspan=2, column=2)
    
    if firstchoice.get() == '4':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x150')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3p)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')
        
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot3p)

        label_last = tk.Label(branch, text='4')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)
    
        label_last.grid(row=3, column=0, padx=5)
        option_last.grid(row=3, column=1, padx=5)
        display_last.grid(row=3, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()            

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=4, rowspan=2, column=2)

    if firstchoice.get() == '5':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x180')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_four = tk.StringVar(branch)
        ordertotal_four.set('# of Orders')

        input_four = tk.StringVar(branch)
        input_four.set(numbered_metro_list[0])
        option_four = tk.OptionMenu(branch, input_four, *numbered_metro_list, command=select4p)
        option_four.config(width=20)
        input_four.trace_add("write", scoot3)

        label_four = tk.Label(branch, text='4')
        display_four = tk.Label(branch, width=10, textvariable=ordertotal_four)

        label_four.grid(row=3, column=0, padx=5)
        option_four.grid(row=3, column=1, padx=5)
        display_four.grid(row=3, column=2,columnspan=2)


        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')
        
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot4p)

        label_last = tk.Label(branch, text='5')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)
    
        label_last.grid(row=4, column=0, padx=5)
        option_last.grid(row=4, column=1, padx=5)
        display_last.grid(row=4, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=5, rowspan=2, column=2)

    if firstchoice.get() == '6':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x210')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_four = tk.StringVar(branch)
        ordertotal_four.set('# of Orders')

        input_four = tk.StringVar(branch)
        input_four.set(numbered_metro_list[0])
        option_four = tk.OptionMenu(branch, input_four, *numbered_metro_list, command=select4)
        option_four.config(width=20)
        input_four.trace_add("write", scoot3)

        label_four = tk.Label(branch, text='4')
        display_four = tk.Label(branch, width=10, textvariable=ordertotal_four)

        label_four.grid(row=3, column=0, padx=5)
        option_four.grid(row=3, column=1, padx=5)
        display_four.grid(row=3, column=2,columnspan=2)


        ordertotal_five = tk.StringVar(branch)
        ordertotal_five.set('# of Orders')

        input_five = tk.StringVar(branch)
        input_five.set(numbered_metro_list[0])
        option_five = tk.OptionMenu(branch, input_five, *numbered_metro_list, command=select5p)
        option_five.config(width=20)
        input_five.trace_add("write", scoot4)

        label_five = tk.Label(branch, text='5')
        display_five = tk.Label(branch, width=10, textvariable=ordertotal_five)

        label_five.grid(row=4, column=0, padx=5)
        option_five.grid(row=4, column=1, padx=5)
        display_five.grid(row=4, column=2,columnspan=2)

        
        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')
        
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot5p)

        label_last = tk.Label(branch, text='6')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)
    
        label_last.grid(row=5, column=0, padx=5)
        option_last.grid(row=5, column=1, padx=5)
        display_last.grid(row=5, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_last.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=6, rowspan=2, column=2)

    if firstchoice.get() == '7':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x240')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_four = tk.StringVar(branch)
        ordertotal_four.set('# of Orders')

        input_four = tk.StringVar(branch)
        input_four.set(numbered_metro_list[0])
        option_four = tk.OptionMenu(branch, input_four, *numbered_metro_list, command=select4)
        option_four.config(width=20)
        input_four.trace_add("write", scoot3)

        label_four = tk.Label(branch, text='4')
        display_four = tk.Label(branch, width=10, textvariable=ordertotal_four)

        label_four.grid(row=3, column=0, padx=5)
        option_four.grid(row=3, column=1, padx=5)
        display_four.grid(row=3, column=2,columnspan=2)


        ordertotal_five = tk.StringVar(branch)
        ordertotal_five.set('# of Orders')

        input_five = tk.StringVar(branch)
        input_five.set(numbered_metro_list[0])
        option_five = tk.OptionMenu(branch, input_five, *numbered_metro_list, command=select5)
        option_five.config(width=20)
        input_five.trace_add("write", scoot4)

        label_five = tk.Label(branch, text='5')
        display_five = tk.Label(branch, width=10, textvariable=ordertotal_five)

        label_five.grid(row=4, column=0, padx=5)
        option_five.grid(row=4, column=1, padx=5)
        display_five.grid(row=4, column=2,columnspan=2)

        ordertotal_six = tk.StringVar(branch)
        ordertotal_six.set('# of Orders')

        input_six = tk.StringVar(branch)
        input_six.set(numbered_metro_list[0])
        option_six = tk.OptionMenu(branch, input_six, *numbered_metro_list, command=select6p)
        option_six.config(width=20)
        input_six.trace_add("write", scoot5)

        label_six = tk.Label(branch, text='6')
        display_six = tk.Label(branch, width=10, textvariable=ordertotal_six)

        label_six.grid(row=5, column=0, padx=5)
        option_six.grid(row=5, column=1, padx=5)
        display_six.grid(row=5, column=2,columnspan=2)


        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')

        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot6p)

        label_last = tk.Label(branch, text='7')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

        label_last.grid(row=6, column=0, padx=5)
        option_last.grid(row=6, column=1, padx=5)
        display_last.grid(row=6, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_five.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_six.get())] + ' / Orders: ' + ordertotal_six.get() + '''
7. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + ''' 
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=7, rowspan=2, column=2)  

    if firstchoice.get() == '8':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x270')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_four = tk.StringVar(branch)
        ordertotal_four.set('# of Orders')

        input_four = tk.StringVar(branch)
        input_four.set(numbered_metro_list[0])
        option_four = tk.OptionMenu(branch, input_four, *numbered_metro_list, command=select4)
        option_four.config(width=20)
        input_four.trace_add("write", scoot3)

        label_four = tk.Label(branch, text='4')
        display_four = tk.Label(branch, width=10, textvariable=ordertotal_four)

        label_four.grid(row=3, column=0, padx=5)
        option_four.grid(row=3, column=1, padx=5)
        display_four.grid(row=3, column=2,columnspan=2)


        ordertotal_five = tk.StringVar(branch)
        ordertotal_five.set('# of Orders')

        input_five = tk.StringVar(branch)
        input_five.set(numbered_metro_list[0])
        option_five = tk.OptionMenu(branch, input_five, *numbered_metro_list, command=select5)
        option_five.config(width=20)
        input_five.trace_add("write", scoot4)

        label_five = tk.Label(branch, text='5')
        display_five = tk.Label(branch, width=10, textvariable=ordertotal_five)

        label_five.grid(row=4, column=0, padx=5)
        option_five.grid(row=4, column=1, padx=5)
        display_five.grid(row=4, column=2,columnspan=2)

        ordertotal_six = tk.StringVar(branch)
        ordertotal_six.set('# of Orders')

        input_six = tk.StringVar(branch)
        input_six.set(numbered_metro_list[0])
        option_six = tk.OptionMenu(branch, input_six, *numbered_metro_list, command=select6)
        option_six.config(width=20)
        input_six.trace_add("write", scoot5)

        label_six = tk.Label(branch, text='6')
        display_six = tk.Label(branch, width=10, textvariable=ordertotal_six)

        label_six.grid(row=5, column=0, padx=5)
        option_six.grid(row=5, column=1, padx=5)
        display_six.grid(row=5, column=2,columnspan=2)

        ordertotal_seven = tk.StringVar(branch)
        ordertotal_seven.set('# of Orders')

        input_seven = tk.StringVar(branch)
        input_seven.set(numbered_metro_list[0])
        option_seven = tk.OptionMenu(branch, input_seven, *numbered_metro_list, command=select7p)
        option_seven.config(width=20)
        input_seven.trace_add("write", scoot6)

        label_seven = tk.Label(branch, text='7')
        display_seven = tk.Label(branch, width=10, textvariable=ordertotal_seven)

        label_seven.grid(row=6, column=0, padx=5)
        option_seven.grid(row=6, column=1, padx=5)
        display_seven.grid(row=6, column=2,columnspan=2)


        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')

        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot7p)

        label_last = tk.Label(branch, text='8')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

        label_last.grid(row=7, column=0, padx=5)
        option_last.grid(row=7, column=1, padx=5)
        display_last.grid(row=7, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_five.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_six.get())] + ' / Orders: ' + ordertotal_six.get() + '''
7. Metro: ''' +   metro_list[numbered_metro_list.index(input_seven.get())] + ' / Orders: ' + ordertotal_seven.get() + ''' 
8. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=8, rowspan=2, column=2)

    if firstchoice.get() == '9':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x300')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_four = tk.StringVar(branch)
        ordertotal_four.set('# of Orders')

        input_four = tk.StringVar(branch)
        input_four.set(numbered_metro_list[0])
        option_four = tk.OptionMenu(branch, input_four, *numbered_metro_list, command=select4)
        option_four.config(width=20)
        input_four.trace_add("write", scoot3)

        label_four = tk.Label(branch, text='4')
        display_four = tk.Label(branch, width=10, textvariable=ordertotal_four)

        label_four.grid(row=3, column=0, padx=5)
        option_four.grid(row=3, column=1, padx=5)
        display_four.grid(row=3, column=2,columnspan=2)


        ordertotal_five = tk.StringVar(branch)
        ordertotal_five.set('# of Orders')

        input_five = tk.StringVar(branch)
        input_five.set(numbered_metro_list[0])
        option_five = tk.OptionMenu(branch, input_five, *numbered_metro_list, command=select5)
        option_five.config(width=20)
        input_five.trace_add("write", scoot4)

        label_five = tk.Label(branch, text='5')
        display_five = tk.Label(branch, width=10, textvariable=ordertotal_five)

        label_five.grid(row=4, column=0, padx=5)
        option_five.grid(row=4, column=1, padx=5)
        display_five.grid(row=4, column=2,columnspan=2)

        ordertotal_six = tk.StringVar(branch)
        ordertotal_six.set('# of Orders')

        input_six = tk.StringVar(branch)
        input_six.set(numbered_metro_list[0])
        option_six = tk.OptionMenu(branch, input_six, *numbered_metro_list, command=select6)
        option_six.config(width=20)
        input_six.trace_add("write", scoot5)

        label_six = tk.Label(branch, text='6')
        display_six = tk.Label(branch, width=10, textvariable=ordertotal_six)

        label_six.grid(row=5, column=0, padx=5)
        option_six.grid(row=5, column=1, padx=5)
        display_six.grid(row=5, column=2,columnspan=2)

        ordertotal_seven = tk.StringVar(branch)
        ordertotal_seven.set('# of Orders')

        input_seven = tk.StringVar(branch)
        input_seven.set(numbered_metro_list[0])
        option_seven = tk.OptionMenu(branch, input_seven, *numbered_metro_list, command=select7)
        option_seven.config(width=20)
        input_seven.trace_add("write", scoot6)

        label_seven = tk.Label(branch, text='7')
        display_seven = tk.Label(branch, width=10, textvariable=ordertotal_seven)

        label_seven.grid(row=6, column=0, padx=5)
        option_seven.grid(row=6, column=1, padx=5)
        display_seven.grid(row=6, column=2,columnspan=2)


        ordertotal_eight = tk.StringVar(branch)
        ordertotal_eight.set('# of Orders')

        input_eight = tk.StringVar(branch)
        input_eight.set(numbered_metro_list[0])
        option_eight = tk.OptionMenu(branch, input_eight, *numbered_metro_list, command=select8p)
        option_eight.config(width=20)
        input_eight.trace_add("write", scoot7)

        label_eight = tk.Label(branch, text='8')
        display_eight = tk.Label(branch, width=10, textvariable=ordertotal_eight)

        label_eight.grid(row=7, column=0, padx=5)
        option_eight.grid(row=7, column=1, padx=5)
        display_eight.grid(row=7, column=2,columnspan=2)


        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')

        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot8p)

        label_last = tk.Label(branch, text='9')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

        label_last.grid(row=8, column=0, padx=5)
        option_last.grid(row=8, column=1, padx=5)
        display_last.grid(row=8, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_five.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_six.get())] + ' / Orders: ' + ordertotal_six.get() + '''
7. Metro: ''' +   metro_list[numbered_metro_list.index(input_seven.get())] + ' / Orders: ' + ordertotal_seven.get() + '''
8. Metro: ''' +   metro_list[numbered_metro_list.index(input_eight.get())] + ' / Orders: ' + ordertotal_eight.get() + '''
9. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + ''' 
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=9, rowspan=2, column=2)

    if firstchoice.get() == '10':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x330')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_four = tk.StringVar(branch)
        ordertotal_four.set('# of Orders')

        input_four = tk.StringVar(branch)
        input_four.set(numbered_metro_list[0])
        option_four = tk.OptionMenu(branch, input_four, *numbered_metro_list, command=select4)
        option_four.config(width=20)
        input_four.trace_add("write", scoot3)

        label_four = tk.Label(branch, text='4')
        display_four = tk.Label(branch, width=10, textvariable=ordertotal_four)

        label_four.grid(row=3, column=0, padx=5)
        option_four.grid(row=3, column=1, padx=5)
        display_four.grid(row=3, column=2,columnspan=2)


        ordertotal_five = tk.StringVar(branch)
        ordertotal_five.set('# of Orders')

        input_five = tk.StringVar(branch)
        input_five.set(numbered_metro_list[0])
        option_five = tk.OptionMenu(branch, input_five, *numbered_metro_list, command=select5)
        option_five.config(width=20)
        input_five.trace_add("write", scoot4)

        label_five = tk.Label(branch, text='5')
        display_five = tk.Label(branch, width=10, textvariable=ordertotal_five)

        label_five.grid(row=4, column=0, padx=5)
        option_five.grid(row=4, column=1, padx=5)
        display_five.grid(row=4, column=2,columnspan=2)

        ordertotal_six = tk.StringVar(branch)
        ordertotal_six.set('# of Orders')

        input_six = tk.StringVar(branch)
        input_six.set(numbered_metro_list[0])
        option_six = tk.OptionMenu(branch, input_six, *numbered_metro_list, command=select6)
        option_six.config(width=20)
        input_six.trace_add("write", scoot5)

        label_six = tk.Label(branch, text='6')
        display_six = tk.Label(branch, width=10, textvariable=ordertotal_six)

        label_six.grid(row=5, column=0, padx=5)
        option_six.grid(row=5, column=1, padx=5)
        display_six.grid(row=5, column=2,columnspan=2)

        ordertotal_seven = tk.StringVar(branch)
        ordertotal_seven.set('# of Orders')

        input_seven = tk.StringVar(branch)
        input_seven.set(numbered_metro_list[0])
        option_seven = tk.OptionMenu(branch, input_seven, *numbered_metro_list, command=select7)
        option_seven.config(width=20)
        input_seven.trace_add("write", scoot6)

        label_seven = tk.Label(branch, text='7')
        display_seven = tk.Label(branch, width=10, textvariable=ordertotal_seven)

        label_seven.grid(row=6, column=0, padx=5)
        option_seven.grid(row=6, column=1, padx=5)
        display_seven.grid(row=6, column=2,columnspan=2)


        ordertotal_eight = tk.StringVar(branch)
        ordertotal_eight.set('# of Orders')

        input_eight = tk.StringVar(branch)
        input_eight.set(numbered_metro_list[0])
        option_eight = tk.OptionMenu(branch, input_eight, *numbered_metro_list, command=select8)
        option_eight.config(width=20)
        input_eight.trace_add("write", scoot7)

        label_eight = tk.Label(branch, text='8')
        display_eight = tk.Label(branch, width=10, textvariable=ordertotal_eight)

        label_eight.grid(row=7, column=0, padx=5)
        option_eight.grid(row=7, column=1, padx=5)
        display_eight.grid(row=7, column=2,columnspan=2)

        ordertotal_nine = tk.StringVar(branch)
        ordertotal_nine.set('# of Orders')

        input_nine = tk.StringVar(branch)
        input_nine.set(numbered_metro_list[0])
        option_nine = tk.OptionMenu(branch, input_nine, *numbered_metro_list, command=select9p)
        option_nine.config(width=20)
        input_nine.trace_add("write", scoot8)

        label_nine = tk.Label(branch, text='9')
        display_nine = tk.Label(branch, width=10, textvariable=ordertotal_nine)

        label_nine.grid(row=8, column=0, padx=5)
        option_nine.grid(row=8, column=1, padx=5)
        display_nine.grid(row=8, column=2,columnspan=2)


        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')

        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot9p)

        label_last = tk.Label(branch, text='10')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

        label_last.grid(row=9, column=0, padx=5)
        option_last.grid(row=9, column=1, padx=5)
        display_last.grid(row=9, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_five.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_six.get())] + ' / Orders: ' + ordertotal_six.get() + '''
7. Metro: ''' +   metro_list[numbered_metro_list.index(input_seven.get())] + ' / Orders: ' + ordertotal_seven.get() + '''
8. Metro: ''' +   metro_list[numbered_metro_list.index(input_eight.get())] + ' / Orders: ' + ordertotal_eight.get() + '''
9. Metro: ''' +   metro_list[numbered_metro_list.index(input_nine.get())] + ' / Orders: ' + ordertotal_nine.get() + ''' 
10. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=10, rowspan=2, column=2)

    if firstchoice.get() == '11':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x360')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_four = tk.StringVar(branch)
        ordertotal_four.set('# of Orders')

        input_four = tk.StringVar(branch)
        input_four.set(numbered_metro_list[0])
        option_four = tk.OptionMenu(branch, input_four, *numbered_metro_list, command=select4)
        option_four.config(width=20)
        input_four.trace_add("write", scoot3)

        label_four = tk.Label(branch, text='4')
        display_four = tk.Label(branch, width=10, textvariable=ordertotal_four)

        label_four.grid(row=3, column=0, padx=5)
        option_four.grid(row=3, column=1, padx=5)
        display_four.grid(row=3, column=2,columnspan=2)


        ordertotal_five = tk.StringVar(branch)
        ordertotal_five.set('# of Orders')

        input_five = tk.StringVar(branch)
        input_five.set(numbered_metro_list[0])
        option_five = tk.OptionMenu(branch, input_five, *numbered_metro_list, command=select5)
        option_five.config(width=20)
        input_five.trace_add("write", scoot4)

        label_five = tk.Label(branch, text='5')
        display_five = tk.Label(branch, width=10, textvariable=ordertotal_five)

        label_five.grid(row=4, column=0, padx=5)
        option_five.grid(row=4, column=1, padx=5)
        display_five.grid(row=4, column=2,columnspan=2)

        ordertotal_six = tk.StringVar(branch)
        ordertotal_six.set('# of Orders')

        input_six = tk.StringVar(branch)
        input_six.set(numbered_metro_list[0])
        option_six = tk.OptionMenu(branch, input_six, *numbered_metro_list, command=select6)
        option_six.config(width=20)
        input_six.trace_add("write", scoot5)

        label_six = tk.Label(branch, text='6')
        display_six = tk.Label(branch, width=10, textvariable=ordertotal_six)

        label_six.grid(row=5, column=0, padx=5)
        option_six.grid(row=5, column=1, padx=5)
        display_six.grid(row=5, column=2,columnspan=2)

        ordertotal_seven = tk.StringVar(branch)
        ordertotal_seven.set('# of Orders')

        input_seven = tk.StringVar(branch)
        input_seven.set(numbered_metro_list[0])
        option_seven = tk.OptionMenu(branch, input_seven, *numbered_metro_list, command=select7)
        option_seven.config(width=20)
        input_seven.trace_add("write", scoot6)

        label_seven = tk.Label(branch, text='7')
        display_seven = tk.Label(branch, width=10, textvariable=ordertotal_seven)

        label_seven.grid(row=6, column=0, padx=5)
        option_seven.grid(row=6, column=1, padx=5)
        display_seven.grid(row=6, column=2,columnspan=2)


        ordertotal_eight = tk.StringVar(branch)
        ordertotal_eight.set('# of Orders')

        input_eight = tk.StringVar(branch)
        input_eight.set(numbered_metro_list[0])
        option_eight = tk.OptionMenu(branch, input_eight, *numbered_metro_list, command=select8)
        option_eight.config(width=20)
        input_eight.trace_add("write", scoot7)

        label_eight = tk.Label(branch, text='8')
        display_eight = tk.Label(branch, width=10, textvariable=ordertotal_eight)

        label_eight.grid(row=7, column=0, padx=5)
        option_eight.grid(row=7, column=1, padx=5)
        display_eight.grid(row=7, column=2,columnspan=2)

        ordertotal_nine = tk.StringVar(branch)
        ordertotal_nine.set('# of Orders')

        input_nine = tk.StringVar(branch)
        input_nine.set(numbered_metro_list[0])
        option_nine = tk.OptionMenu(branch, input_nine, *numbered_metro_list, command=select9)
        option_nine.config(width=20)
        input_nine.trace_add("write", scoot8)

        label_nine = tk.Label(branch, text='9')
        display_nine = tk.Label(branch, width=10, textvariable=ordertotal_nine)

        label_nine.grid(row=8, column=0, padx=5)
        option_nine.grid(row=8, column=1, padx=5)
        display_nine.grid(row=8, column=2,columnspan=2)

        ordertotal_ten = tk.StringVar(branch)
        ordertotal_ten.set('# of Orders')

        input_ten = tk.StringVar(branch)
        input_ten.set(numbered_metro_list[0])
        option_ten = tk.OptionMenu(branch, input_ten, *numbered_metro_list, command=select10p)
        option_ten.config(width=20)
        input_ten.trace_add("write", scoot9)

        label_ten = tk.Label(branch, text='10')
        display_ten = tk.Label(branch, width=10, textvariable=ordertotal_ten)

        label_ten.grid(row=9, column=0, padx=5)
        option_ten.grid(row=9, column=1, padx=5)
        display_ten.grid(row=9, column=2,columnspan=2)


        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')

        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot10p)

        label_last = tk.Label(branch, text='11')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

        label_last.grid(row=10, column=0, padx=5)
        option_last.grid(row=10, column=1, padx=5)
        display_last.grid(row=10, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_five.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_six.get())] + ' / Orders: ' + ordertotal_six.get() + '''
7. Metro: ''' +   metro_list[numbered_metro_list.index(input_seven.get())] + ' / Orders: ' + ordertotal_seven.get() + '''
8. Metro: ''' +   metro_list[numbered_metro_list.index(input_eight.get())] + ' / Orders: ' + ordertotal_eight.get() + '''
9. Metro: ''' +   metro_list[numbered_metro_list.index(input_nine.get())] + ' / Orders: ' + ordertotal_nine.get() + ''' 
10. Metro: ''' +   metro_list[numbered_metro_list.index(input_ten.get())] + ' / Orders: ' + ordertotal_ten.get() + '''
11. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=11, rowspan=2, column=2)

    if firstchoice.get() == '12':

        branch = tk.Tk()
        branch.title('\N{rocket} Scooter 1.0 \N{rocket}')
        branch.geometry('330x390')

        root.destroy()

        ordertotal_one = tk.StringVar(branch)
        ordertotal_one.set('# of Orders')

        input_one = tk.StringVar(branch)
        input_one.set(numbered_metro_list[0])
        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_one = tk.OptionMenu(branch, input_one, *numbered_metro_list, command=select1)
        option_one.config(width=20)

        label_one = tk.Label(branch, text='1')
        display_one = tk.Label(branch, width=10, textvariable=ordertotal_one)

        label_one.grid(row=0, column=0, padx=5)
        option_one.grid(row=0, column=1, padx=5)
        display_one.grid(row=0, column=2,columnspan=2)


        ordertotal_two = tk.StringVar(branch)
        ordertotal_two.set('# of Orders')

        input_two = tk.StringVar(branch)
        input_two.set(numbered_metro_list[0])
        option_two = tk.OptionMenu(branch, input_two, *numbered_metro_list, command=select2)
        option_two.config(width=20)
        input_two.trace_add("write", scoot1)

        label_two = tk.Label(branch, text='2')
        display_two = tk.Label(branch, width=10, textvariable=ordertotal_two)

        label_two.grid(row=1, column=0, padx=5)
        option_two.grid(row=1, column=1, padx=5)
        display_two.grid(row=1, column=2,columnspan=2)


        ordertotal_three = tk.StringVar(branch)
        ordertotal_three.set('# of Orders')

        input_three = tk.StringVar(branch)
        input_three.set(numbered_metro_list[0])
        option_three = tk.OptionMenu(branch, input_three, *numbered_metro_list, command=select3)
        option_three.config(width=20)
        input_three.trace_add("write", scoot2)

        label_three = tk.Label(branch, text='3')
        display_three = tk.Label(branch, width=10, textvariable=ordertotal_three)

        label_three.grid(row=2, column=0, padx=5)
        option_three.grid(row=2, column=1, padx=5)
        display_three.grid(row=2, column=2,columnspan=2)


        ordertotal_four = tk.StringVar(branch)
        ordertotal_four.set('# of Orders')

        input_four = tk.StringVar(branch)
        input_four.set(numbered_metro_list[0])
        option_four = tk.OptionMenu(branch, input_four, *numbered_metro_list, command=select4)
        option_four.config(width=20)
        input_four.trace_add("write", scoot3)

        label_four = tk.Label(branch, text='4')
        display_four = tk.Label(branch, width=10, textvariable=ordertotal_four)

        label_four.grid(row=3, column=0, padx=5)
        option_four.grid(row=3, column=1, padx=5)
        display_four.grid(row=3, column=2,columnspan=2)


        ordertotal_five = tk.StringVar(branch)
        ordertotal_five.set('# of Orders')

        input_five = tk.StringVar(branch)
        input_five.set(numbered_metro_list[0])
        option_five = tk.OptionMenu(branch, input_five, *numbered_metro_list, command=select5)
        option_five.config(width=20)
        input_five.trace_add("write", scoot4)

        label_five = tk.Label(branch, text='5')
        display_five = tk.Label(branch, width=10, textvariable=ordertotal_five)

        label_five.grid(row=4, column=0, padx=5)
        option_five.grid(row=4, column=1, padx=5)
        display_five.grid(row=4, column=2,columnspan=2)

        ordertotal_six = tk.StringVar(branch)
        ordertotal_six.set('# of Orders')

        input_six = tk.StringVar(branch)
        input_six.set(numbered_metro_list[0])
        option_six = tk.OptionMenu(branch, input_six, *numbered_metro_list, command=select6)
        option_six.config(width=20)
        input_six.trace_add("write", scoot5)

        label_six = tk.Label(branch, text='6')
        display_six = tk.Label(branch, width=10, textvariable=ordertotal_six)

        label_six.grid(row=5, column=0, padx=5)
        option_six.grid(row=5, column=1, padx=5)
        display_six.grid(row=5, column=2,columnspan=2)

        ordertotal_seven = tk.StringVar(branch)
        ordertotal_seven.set('# of Orders')

        input_seven = tk.StringVar(branch)
        input_seven.set(numbered_metro_list[0])
        option_seven = tk.OptionMenu(branch, input_seven, *numbered_metro_list, command=select7)
        option_seven.config(width=20)
        input_seven.trace_add("write", scoot6)

        label_seven = tk.Label(branch, text='7')
        display_seven = tk.Label(branch, width=10, textvariable=ordertotal_seven)

        label_seven.grid(row=6, column=0, padx=5)
        option_seven.grid(row=6, column=1, padx=5)
        display_seven.grid(row=6, column=2,columnspan=2)


        ordertotal_eight = tk.StringVar(branch)
        ordertotal_eight.set('# of Orders')

        input_eight = tk.StringVar(branch)
        input_eight.set(numbered_metro_list[0])
        option_eight = tk.OptionMenu(branch, input_eight, *numbered_metro_list, command=select8)
        option_eight.config(width=20)
        input_eight.trace_add("write", scoot7)

        label_eight = tk.Label(branch, text='8')
        display_eight = tk.Label(branch, width=10, textvariable=ordertotal_eight)

        label_eight.grid(row=7, column=0, padx=5)
        option_eight.grid(row=7, column=1, padx=5)
        display_eight.grid(row=7, column=2,columnspan=2)

        ordertotal_nine = tk.StringVar(branch)
        ordertotal_nine.set('# of Orders')

        input_nine = tk.StringVar(branch)
        input_nine.set(numbered_metro_list[0])
        option_nine = tk.OptionMenu(branch, input_nine, *numbered_metro_list, command=select9)
        option_nine.config(width=20)
        input_nine.trace_add("write", scoot8)

        label_nine = tk.Label(branch, text='9')
        display_nine = tk.Label(branch, width=10, textvariable=ordertotal_nine)

        label_nine.grid(row=8, column=0, padx=5)
        option_nine.grid(row=8, column=1, padx=5)
        display_nine.grid(row=8, column=2,columnspan=2)

        ordertotal_ten = tk.StringVar(branch)
        ordertotal_ten.set('# of Orders')

        input_ten = tk.StringVar(branch)
        input_ten.set(numbered_metro_list[0])
        option_ten = tk.OptionMenu(branch, input_ten, *numbered_metro_list, command=select10)
        option_ten.config(width=20)
        input_ten.trace_add("write", scoot9)

        label_ten = tk.Label(branch, text='10')
        display_ten = tk.Label(branch, width=10, textvariable=ordertotal_ten)

        label_ten.grid(row=9, column=0, padx=5)
        option_ten.grid(row=9, column=1, padx=5)
        display_ten.grid(row=9, column=2,columnspan=2)


        ordertotal_eleven = tk.StringVar(branch)
        ordertotal_eleven.set('# of Orders')

        input_eleven = tk.StringVar(branch)
        input_eleven.set(numbered_metro_list[0])
        option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11p)
        option_eleven.config(width=20)
        input_eleven.trace_add("write", scoot10)

        label_eleven = tk.Label(branch, text='11')
        display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

        label_eleven.grid(row=10, column=0, padx=5)
        option_eleven.grid(row=10, column=1, padx=5)
        display_eleven.grid(row=10, column=2,columnspan=2)

        ordertotal_last = tk.StringVar(branch)
        ordertotal_last.set('# of Orders')

        input_last = tk.StringVar(branch)
        input_last.set(numbered_metro_list[-1])
        option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
        option_last.config(width=20)
        input_last.trace_add("write", scoot11p)

        label_last = tk.Label(branch, text='12')
        display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

        label_last.grid(row=11, column=0, padx=5)
        option_last.grid(row=11, column=1, padx=5)
        display_last.grid(row=11, column=2,columnspan=2)

        def finisher():
            result = tk.Tk()
            result.title('\U0001F44C Scooted \U0001F44C')

            split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_five.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_six.get())] + ' / Orders: ' + ordertotal_six.get() + '''
7. Metro: ''' +   metro_list[numbered_metro_list.index(input_seven.get())] + ' / Orders: ' + ordertotal_seven.get() + '''
8. Metro: ''' +   metro_list[numbered_metro_list.index(input_eight.get())] + ' / Orders: ' + ordertotal_eight.get() + '''
9. Metro: ''' +   metro_list[numbered_metro_list.index(input_nine.get())] + ' / Orders: ' + ordertotal_nine.get() + ''' 
10. Metro: ''' +   metro_list[numbered_metro_list.index(input_ten.get())] + ' / Orders: ' + ordertotal_ten.get() + '''
11. Metro: ''' +   metro_list[numbered_metro_list.index(input_eleven.get())] + ' / Orders: ' + ordertotal_eleven.get() + '''
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

            display_result = tk.Text(result)
            display_result.insert(1.0, split)
            display_result.pack()

            branch.destroy()
            helper.destroy()

        generate = tk.Button(branch, text='Generate', command=finisher)
        generate.grid(row=12, rowspan=2, column=2)


firstchoice = ttk.Combobox(root, value=listofoptions, width=10)
firstchoice.set('''# of Logi's''')

initialize = tk.Button(root, text='Initialize', command=logi_numerizer, state='normal')

filedisplay.grid(row=0, column=0, columnspan=2, pady=5)
fileopen.grid(row=0, column=2)
firstchoice.grid(row=1, column=0)
initialize.grid(row=1, column=2)

root.mainloop()