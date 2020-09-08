    ### Scooter 1.1 ###

'''

 Assembled With:

    Python 3.8.1
    tkinter 8.6
    Py2App 0.21
 

Caveat
	
    Due to complications with permissions and my installation of Python, I’m now 
    using an older version of Python (3.8.1) which I installed with pyenv. 
    For that reason, running the script using Python 3.8.2+ might produce slightly 
    different results. It should still be perfectly functional either way.

    This code is deceptively long due to other complications with tkinter 
    itself. I experimented with using combinations of classes, methods, 
    and nested if statements but found that those would not run properly 
    with the way tkinter is setup. The main three issues are as follows: 

        1) A tkinter window and its components must be in the same statement. 
        That is to say that that you cannot separate them with if statements or 
        hide widgets inside a function.

        2) Certain tkinter components can’t be used in a function/method 
        at all. The main one that can’t be used as a command, much to my 
        dismay, is Combobox. Those are the pretty dropdown boxes.

        3) You cannot, based on my knowledge and experimentation, define a variable
        using the attributes from an object. This makes classes not 
        particularly useful in this case.

    That being said, I am open to any suggestions/fixes to these issues. 
    Scooter is still very much a work in progress, as far as I’m concerned.
    
    If you read through all of this script you’ll find a staggering amount of
    redundancy! 

    I hope this documentation will help you understand the architecture of 
    this script without too much trouble.

 DESCRIPTION: 

    Scooter is a new alternative to the Splitter we’ve all come to know 
    and love! It allows complete control over the split you’re generating
    by showing immediate tallies of how many orders each Logi would get if 
    they had slightly different letters. To put it simply: if Splitter 1.01 is
    a self-driving car and splitting manually is driving stick, Scooter is 
    like driving your first automatic. 

 HOW TO: 

    1. After running the split query, open an instance of Scooter and 
        copy the query results as a CSV.

        a.  To copy a CSV in Snowflake, click on the Download or View Results 
            button next to the Copy button above results and then click Show in 
            Dialog and it’ll present the data in text format to just 
            copy/paste into Scooter.
        b.   To copy a CSV in PopSQL, click on the Export button and then click Copy CSV.

    2. Highlight the text that says “(Please paste CSV info here)” and paste 
        the CSV file you just exported and copied to replace the text with the data.  

    3. Type in the number of logisticians you are splitting for 
        (or select from the dropdown) and hit “Initialize”. 

    4. Two windows will pop up - Scooter and Handlebars. Scooter is the main application window, 
        where the split is actually done. Handlebars is the companion window, showing the 
        raw order counts by metro in order to help with split adjustments.

    5. Review the split output in the Scooter window (preliminary 
        order counts are shown to the right of the metros). If the output works as-is, 
        move on to step 6. If it doesn’t look particularly even, you have two options:

            Use the dropdown menu to the left of “Generate” to adjust the  automatically 
            generated split (similar to how we used to rerun splits with decimals added to the 
            number of logis but without having to restart the process). If any of the order 
            totals are at “0” or “# of orders” then you’ll need to increase the number in 
            that dropdown menu. If the last order total is rather large and the others are too 
            small, you’ll need to decrease the number. 

            Manually move the dropdown menus to fix the order totals. Every selection affects 
            the Logi whose metros you changed as well as the one above. Decreasing the metro 
            number of a Logi will increase their order total but decrease the order total of 
            the Logi above, and vice versa. The Handlebars window shows each metro’s order 
            totals for reference.

    6. Once satisfied with the split, hit “Generate”. A new window will appear with the results. 


 FLOW: 

    >User boots up Scooter 

    > root window (“Initializing Scooter”) appears, with a data input 
        Text box (filedisplay), a Combobox (firstchoice), 
        and a second button (initialize)
    > User selects the number of Logi’s (firstchoice) 
    > User confirms selection by hitting “Generate” button, 
        which starts the function logi_numerizer():

        > logi_numerizer() then sets all input/ordertotal variables to 
            global, meaning that any changes made inside of this function 
            are universal

        > logi_numerizer() opens helper window (“Handlebars”), with a for 
            loop to insert the text from helpertext (the list that was a 
            combination of numbered_metro_list and order_list_str), 
            then disables the text window so user can't type in it

        > logi_numerizer() opens one of thirty versions of the 
            branch window (“Scooter 1.1”), based on the results of 
            firstchoice.get() (the “Initialize” button) 

    > branch window consists of the following:
    
    (firstchoice.get() # of logi rows consisting of):

        label_x (Logi’s #) | option_x (dropdown menu which affects input_x 
        and starts function select_x/select_xp) | display_x label 
        (order tally, value is set by function in option_x)

        final row with a button (“Generate”) in the right corner and 

    > User selects options using option_x dropdown menus
    > any time a dropdown menu is used, select_x() / select_x() 
        and scoot_x() / scoot_xp() are started:
    
            > select_x() calculates the order tally (text in display_x) 
                by finding sum of the range of numbers from the index 
                number of the current value of input_x to the current value
                of input_y (the next dropdown menu) and converting it to 
                a string which it then sets as ordertotal_x

            > scoot_x() does the same but is triggered when the dropdown menu 
                below is changed (I.e. if you changed option_four it would 
                trigger scoot3 so that the order tally will automatically 
                adjust either way) 

            >select/scoot_xp are copies of the same functions that use the 
                index number of the last dropdown menu (which is named 
                label/option/input/display_last) instead of the next number 
                value’s (I.e. instead of checking for the sum of the 
                range of order tallies from input_three to input_four, 
                it checks for the sum for input_three to input_last) 

            > the p is for “penultimate”, isn’t that fun?

    > Once User is done scooting, they hit the “Generate” button, 
        which starts finisher():
    
            > finisher() opens a final window, (result, “Scooted”)

            > finisher() declares a string variable named split and 
                inserts the selected metro for each logi (found by 
                using the index number to return the metro from input_x but 
                from metro_list so it doesn’t have the number) and the order 
                tallies (using ordertotal_x(get)) into a prewritten 
                blank split 

            > finisher() closes the branch and helper windows

    > fin 
    
    '''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from io import StringIO
import csv
import json
import re #This is used for Regular Expressions, in this case to search strings for certain characters


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


def select13(event):
    ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))

def select13p(event):
    ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_last.get())])))    

def scoot13(var, indx, mode):
    ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))

def scoot13p(var, indx, mode):
    ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_last.get())])))


def select14(event):
    ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))

def select14p(event):
    ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_last.get())])))    

def scoot14(var, indx, mode):
    ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))

def scoot14p(var, indx, mode):
    ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_last.get())])))


def select15(event):
    ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))

def select15p(event):
    ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_last.get())])))    

def scoot15(var, indx, mode):
    ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))

def scoot15p(var, indx, mode):
    ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_last.get())])))


def select16(event):
    ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))

def select16p(event):
    ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_last.get())])))    

def scoot16(var, indx, mode):
    ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))

def scoot16p(var, indx, mode):
    ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_last.get())])))


def select17(event):
    ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))

def select17p(event):
    ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_last.get())])))    

def scoot17(var, indx, mode):
    ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))

def scoot17p(var, indx, mode):
    ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_last.get())])))


def select18(event):
    ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))

def select18p(event):
    ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_last.get())])))    

def scoot18(var, indx, mode):
    ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))

def scoot18p(var, indx, mode):
    ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_last.get())])))


def select19(event):
    ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))

def select19p(event):
    ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_last.get())])))    

def scoot19(var, indx, mode):
    ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))

def scoot19p(var, indx, mode):
    ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_last.get())])))


def select20(event):
    ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))

def select20p(event):
    ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_last.get())])))    

def scoot20(var, indx, mode):
    ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))

def scoot20p(var, indx, mode):
    ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_last.get())])))


def select21(event):
    ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())])))

def select21p(event):
    ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_last.get())])))    

def scoot21(var, indx, mode):
    ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())])))

def scoot21p(var, indx, mode):
    ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_last.get())])))


def select22(event):
    ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())])))

def select22p(event):
    ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_last.get())])))    

def scoot22(var, indx, mode):
    ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())])))

def scoot22p(var, indx, mode):
    ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_last.get())])))


def select23(event):
    ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))

def select23p(event):
    ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_last.get())])))    

def scoot23(var, indx, mode):
    ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))

def scoot23p(var, indx, mode):
    ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_last.get())])))


def select24(event):
    ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))

def select24p(event):
    ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_last.get())])))    

def scoot24(var, indx, mode):
    ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))

def scoot24p(var, indx, mode):
    ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_last.get())])))


def select25(event):
    ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))

def select25p(event):
    ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_last.get())])))    

def scoot25(var, indx, mode):
    ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))

def scoot25p(var, indx, mode):
    ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_last.get())])))


def select26(event):
    ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_twentyseven.get())])))

def select26p(event):
    ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_last.get())])))    

def scoot26(var, indx, mode):
    ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_twentyseven.get())])))

def scoot26p(var, indx, mode):
    ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_last.get())])))


def select27(event):
    ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_twentyeight.get())])))

def select27p(event):
    ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_last.get())])))    

def scoot27(var, indx, mode):
    ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_twentyeight.get())])))

def scoot27p(var, indx, mode):
    ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_last.get())])))


def select28(event):
    ordertotal_twentyeight.set(str(sum(order_list[numbered_metro_list.index(input_twentyeight.get()):numbered_metro_list.index(input_twentynine.get())])))

def select28p(event):
    ordertotal_twentyeight.set(str(sum(order_list[numbered_metro_list.index(input_twentyeight.get()):numbered_metro_list.index(input_last.get())])))    

def scoot28(var, indx, mode):
    ordertotal_twentyeight.set(str(sum(order_list[numbered_metro_list.index(input_twentyeight.get()):numbered_metro_list.index(input_twentynine.get())])))

def scoot28p(var, indx, mode):
    ordertotal_twentyeight.set(str(sum(order_list[numbered_metro_list.index(input_twentyeight.get()):numbered_metro_list.index(input_last.get())])))


def select29(event):
    ordertotal_twentynine.set(str(sum(order_list[numbered_metro_list.index(input_twentynine.get()):numbered_metro_list.index(input_thirty.get())])))

def select29p(event):
    ordertotal_twentynine.set(str(sum(order_list[numbered_metro_list.index(input_twentynine.get()):numbered_metro_list.index(input_last.get())])))    

def scoot29(var, indx, mode):
    ordertotal_twentynine.set(str(sum(order_list[numbered_metro_list.index(input_twentynine.get()):numbered_metro_list.index(input_thirty.get())])))

def scoot29p(var, indx, mode):
    ordertotal_twentynine.set(str(sum(order_list[numbered_metro_list.index(input_twentynine.get()):numbered_metro_list.index(input_last.get())])))


def select30(event):
    ordertotal_thirty.set(str(sum(order_list[numbered_metro_list.index(input_thirty.get()):numbered_metro_list.index(input_thirtyone.get())])))

def select30p(event):
    ordertotal_thirty.set(str(sum(order_list[numbered_metro_list.index(input_thirty.get()):numbered_metro_list.index(input_last.get())])))    

def scoot30(var, indx, mode):
    ordertotal_thirty.set(str(sum(order_list[numbered_metro_list.index(input_thirty.get()):numbered_metro_list.index(input_thirtyone.get())])))

def scoot30p(var, indx, mode):
    ordertotal_thirty.set(str(sum(order_list[numbered_metro_list.index(input_thirty.get()):numbered_metro_list.index(input_last.get())])))


def selectlast(event):
    ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

global return_number
return_number = 0

def home_screen():
    global root
    global return_check

    root = tk.Tk()
    root.title('\N{fire} Initializing Scooter 1.1 \N{fire}')
    if return_number == 0:
        root.geometry('255x60')
    elif return_number > 0:
        if re.search('255x60.+', previous_geometry):
            root.geometry('255x60' + previous_location)
    else:
        root.geometry(previous_geometry)

    listofoptions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']

    '''
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

    '''

    def csvchooser():
        global numbers_list
        global numbered_metro_list
        global metro_list
        global order_list
        global numbered_master_list
        global helpertext

        #csvstring = data_input.get("1.0", 'end-1c')
        splitcsv = previous_input.splitlines()

        csvfile = csv.reader(splitcsv, delimiter=',')
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

        numbers_list = list(str(i) for i in [i + 1 for i in (range(len(metro_list)))])
        numbered_metro_list = [numbers + '. ' + words for numbers, words in zip(numbers_list, metro_list)]
        helpertext = [metros + ' ' + orders for metros, orders in zip(numbered_metro_list, order_list_str)]

    def jsonchooser():
        global numbers_list
        global numbered_metro_list
        global metro_list
        global order_list
        global numbered_master_list
        global helpertext

        #jsonstring = data_input.get("1.0", 'end-1c')
        json_dict = json.loads(previous_input)

        metro_list = []
        order_list = []
        order_list_str = []

        for row in json_dict:
            order = row['count']
            metro = row['Metro']

            metro_list.append(metro)
            order_list.append(int(order))
            order_list_str.append(order)

        numbers_list = list(str(i) for i in [i + 1 for i in (range(len(metro_list)))])
        numbered_metro_list = [numbers + '. ' + words for numbers, words in zip(numbers_list, metro_list)]
        helpertext = [metros + ' ' + orders for metros, orders in zip(numbered_metro_list, order_list_str)]

    def tsvchooser():

        global numbers_list
        global numbered_metro_list
        global metro_list
        global order_list
        global numbered_master_list
        global helpertext

        #tsvstring = data_input.get("1.0", 'end-1c')
        splittsv = previous_input.splitlines()

        tsvfile = csv.reader(splittsv, delimiter='\t')
        metro_list = []
        order_list = []
        order_list_str = []
        next(tsvfile)
        for row in tsvfile:
            order = row[1]
            metro = row[0]

            metro_list.append(metro)
            order_list.append(int(order))
            order_list_str.append(order)

        numbers_list = list(str(i) for i in [i + 1 for i in (range(len(metro_list)))])
        numbered_metro_list = [numbers + '. ' + words for numbers, words in zip(numbers_list, metro_list)]
        helpertext = [metros + ' ' + orders for metros, orders in zip(numbered_metro_list, order_list_str)]

    input_string = tk.StringVar()
    input_string.set('(Please paste CSV/TSV/JSON here)')
    #csvopen = tk.Button(root, text='Choose file', command=csvchooser, state='normal')

    global data_input
    data_input = tk.Text(root, width=35, height=1, wrap='none')

    print("Return number: " + str(return_number))

    if return_number == 0: #Checking to see if this is the first split or if we're coming to this point from a Back/Home button
        data_input.insert(1.0, input_string.get())

    else:
        data_input.insert(1.0, previous_input) #pulling old split data

    global logi_numerizer

    return_check = 'Full'


    def logi_numerizer():
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
        global input_fourteen
        global ordertotal_fourteen
        global input_fifteen
        global ordertotal_fifteen
        global input_sixteen
        global ordertotal_sixteen
        global input_seventeen
        global ordertotal_seventeen
        global input_eighteen
        global ordertotal_eighteen
        global input_nineteen
        global ordertotal_nineteen
        global input_twenty
        global ordertotal_twenty
        global input_twentyone
        global ordertotal_twentyone
        global input_twentytwo
        global ordertotal_twentytwo
        global input_twentythree
        global ordertotal_twentythree
        global input_twentyfour
        global ordertotal_twentyfour
        global input_twentyfive
        global ordertotal_twentyfive
        global input_twentysix
        global ordertotal_twentysix
        global input_twentyseven
        global ordertotal_twentyseven
        global input_twentyeight
        global ordertotal_twentyeight
        global input_twentynine
        global ordertotal_twentynine
        global input_thirty
        global ordertotal_thirty

        global split
        global reset_number_str
        global reset_number 
        global numberoflogis

        global branch
        global helper
        global result
        global previous_input
        global numberoflogis_str
        global previous_geometry
        global previous_location
        global return_check
        global helper_location
        global helper_location_inverted

        if return_check == 'Full':

            previous_input = data_input.get("1.0", 'end-1c')
            previous_geometry = root.winfo_geometry()
            previous_location = '+' + str(root.winfo_x()) + '+' + (str(root.winfo_y()))

            helper_location = '+' + str(root.winfo_x() + root.winfo_width() + 170) + '+' + str(root.winfo_y() + 100)
            helper_location_inverted = '+' + str(root.winfo_x() - 425) + '+' + str(root.winfo_y() + 100)

            numberoflogis = int(firstchoice.get())
            numberoflogis_str = firstchoice.get()  

            #root.destroy()

        if '[' in previous_input:
            jsonchooser()
        
        elif ',' in previous_input:
            csvchooser()

        else: 
            tsvchooser()

        #csvchooser()
        #jsonchooser()
        print(numbered_metro_list)


        mode_options = [-2.0, -1.9, -1.8, -1.7, -1.6, -1.5, -1.4, -1.3, -1.2, -1.1, -1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2,2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0]

        def splitter():
            global split

            try: 
                root.winfo_exists()

                if root.winfo_exists():
                    root.destroy()
            
            except:
                return_check = 'Half'

            split = []
            molehill_firstlist = []
            ordertotal_blank = 0
            print(numberoflogis)
            print(numberoflogis + reset_number)
            goalnumber_plain = int(sum(order_list) / (float(numberoflogis) + reset_number))

            firstindex = 0
            secondindex = 0
            molehill_tally = 0

            for metros in range(len(order_list)):
                if order_list[metros] >= 1.5 * goalnumber_plain:
                    molehill_firstlist.append(0)
                    molehill_tally += 1

                else:
                    molehill_firstlist.append(order_list[metros])

            goalnumber_modified = int(sum(molehill_firstlist) // ((float(numberoflogis) + reset_number) - molehill_tally))

            molehill_masterlist = []
            molehill_index = []
            valley_totals = []
            
            while secondindex < len(molehill_firstlist):
                if secondindex < len(molehill_firstlist):
                    secondindex += 1

                if molehill_firstlist[firstindex] == 0: 
                    molehill_masterlist.append(0)
                    molehill_index.append('molehill')
                    valley_totals.append(0)
                    firstindex = secondindex

                    continue

                if secondindex == len(molehill_firstlist):
                    if sum((molehill_firstlist[firstindex:secondindex])) < goalnumber_modified:
                        if sum((molehill_firstlist[firstindex:secondindex])) < 100:
                            secondindex += 1

                            for endingconsolidatedmetros in range(secondindex - firstindex):
                                molehill_masterlist.append(0)

                            break

                        else: 
                            for endingvalleymetros in range(secondindex - firstindex):
                                molehill_masterlist.append(molehill_firstlist[firstindex + endingvalleymetros])
                            
                            molehill_index.append('valley')
                            valley_totals.append(sum(molehill_firstlist[firstindex:secondindex]))

                            break

                    else: 
                        for endingvalleymetros in range(secondindex - firstindex):
                            molehill_masterlist.append(molehill_firstlist[firstindex + endingvalleymetros])
                        
                        molehill_index.append('valley')
                        valley_totals.append(sum(molehill_firstlist[firstindex:secondindex]))

                        break

                elif molehill_firstlist[secondindex] == 0:
                    if sum((molehill_firstlist[firstindex:secondindex])) < goalnumber_modified:
                        if sum((molehill_firstlist[firstindex:secondindex])) < 100:
                            secondindex += 1

                            for consolidatedmetros in range(secondindex - firstindex):
                                molehill_masterlist.append(0)

                            molehill_index.append('molehill')
                            valley_totals.append(0)
                            firstindex = secondindex

                        else:

                            for smallvalleymetros in range(secondindex - firstindex):
                                molehill_masterlist.append(molehill_firstlist[firstindex + smallvalleymetros])

                            molehill_index.append('valley')
                            valley_totals.append(sum(molehill_firstlist[firstindex:secondindex]))
                            firstindex = secondindex

                    else: 

                        for valleymetros in range(secondindex - firstindex):
                            molehill_masterlist.append(molehill_firstlist[firstindex + valleymetros])

                        molehill_index.append('valley')
                        valley_totals.append(sum(molehill_firstlist[firstindex:secondindex]))
                        firstindex = secondindex
                
            firstindex = 0
            secondindex = 0

            goalnumber_final = int(sum(molehill_masterlist) // ((float(numberoflogis) + reset_number) - molehill_tally))
            ratio_index = []
                            
            for areas in range(len(molehill_index)):
                if molehill_index[areas] == 'valley':
                    ratio_index.append(valley_totals[areas] // goalnumber_final)
                    if ratio_index[areas] == 0:
                        ratio_index[areas] = 1

                if molehill_index[areas] == 'molehill':
                    ratio_index.append(1)

            #if sum(ratio_index) > int(firstchoice.get()) - molehill_tally:
                #ratio_index[ratio_index.index(max(ratio_index))] = max(ratio_index) - ((int(firstchoice.get()) - molehill_tally) - sum(ratio_index))
            
            if sum(ratio_index) != numberoflogis:
                ratio_index[ratio_index.index(max(ratio_index))] = max(ratio_index) + (numberoflogis - sum(ratio_index))
                
            print(ratio_index)
            print(molehill_index)

            firstindex = 0
            secondindex = 0

            print(ratio_index)
            for ratios in range(len(ratio_index)):
                if molehill_index[ratios] == 'valley':
                    for valleysize in range(ratio_index[ratios]):
                        while ordertotal_blank < goalnumber_final:

                            if secondindex == len(order_list):
                                print(firstindex)
                                if firstindex > len(order_list):
                                    firstindex = firstindex - (firstindex - len(order_list))

                                elif firstindex == len(order_list):
                                    firstindex = len(order_list) - 1

                                split.append(numbered_metro_list[firstindex])

                                ordertotal_blank = 0
                                break

                            if molehill_masterlist[secondindex] == 0:
                                split.append(numbered_metro_list[firstindex])
                                print(split)

                                firstindex = secondindex
                                ordertotal_blank = 0
                                break  

                            secondindex += 1
                            ordertotal_blank = sum((molehill_firstlist[firstindex:secondindex]))   

                
                        if ordertotal_blank >= int(goalnumber_modified):
                            split.append(numbered_metro_list[firstindex])

                            firstindex = secondindex 
                            ordertotal_blank = 0

                elif molehill_index[ratios] == 'molehill':
                    #if secondindex == len(order_list):
                            #split.append(numbered_metro_list[firstindex])
                            #break

                    while molehill_masterlist[firstindex] != 0:
                        if firstindex >= len(order_list):
                            split.append(numbered_metro_list[firstindex])
                            break

                        else:
                            firstindex += 1
                        
                    secondindex = firstindex

                    while molehill_masterlist[secondindex] == 0:
                        if secondindex == len(order_list):
                            split.append(numbered_metro_list[firstindex])
                            break
                        
                        else:
                            secondindex += 1                    

                    split.append(numbered_metro_list[firstindex])

                    firstindex = secondindex
                    ordertotal_blank = 0

        def saver():
            global saved_split
            saved_split = []

            if numberoflogis == 1:

                saved_split.append(input_last.get())

            if numberoflogis == 2: 

                saved_split.append(input_one.get())
                saved_split.append(input_last.get())

            if numberoflogis == 3:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_last.get())

            if numberoflogis == 4:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_last.get())

            if numberoflogis == 5:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_last.get())

            if numberoflogis == 6:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_last.get())  
                
            if numberoflogis == 7:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_last.get())

            if numberoflogis == 8:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_last.get())

            if numberoflogis == 9:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_last.get())

            if numberoflogis == 10:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_last.get())

            if numberoflogis == 11:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_last.get())

            if numberoflogis == 12:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_last.get())

            if numberoflogis == 13:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_last.get())

            if numberoflogis == 14:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_last.get())

            if numberoflogis == 15:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_last.get())

            if numberoflogis == 16:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_last.get())

            if numberoflogis == 17:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_last.get())

            if numberoflogis == 18:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_last.get())

            if numberoflogis == 19:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_last.get())

            if numberoflogis == 20:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_last.get())

            if numberoflogis == 21:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_last.get())

            if numberoflogis == 22:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_last.get())

            if numberoflogis == 23:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_twentytwo.get())
                saved_split.append(input_last.get())

            if numberoflogis == 24:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_twentytwo.get())
                saved_split.append(input_twentythree.get())
                saved_split.append(input_last.get())

            if numberoflogis == 25:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_twentytwo.get())
                saved_split.append(input_twentythree.get())
                saved_split.append(input_twentyfour.get())
                saved_split.append(input_last.get())

            if numberoflogis == 26:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_twentytwo.get())
                saved_split.append(input_twentythree.get())
                saved_split.append(input_twentyfour.get())
                saved_split.append(input_twentyfive.get())
                saved_split.append(input_last.get())

            if numberoflogis == 27:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_twentytwo.get())
                saved_split.append(input_twentythree.get())
                saved_split.append(input_twentyfour.get())
                saved_split.append(input_twentyfive.get())
                saved_split.append(input_twentysix.get())
                saved_split.append(input_last.get())

            if numberoflogis == 28:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_twentytwo.get())
                saved_split.append(input_twentythree.get())
                saved_split.append(input_twentyfour.get())
                saved_split.append(input_twentyfive.get())
                saved_split.append(input_twentysix.get())
                saved_split.append(input_twentyseven.get())
                saved_split.append(input_last.get())

            if numberoflogis == 29:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_twentytwo.get())
                saved_split.append(input_twentythree.get())
                saved_split.append(input_twentyfour.get())
                saved_split.append(input_twentyfive.get())
                saved_split.append(input_twentysix.get())
                saved_split.append(input_twentyseven.get())
                saved_split.append(input_twentyeight.get())
                saved_split.append(input_last.get())

            if numberoflogis == 30:

                saved_split.append(input_one.get())
                saved_split.append(input_two.get())
                saved_split.append(input_three.get())
                saved_split.append(input_four.get())
                saved_split.append(input_five.get())
                saved_split.append(input_six.get())
                saved_split.append(input_seven.get())
                saved_split.append(input_eight.get())
                saved_split.append(input_nine.get())
                saved_split.append(input_ten.get())
                saved_split.append(input_eleven.get())
                saved_split.append(input_twelve.get())
                saved_split.append(input_thirteen.get())
                saved_split.append(input_fourteen.get())
                saved_split.append(input_fifteen.get())
                saved_split.append(input_sixteen.get())
                saved_split.append(input_seventeen.get())
                saved_split.append(input_eighteen.get())
                saved_split.append(input_nineteen.get())
                saved_split.append(input_twenty.get())
                saved_split.append(input_twentyone.get())
                saved_split.append(input_twentytwo.get())
                saved_split.append(input_twentythree.get())
                saved_split.append(input_twentyfour.get())
                saved_split.append(input_twentyfive.get())
                saved_split.append(input_twentysix.get())
                saved_split.append(input_twentyseven.get())
                saved_split.append(input_twentyeight.get())
                saved_split.append(input_twentynine.get())
                saved_split.append(input_last.get())

            global previous_helper_location 
            previous_helper_location = '+' + str(helper.winfo_x()) + '+' + str(helper.winfo_y())

        helper = tk.Tk()
        #helper.geometry('225x330+425+100')

        if return_check == 'Full':
            if previous_geometry == '255x60':
                helper.geometry('225x330+425+100')

            elif re.search('255x60.+', previous_geometry):
                if root.winfo_screenwidth() - (root.winfo_x() + 352 + 395) < 255:
                    #This is testing whether there's room for the Helper window after accounting for the size of the Branch window
                    #355 being the width of a regular Branch window, 395 = Helper width + optimal distance between Helper & Branch
                    helper.geometry('255x330' + helper_location_inverted)

                elif root.winfo_screenwidth() - (root.winfo_x() + 352 + 395) > 255:
                    helper.geometry('255x330' + helper_location)


            helper.title('\U0001F916 Handlebars \U0001F916')
            helperdisplay = tk.Text(helper)

            for values in helpertext:
                helperdisplay.insert(tk.END, values + '\n')

            helperdisplay.config(state='disabled')
            helperdisplay.pack()


        if numberoflogis_str == '1':
            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x60+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x60' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result 

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x175' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() +'''
----------------------------------------''')
                display_result = tk.Text(result, width=50, height=10)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=1, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=1, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=1, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=1, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_last.set(split[0])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))         

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=1, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_last.set(split[0])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            elif return_check == 'Half':

                input_last.set(saved_split[0])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))         

        if numberoflogis_str == '2':
            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x86+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x86' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')
                #result.geometry('352x175+20+40')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x175' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')
                display_result = tk.Text(result, width=50, height=10)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()            

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=2, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=2, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_last.set(split[1])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=2, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_last.set(split[1])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_last.get())]))) 
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_last.set(saved_split[1])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_last.get())]))) 
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

        if  numberoflogis_str == '3':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x109+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x109' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x175' + previous_location)
                else:
                    result.geometry(previous_geometry)                  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=10)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=1, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=1, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=3, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=3, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_last.set(split[2])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=3, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_last.set(split[2])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_last.get())])))  
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_last.set(saved_split[2])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_last.get())]))) 
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))
        
        if numberoflogis_str == '4':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x132+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x132' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x175' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=10)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()            

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=4, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=4, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_last.set(split[3])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=4, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_last.set(split[3])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_last.get())]))) 
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_last.set(saved_split[3])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_last.get())]))) 
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '5':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x155+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x155' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x175' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=10)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=5, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=5, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_last.set(split[4])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=5, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_last.set(split[4])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_last.get())])))  
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_last.set(saved_split[4])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_last.get())])))  
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '6':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x178+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x178' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x175' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_five.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=10)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=6, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=6, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_last.set(split[5])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=6, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_last.set(split[5])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_last.get())])))  
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_last.set(saved_split[5])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())])))  
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_last.get())])))  
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '7':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x201+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x201' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x195' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
----------------------------------------
1. Metro: ''' +   metro_list[numbered_metro_list.index(input_one.get())] + ' / Orders: ' + ordertotal_one.get() + '''
2. Metro: ''' +   metro_list[numbered_metro_list.index(input_two.get())] + ' / Orders: ' + ordertotal_two.get() + '''
3. Metro: ''' +   metro_list[numbered_metro_list.index(input_three.get())] + ' / Orders: ' + ordertotal_three.get() + '''
4. Metro: ''' +   metro_list[numbered_metro_list.index(input_four.get())] + ' / Orders: ' + ordertotal_four.get() + '''
5. Metro: ''' +   metro_list[numbered_metro_list.index(input_five.get())] + ' / Orders: ' + ordertotal_five.get() + '''
6. Metro: ''' +   metro_list[numbered_metro_list.index(input_six.get())] + ' / Orders: ' + ordertotal_six.get() + '''
7. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + ''' 
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=12)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=7, rowspan=2, column=2)  

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=7, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_last.set(split[6])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=7, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_last.set(split[6])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_last.set(saved_split[5])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())])))  
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())]))) 
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_last.get())]))) 
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '8':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x224+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x224' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x195' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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

                display_result = tk.Text(result, width=50, height=12)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=8, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=8, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_last.set(split[7])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=8, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_last.set(split[7])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_last.set(saved_split[7])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())])))  
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())]))) 
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())]))) 
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_last.get())])))
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '9':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('352x247+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('352x247' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('352.+', previous_geometry):
                    result.geometry('352x220' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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

                display_result = tk.Text(result, width=50, height=14)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=9, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=9, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_last.set(split[8])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=9, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_last.set(split[8])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_last.set(saved_split[8])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())])))  
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())]))) 
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())]))) 
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_last.get())])))
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '10':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x274+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x274' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x245' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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

                display_result = tk.Text(result, width=50, height=16)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=10, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=10, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_last.set(split[9])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=10, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_last.set(split[9])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_last.set(saved_split[9])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '11':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x297+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x297' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x260' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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

                display_result = tk.Text(result, width=50, height=17)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=11, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=11, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_last.set(split[10])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=11, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_last.set(split[10])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_last.set(saved_split[10])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '12':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')
            branch.geometry('360x320')

            if previous_geometry == '255x60':
                branch.geometry('360x320+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x320' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x275' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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

                display_result = tk.Text(result, width=50, height=18)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=12, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_last.set(split[11])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=12, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=12, rowspan=2, column=2)

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=12, column=1, sticky='w')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_last.set(split[11])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_last.set(saved_split[11])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '13':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')
            branch.geometry('360x343')

            if previous_geometry == '255x60':
                branch.geometry('360x343+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x343' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12p)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot12p)

            label_last = tk.Label(branch, text='13')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=12, column=0, padx=5)
            option_last.grid(row=12, column=1, padx=5)
            display_last.grid(row=12, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x290' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=19)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=13, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=13, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_last.set(split[12])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=13, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=13, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_last.set(split[12])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_last.set(saved_split[12])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '14':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x366+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x366' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13p)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot13p)

            label_last = tk.Label(branch, text='14')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=13, column=0, padx=5)
            option_last.grid(row=13, column=1, padx=5)
            display_last.grid(row=13, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x300' + previous_location)
                else:
                    result.geometry(previous_geometry) 

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=20)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=14, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=14, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_last.set(split[13])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=14, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=14, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_last.set(split[13])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_last.set(saved_split[13])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '15':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x389+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x389' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14p)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot14p)

            label_last = tk.Label(branch, text='15')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=14, column=0, padx=5)
            option_last.grid(row=14, column=1, padx=5)
            display_last.grid(row=14, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x315' + previous_location)
                else:
                    result.geometry(previous_geometry) 

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=21)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=15, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=15, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_last.set(split[14])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=15, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=15, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_last.set(split[14])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_last.set(saved_split[14])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '16':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x415+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x415' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15p)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot15p)

            label_last = tk.Label(branch, text='16')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=15, column=0, padx=5)
            option_last.grid(row=15, column=1, padx=5)
            display_last.grid(row=15, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x325' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=22)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=16, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=16, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()

                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_last.set(split[15])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=16, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_last.set(split[15])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_last.set(saved_split[15])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '17':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x440+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x440' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16p)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot16p)

            label_last = tk.Label(branch, text='17')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=16, column=0, padx=5)
            option_last.grid(row=16, column=1, padx=5)
            display_last.grid(row=16, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x340' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=23)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=17, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=17, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_last.set(split[16])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=17, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=17, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_last.set(split[16])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_last.set(saved_split[16])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '18':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x465+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x465' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17p)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot17p)

            label_last = tk.Label(branch, text='18')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=17, column=0, padx=5)
            option_last.grid(row=17, column=1, padx=5)
            display_last.grid(row=17, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x350' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=24)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=18, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=18, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_last.set(split[17])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=18, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=18, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_last.set(split[17])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_last.set(saved_split[17])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '19':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x487+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x487' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18p)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot18p)

            label_last = tk.Label(branch, text='19')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=18, column=0, padx=5)
            option_last.grid(row=18, column=1, padx=5)
            display_last.grid(row=18, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x365' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=25)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=19, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=19, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_last.set(split[18])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=19, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=19, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_last.set(split[18])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_last.set(saved_split[18])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '20':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x512+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x512' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19p)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot19p)

            label_last = tk.Label(branch, text='20')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=19, column=0, padx=5)
            option_last.grid(row=19, column=1, padx=5)
            display_last.grid(row=19, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x378' + previous_location)
                else:
                    result.geometry(previous_geometry) 

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=26)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=20, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=20, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_last.set(split[19])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=20, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=20, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_last.set(split[19])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_last.set(saved_split[19])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '21':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x535+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x535' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20p)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot20p)

            label_last = tk.Label(branch, text='21')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=20, column=0, padx=5)
            option_last.grid(row=20, column=1, padx=5)
            display_last.grid(row=20, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x391' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=27)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=21, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=21, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_last.set(split[20])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=21, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=21, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_last.set(split[20])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_last.set(saved_split[20])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '22':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x560+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x560' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21p)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot21p)

            label_last = tk.Label(branch, text='22')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=21, column=0, padx=5)
            option_last.grid(row=21, column=1, padx=5)
            display_last.grid(row=21, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x404' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=28)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=22, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=22, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_last.set(split[21])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=22, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=22, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_last.set(split[21])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_last.set(saved_split[21])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '23':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')
            branch.geometry('360x577')

            if previous_geometry == '255x60':
                branch.geometry('360x584+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x584' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_twentytwo = tk.StringVar(branch)
            ordertotal_twentytwo.set('# of Orders')

            input_twentytwo = tk.StringVar(branch)
            input_twentytwo.set(numbered_metro_list[0])
            option_twentytwo = tk.OptionMenu(branch, input_twentytwo, *numbered_metro_list, command=select22p)
            option_twentytwo.config(width=20)
            input_twentytwo.trace_add("write", scoot21)

            label_twentytwo = tk.Label(branch, text='22')
            display_twentytwo = tk.Label(branch, width=10, textvariable=ordertotal_twentytwo)

            label_twentytwo.grid(row=21, column=0, padx=5)
            option_twentytwo.grid(row=21, column=1, padx=5)
            display_twentytwo.grid(row=21, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot22p)

            label_last = tk.Label(branch, text='23')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=22, column=0, padx=5)
            option_last.grid(row=22, column=1, padx=5)
            display_last.grid(row=22, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x418' + previous_location)
                else:
                    result.geometry(previous_geometry) 

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentytwo.get())] + ' / Orders: ' + ordertotal_twentytwo.get() + '''
23. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=29)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=23, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=23, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_last.set(split[22])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=23, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_last.set(split[22])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_twentytwo.set(saved_split[21])
                input_last.set(saved_split[22])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '24':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x609+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x609' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_twentytwo = tk.StringVar(branch)
            ordertotal_twentytwo.set('# of Orders')

            input_twentytwo = tk.StringVar(branch)
            input_twentytwo.set(numbered_metro_list[0])
            option_twentytwo = tk.OptionMenu(branch, input_twentytwo, *numbered_metro_list, command=select22)
            option_twentytwo.config(width=20)
            input_twentytwo.trace_add("write", scoot21)

            label_twentytwo = tk.Label(branch, text='22')
            display_twentytwo = tk.Label(branch, width=10, textvariable=ordertotal_twentytwo)

            label_twentytwo.grid(row=21, column=0, padx=5)
            option_twentytwo.grid(row=21, column=1, padx=5)
            display_twentytwo.grid(row=21, column=2,columnspan=2)

            ordertotal_twentythree = tk.StringVar(branch)
            ordertotal_twentythree.set('# of Orders')

            input_twentythree = tk.StringVar(branch)
            input_twentythree.set(numbered_metro_list[0])
            option_twentythree = tk.OptionMenu(branch, input_twentythree, *numbered_metro_list, command=select23p)
            option_twentythree.config(width=20)
            input_twentythree.trace_add("write", scoot22)

            label_twentythree = tk.Label(branch, text='23')
            display_twentythree = tk.Label(branch, width=10, textvariable=ordertotal_twentythree)

            label_twentythree.grid(row=22, column=0, padx=5)
            option_twentythree.grid(row=22, column=1, padx=5)
            display_twentythree.grid(row=22, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot23p)

            label_last = tk.Label(branch, text='24')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=23, column=0, padx=5)
            option_last.grid(row=23, column=1, padx=5)
            display_last.grid(row=23, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x429' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentytwo.get())] + ' / Orders: ' + ordertotal_twentytwo.get() + '''
23. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentythree.get())] + ' / Orders: ' + ordertotal_twentythree.get() + '''
24. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=30)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)
                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=24, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=24, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_last.set(split[23])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=24, column=1, sticky='e')

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=24, rowspan=2, column=2)

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_last.set(split[23])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_twentytwo.set(saved_split[21])
                input_twentythree.set(saved_split[22])
                input_last.set(saved_split[23])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_last.get())])))   
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '25':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x632+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x632' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_twentytwo = tk.StringVar(branch)
            ordertotal_twentytwo.set('# of Orders')

            input_twentytwo = tk.StringVar(branch)
            input_twentytwo.set(numbered_metro_list[0])
            option_twentytwo = tk.OptionMenu(branch, input_twentytwo, *numbered_metro_list, command=select22)
            option_twentytwo.config(width=20)
            input_twentytwo.trace_add("write", scoot21)

            label_twentytwo = tk.Label(branch, text='22')
            display_twentytwo = tk.Label(branch, width=10, textvariable=ordertotal_twentytwo)

            label_twentytwo.grid(row=21, column=0, padx=5)
            option_twentytwo.grid(row=21, column=1, padx=5)
            display_twentytwo.grid(row=21, column=2,columnspan=2)

            ordertotal_twentythree = tk.StringVar(branch)
            ordertotal_twentythree.set('# of Orders')

            input_twentythree = tk.StringVar(branch)
            input_twentythree.set(numbered_metro_list[0])
            option_twentythree = tk.OptionMenu(branch, input_twentythree, *numbered_metro_list, command=select23)
            option_twentythree.config(width=20)
            input_twentythree.trace_add("write", scoot22)

            label_twentythree = tk.Label(branch, text='23')
            display_twentythree = tk.Label(branch, width=10, textvariable=ordertotal_twentythree)

            label_twentythree.grid(row=22, column=0, padx=5)
            option_twentythree.grid(row=22, column=1, padx=5)
            display_twentythree.grid(row=22, column=2,columnspan=2)

            ordertotal_twentyfour = tk.StringVar(branch)
            ordertotal_twentyfour.set('# of Orders')

            input_twentyfour = tk.StringVar(branch)
            input_twentyfour.set(numbered_metro_list[0])
            option_twentyfour = tk.OptionMenu(branch, input_twentyfour, *numbered_metro_list, command=select24p)
            option_twentyfour.config(width=20)
            input_twentyfour.trace_add("write", scoot23)

            label_twentyfour = tk.Label(branch, text='24')
            display_twentyfour = tk.Label(branch, width=10, textvariable=ordertotal_twentyfour)

            label_twentyfour.grid(row=23, column=0, padx=5)
            option_twentyfour.grid(row=23, column=1, padx=5)
            display_twentyfour.grid(row=23, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot24p)

            label_last = tk.Label(branch, text='25')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=24, column=0, padx=5)
            option_last.grid(row=24, column=1, padx=5)
            display_last.grid(row=24, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x442' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentytwo.get())] + ' / Orders: ' + ordertotal_twentytwo.get() + '''
23. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentythree.get())] + ' / Orders: ' + ordertotal_twentythree.get() + '''
24. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfour.get())] + ' / Orders: ' + ordertotal_twentyfour.get() + '''
25. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=31)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)
                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=25, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=25, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_last.set(split[24])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=25, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_last.set(split[24])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_twentytwo.set(saved_split[21])
                input_twentythree.set(saved_split[22])
                input_twentyfour.set(saved_split[23])
                input_last.set(saved_split[24])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '26':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x655+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x655' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_twentytwo = tk.StringVar(branch)
            ordertotal_twentytwo.set('# of Orders')

            input_twentytwo = tk.StringVar(branch)
            input_twentytwo.set(numbered_metro_list[0])
            option_twentytwo = tk.OptionMenu(branch, input_twentytwo, *numbered_metro_list, command=select22)
            option_twentytwo.config(width=20)
            input_twentytwo.trace_add("write", scoot21)

            label_twentytwo = tk.Label(branch, text='22')
            display_twentytwo = tk.Label(branch, width=10, textvariable=ordertotal_twentytwo)

            label_twentytwo.grid(row=21, column=0, padx=5)
            option_twentytwo.grid(row=21, column=1, padx=5)
            display_twentytwo.grid(row=21, column=2,columnspan=2)

            ordertotal_twentythree = tk.StringVar(branch)
            ordertotal_twentythree.set('# of Orders')

            input_twentythree = tk.StringVar(branch)
            input_twentythree.set(numbered_metro_list[0])
            option_twentythree = tk.OptionMenu(branch, input_twentythree, *numbered_metro_list, command=select23)
            option_twentythree.config(width=20)
            input_twentythree.trace_add("write", scoot22)

            label_twentythree = tk.Label(branch, text='23')
            display_twentythree = tk.Label(branch, width=10, textvariable=ordertotal_twentythree)

            label_twentythree.grid(row=22, column=0, padx=5)
            option_twentythree.grid(row=22, column=1, padx=5)
            display_twentythree.grid(row=22, column=2,columnspan=2)

            ordertotal_twentyfour = tk.StringVar(branch)
            ordertotal_twentyfour.set('# of Orders')

            input_twentyfour = tk.StringVar(branch)
            input_twentyfour.set(numbered_metro_list[0])
            option_twentyfour = tk.OptionMenu(branch, input_twentyfour, *numbered_metro_list, command=select24)
            option_twentyfour.config(width=20)
            input_twentyfour.trace_add("write", scoot23)

            label_twentyfour = tk.Label(branch, text='24')
            display_twentyfour = tk.Label(branch, width=10, textvariable=ordertotal_twentyfour)

            label_twentyfour.grid(row=23, column=0, padx=5)
            option_twentyfour.grid(row=23, column=1, padx=5)
            display_twentyfour.grid(row=23, column=2,columnspan=2)

            ordertotal_twentyfive = tk.StringVar(branch)
            ordertotal_twentyfive.set('# of Orders')

            input_twentyfive = tk.StringVar(branch)
            input_twentyfive.set(numbered_metro_list[0])
            option_twentyfive = tk.OptionMenu(branch, input_twentyfive, *numbered_metro_list, command=select25p)
            option_twentyfive.config(width=20)
            input_twentyfive.trace_add("write", scoot24)

            label_twentyfive = tk.Label(branch, text='25')
            display_twentyfive = tk.Label(branch, width=10, textvariable=ordertotal_twentyfive)

            label_twentyfive.grid(row=24, column=0, padx=5)
            option_twentyfive.grid(row=24, column=1, padx=5)
            display_twentyfive.grid(row=24, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot25p)

            label_last = tk.Label(branch, text='26')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=25, column=0, padx=5)
            option_last.grid(row=25, column=1, padx=5)
            display_last.grid(row=25, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x455' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentytwo.get())] + ' / Orders: ' + ordertotal_twentytwo.get() + '''
23. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentythree.get())] + ' / Orders: ' + ordertotal_twentythree.get() + '''
24. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfour.get())] + ' / Orders: ' + ordertotal_twentyfour.get() + '''
25. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfive.get())] + ' / Orders: ' + ordertotal_twentyfive.get() + '''
26. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=32)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=26, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=26, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                print(len(split))
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_last.set(split[25])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=26, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_last.set(split[25])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_twentytwo.set(saved_split[21])
                input_twentythree.set(saved_split[22])
                input_twentyfour.set(saved_split[23])
                input_twentyfive.set(saved_split[24])
                input_last.set(saved_split[25])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '27':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x680+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x680' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_twentytwo = tk.StringVar(branch)
            ordertotal_twentytwo.set('# of Orders')

            input_twentytwo = tk.StringVar(branch)
            input_twentytwo.set(numbered_metro_list[0])
            option_twentytwo = tk.OptionMenu(branch, input_twentytwo, *numbered_metro_list, command=select22)
            option_twentytwo.config(width=20)
            input_twentytwo.trace_add("write", scoot21)

            label_twentytwo = tk.Label(branch, text='22')
            display_twentytwo = tk.Label(branch, width=10, textvariable=ordertotal_twentytwo)

            label_twentytwo.grid(row=21, column=0, padx=5)
            option_twentytwo.grid(row=21, column=1, padx=5)
            display_twentytwo.grid(row=21, column=2,columnspan=2)

            ordertotal_twentythree = tk.StringVar(branch)
            ordertotal_twentythree.set('# of Orders')

            input_twentythree = tk.StringVar(branch)
            input_twentythree.set(numbered_metro_list[0])
            option_twentythree = tk.OptionMenu(branch, input_twentythree, *numbered_metro_list, command=select23)
            option_twentythree.config(width=20)
            input_twentythree.trace_add("write", scoot22)

            label_twentythree = tk.Label(branch, text='23')
            display_twentythree = tk.Label(branch, width=10, textvariable=ordertotal_twentythree)

            label_twentythree.grid(row=22, column=0, padx=5)
            option_twentythree.grid(row=22, column=1, padx=5)
            display_twentythree.grid(row=22, column=2,columnspan=2)

            ordertotal_twentyfour = tk.StringVar(branch)
            ordertotal_twentyfour.set('# of Orders')

            input_twentyfour = tk.StringVar(branch)
            input_twentyfour.set(numbered_metro_list[0])
            option_twentyfour = tk.OptionMenu(branch, input_twentyfour, *numbered_metro_list, command=select24)
            option_twentyfour.config(width=20)
            input_twentyfour.trace_add("write", scoot23)

            label_twentyfour = tk.Label(branch, text='24')
            display_twentyfour = tk.Label(branch, width=10, textvariable=ordertotal_twentyfour)

            label_twentyfour.grid(row=23, column=0, padx=5)
            option_twentyfour.grid(row=23, column=1, padx=5)
            display_twentyfour.grid(row=23, column=2,columnspan=2)

            ordertotal_twentyfive = tk.StringVar(branch)
            ordertotal_twentyfive.set('# of Orders')

            input_twentyfive = tk.StringVar(branch)
            input_twentyfive.set(numbered_metro_list[0])
            option_twentyfive = tk.OptionMenu(branch, input_twentyfive, *numbered_metro_list, command=select25)
            option_twentyfive.config(width=20)
            input_twentyfive.trace_add("write", scoot24)

            label_twentyfive = tk.Label(branch, text='25')
            display_twentyfive = tk.Label(branch, width=10, textvariable=ordertotal_twentyfive)

            label_twentyfive.grid(row=24, column=0, padx=5)
            option_twentyfive.grid(row=24, column=1, padx=5)
            display_twentyfive.grid(row=24, column=2,columnspan=2)

            ordertotal_twentysix = tk.StringVar(branch)
            ordertotal_twentysix.set('# of Orders')

            input_twentysix = tk.StringVar(branch)
            input_twentysix.set(numbered_metro_list[0])
            option_twentysix = tk.OptionMenu(branch, input_twentysix, *numbered_metro_list, command=select26p)
            option_twentysix.config(width=20)
            input_twentysix.trace_add("write", scoot25)

            label_twentysix = tk.Label(branch, text='26')
            display_twentysix = tk.Label(branch, width=10, textvariable=ordertotal_twentysix)

            label_twentysix.grid(row=25, column=0, padx=5)
            option_twentysix.grid(row=25, column=1, padx=5)
            display_twentysix.grid(row=25, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot26p)

            label_last = tk.Label(branch, text='27')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=26, column=0, padx=5)
            option_last.grid(row=26, column=1, padx=5)
            display_last.grid(row=26, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x470' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentytwo.get())] + ' / Orders: ' + ordertotal_twentytwo.get() + '''
23. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentythree.get())] + ' / Orders: ' + ordertotal_twentythree.get() + '''
24. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfour.get())] + ' / Orders: ' + ordertotal_twentyfour.get() + '''
25. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfive.get())] + ' / Orders: ' + ordertotal_twentyfive.get() + '''
26. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentysix.get())] + ' / Orders: ' + ordertotal_twentysix.get() + '''
27. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=33)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)
                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=27, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=27, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_twentysix.set(split[25])
                input_last.set(split[26])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=27, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_twentysix.set(split[25])
                input_last.set(split[26])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))
                ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_twentytwo.set(saved_split[21])
                input_twentythree.set(saved_split[22])
                input_twentyfour.set(saved_split[23])
                input_twentyfive.set(saved_split[24])
                input_twentysix.set(saved_split[25])
                input_last.set(saved_split[26])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))
                ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '28':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x704+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x704' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_twentytwo = tk.StringVar(branch)
            ordertotal_twentytwo.set('# of Orders')

            input_twentytwo = tk.StringVar(branch)
            input_twentytwo.set(numbered_metro_list[0])
            option_twentytwo = tk.OptionMenu(branch, input_twentytwo, *numbered_metro_list, command=select22)
            option_twentytwo.config(width=20)
            input_twentytwo.trace_add("write", scoot21)

            label_twentytwo = tk.Label(branch, text='22')
            display_twentytwo = tk.Label(branch, width=10, textvariable=ordertotal_twentytwo)

            label_twentytwo.grid(row=21, column=0, padx=5)
            option_twentytwo.grid(row=21, column=1, padx=5)
            display_twentytwo.grid(row=21, column=2,columnspan=2)

            ordertotal_twentythree = tk.StringVar(branch)
            ordertotal_twentythree.set('# of Orders')

            input_twentythree = tk.StringVar(branch)
            input_twentythree.set(numbered_metro_list[0])
            option_twentythree = tk.OptionMenu(branch, input_twentythree, *numbered_metro_list, command=select23)
            option_twentythree.config(width=20)
            input_twentythree.trace_add("write", scoot22)

            label_twentythree = tk.Label(branch, text='23')
            display_twentythree = tk.Label(branch, width=10, textvariable=ordertotal_twentythree)

            label_twentythree.grid(row=22, column=0, padx=5)
            option_twentythree.grid(row=22, column=1, padx=5)
            display_twentythree.grid(row=22, column=2,columnspan=2)

            ordertotal_twentyfour = tk.StringVar(branch)
            ordertotal_twentyfour.set('# of Orders')

            input_twentyfour = tk.StringVar(branch)
            input_twentyfour.set(numbered_metro_list[0])
            option_twentyfour = tk.OptionMenu(branch, input_twentyfour, *numbered_metro_list, command=select24)
            option_twentyfour.config(width=20)
            input_twentyfour.trace_add("write", scoot23)

            label_twentyfour = tk.Label(branch, text='24')
            display_twentyfour = tk.Label(branch, width=10, textvariable=ordertotal_twentyfour)

            label_twentyfour.grid(row=23, column=0, padx=5)
            option_twentyfour.grid(row=23, column=1, padx=5)
            display_twentyfour.grid(row=23, column=2,columnspan=2)

            ordertotal_twentyfive = tk.StringVar(branch)
            ordertotal_twentyfive.set('# of Orders')

            input_twentyfive = tk.StringVar(branch)
            input_twentyfive.set(numbered_metro_list[0])
            option_twentyfive = tk.OptionMenu(branch, input_twentyfive, *numbered_metro_list, command=select25)
            option_twentyfive.config(width=20)
            input_twentyfive.trace_add("write", scoot24)

            label_twentyfive = tk.Label(branch, text='25')
            display_twentyfive = tk.Label(branch, width=10, textvariable=ordertotal_twentyfive)

            label_twentyfive.grid(row=24, column=0, padx=5)
            option_twentyfive.grid(row=24, column=1, padx=5)
            display_twentyfive.grid(row=24, column=2,columnspan=2)

            ordertotal_twentysix = tk.StringVar(branch)
            ordertotal_twentysix.set('# of Orders')

            input_twentysix = tk.StringVar(branch)
            input_twentysix.set(numbered_metro_list[0])
            option_twentysix = tk.OptionMenu(branch, input_twentysix, *numbered_metro_list, command=select26)
            option_twentysix.config(width=20)
            input_twentysix.trace_add("write", scoot25)

            label_twentysix = tk.Label(branch, text='26')
            display_twentysix = tk.Label(branch, width=10, textvariable=ordertotal_twentysix)

            label_twentysix.grid(row=25, column=0, padx=5)
            option_twentysix.grid(row=25, column=1, padx=5)
            display_twentysix.grid(row=25, column=2,columnspan=2)

            ordertotal_twentyseven = tk.StringVar(branch)
            ordertotal_twentyseven.set('# of Orders')

            input_twentyseven = tk.StringVar(branch)
            input_twentyseven.set(numbered_metro_list[0])
            option_twentyseven = tk.OptionMenu(branch, input_twentyseven, *numbered_metro_list, command=select27p)
            option_twentyseven.config(width=20)
            input_twentyseven.trace_add("write", scoot26)

            label_twentyseven = tk.Label(branch, text='27')
            display_twentyseven = tk.Label(branch, width=10, textvariable=ordertotal_twentyseven)

            label_twentyseven.grid(row=26, column=0, padx=5)
            option_twentyseven.grid(row=26, column=1, padx=5)
            display_twentyseven.grid(row=26, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot27p)

            label_last = tk.Label(branch, text='28')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=27, column=0, padx=5)
            option_last.grid(row=27, column=1, padx=5)
            display_last.grid(row=27, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x483' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentytwo.get())] + ' / Orders: ' + ordertotal_twentytwo.get() + '''
23. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentythree.get())] + ' / Orders: ' + ordertotal_twentythree.get() + '''
24. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfour.get())] + ' / Orders: ' + ordertotal_twentyfour.get() + '''
25. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfive.get())] + ' / Orders: ' + ordertotal_twentyfive.get() + '''
26. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentysix.get())] + ' / Orders: ' + ordertotal_twentysix.get() + '''
27. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyseven.get())] + ' / Orders: ' + ordertotal_twentyseven.get() + '''
28. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=34)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=28, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=28, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_twentysix.set(split[25])
                input_twentyseven.set(split[26])
                input_last.set(split[27])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=28, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_twentysix.set(split[25])
                input_twentyseven.set(split[26])
                input_last.set(split[27])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))
                ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_twentyseven.get())])))
                ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_twentytwo.set(saved_split[21])
                input_twentythree.set(saved_split[22])
                input_twentyfour.set(saved_split[23])
                input_twentyfive.set(saved_split[24])
                input_twentysix.set(saved_split[25])
                input_twentyseven.set(saved_split[26])
                input_last.set(saved_split[27])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))
                ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_twentyseven.get())])))
                ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '29':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')

            if previous_geometry == '255x60':
                branch.geometry('360x727+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x727' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_twentytwo = tk.StringVar(branch)
            ordertotal_twentytwo.set('# of Orders')

            input_twentytwo = tk.StringVar(branch)
            input_twentytwo.set(numbered_metro_list[0])
            option_twentytwo = tk.OptionMenu(branch, input_twentytwo, *numbered_metro_list, command=select22)
            option_twentytwo.config(width=20)
            input_twentytwo.trace_add("write", scoot21)

            label_twentytwo = tk.Label(branch, text='22')
            display_twentytwo = tk.Label(branch, width=10, textvariable=ordertotal_twentytwo)

            label_twentytwo.grid(row=21, column=0, padx=5)
            option_twentytwo.grid(row=21, column=1, padx=5)
            display_twentytwo.grid(row=21, column=2,columnspan=2)

            ordertotal_twentythree = tk.StringVar(branch)
            ordertotal_twentythree.set('# of Orders')

            input_twentythree = tk.StringVar(branch)
            input_twentythree.set(numbered_metro_list[0])
            option_twentythree = tk.OptionMenu(branch, input_twentythree, *numbered_metro_list, command=select23)
            option_twentythree.config(width=20)
            input_twentythree.trace_add("write", scoot22)

            label_twentythree = tk.Label(branch, text='23')
            display_twentythree = tk.Label(branch, width=10, textvariable=ordertotal_twentythree)

            label_twentythree.grid(row=22, column=0, padx=5)
            option_twentythree.grid(row=22, column=1, padx=5)
            display_twentythree.grid(row=22, column=2,columnspan=2)

            ordertotal_twentyfour = tk.StringVar(branch)
            ordertotal_twentyfour.set('# of Orders')

            input_twentyfour = tk.StringVar(branch)
            input_twentyfour.set(numbered_metro_list[0])
            option_twentyfour = tk.OptionMenu(branch, input_twentyfour, *numbered_metro_list, command=select24)
            option_twentyfour.config(width=20)
            input_twentyfour.trace_add("write", scoot23)

            label_twentyfour = tk.Label(branch, text='24')
            display_twentyfour = tk.Label(branch, width=10, textvariable=ordertotal_twentyfour)

            label_twentyfour.grid(row=23, column=0, padx=5)
            option_twentyfour.grid(row=23, column=1, padx=5)
            display_twentyfour.grid(row=23, column=2,columnspan=2)

            ordertotal_twentyfive = tk.StringVar(branch)
            ordertotal_twentyfive.set('# of Orders')

            input_twentyfive = tk.StringVar(branch)
            input_twentyfive.set(numbered_metro_list[0])
            option_twentyfive = tk.OptionMenu(branch, input_twentyfive, *numbered_metro_list, command=select25)
            option_twentyfive.config(width=20)
            input_twentyfive.trace_add("write", scoot24)

            label_twentyfive = tk.Label(branch, text='25')
            display_twentyfive = tk.Label(branch, width=10, textvariable=ordertotal_twentyfive)

            label_twentyfive.grid(row=24, column=0, padx=5)
            option_twentyfive.grid(row=24, column=1, padx=5)
            display_twentyfive.grid(row=24, column=2,columnspan=2)

            ordertotal_twentysix = tk.StringVar(branch)
            ordertotal_twentysix.set('# of Orders')

            input_twentysix = tk.StringVar(branch)
            input_twentysix.set(numbered_metro_list[0])
            option_twentysix = tk.OptionMenu(branch, input_twentysix, *numbered_metro_list, command=select26)
            option_twentysix.config(width=20)
            input_twentysix.trace_add("write", scoot25)

            label_twentysix = tk.Label(branch, text='26')
            display_twentysix = tk.Label(branch, width=10, textvariable=ordertotal_twentysix)

            label_twentysix.grid(row=25, column=0, padx=5)
            option_twentysix.grid(row=25, column=1, padx=5)
            display_twentysix.grid(row=25, column=2,columnspan=2)

            ordertotal_twentyseven = tk.StringVar(branch)
            ordertotal_twentyseven.set('# of Orders')

            input_twentyseven = tk.StringVar(branch)
            input_twentyseven.set(numbered_metro_list[0])
            option_twentyseven = tk.OptionMenu(branch, input_twentyseven, *numbered_metro_list, command=select27)
            option_twentyseven.config(width=20)
            input_twentyseven.trace_add("write", scoot26)

            label_twentyseven = tk.Label(branch, text='27')
            display_twentyseven = tk.Label(branch, width=10, textvariable=ordertotal_twentyseven)

            label_twentyseven.grid(row=26, column=0, padx=5)
            option_twentyseven.grid(row=26, column=1, padx=5)
            display_twentyseven.grid(row=26, column=2,columnspan=2)

            ordertotal_twentyeight = tk.StringVar(branch)
            ordertotal_twentyeight.set('# of Orders')

            input_twentyeight = tk.StringVar(branch)
            input_twentyeight.set(numbered_metro_list[0])
            option_twentyeight = tk.OptionMenu(branch, input_twentyeight, *numbered_metro_list, command=select28p)
            option_twentyeight.config(width=20)
            input_twentyeight.trace_add("write", scoot27)

            label_twentyeight = tk.Label(branch, text='28')
            display_twentyeight = tk.Label(branch, width=10, textvariable=ordertotal_twentyeight)

            label_twentyeight.grid(row=27, column=0, padx=5)
            option_twentyeight.grid(row=27, column=1, padx=5)
            display_twentyeight.grid(row=27, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot28p)

            label_last = tk.Label(branch, text='29')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=28, column=0, padx=5)
            option_last.grid(row=28, column=1, padx=5)
            display_last.grid(row=28, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x497' + previous_location)
                else:
                    result.geometry(previous_geometry)  

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentytwo.get())] + ' / Orders: ' + ordertotal_twentytwo.get() + '''
23. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentythree.get())] + ' / Orders: ' + ordertotal_twentythree.get() + '''
24. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfour.get())] + ' / Orders: ' + ordertotal_twentyfour.get() + '''
25. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfive.get())] + ' / Orders: ' + ordertotal_twentyfive.get() + '''
26. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentysix.get())] + ' / Orders: ' + ordertotal_twentysix.get() + '''
27. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyseven.get())] + ' / Orders: ' + ordertotal_twentyseven.get() + '''
28. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyeight.get())] + ' / Orders: ' + ordertotal_twentyeight.get() + '''
29. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
----------------------------------------''')

                display_result = tk.Text(result, width=50, height=35)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)


                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=29, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=29, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_twentysix.set(split[25])
                input_twentyseven.set(split[26])
                input_twentyeight.set(split[27])
                input_last.set(split[28])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=29, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_twentysix.set(split[25])
                input_twentyseven.set(split[26])
                input_twentyeight.set(split[27])
                input_last.set(split[28])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))
                ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_twentyseven.get())])))
                ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_twentyeight.get())])))
                ordertotal_twentyeight.set(str(sum(order_list[numbered_metro_list.index(input_twentyeight.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_twentytwo.set(saved_split[21])
                input_twentythree.set(saved_split[22])
                input_twentyfour.set(saved_split[23])
                input_twentyfive.set(saved_split[24])
                input_twentysix.set(saved_split[25])
                input_twentyseven.set(saved_split[26])
                input_twentyeight.set(saved_split[27])
                input_last.set(saved_split[28])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))
                ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_twentyseven.get())])))
                ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_twentyeight.get())])))
                ordertotal_twentyeight.set(str(sum(order_list[numbered_metro_list.index(input_twentyeight.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if numberoflogis_str == '30':

            branch = tk.Tk()
            branch.title('\N{rocket} Scooter 1.1 \N{rocket}')
            branch.geometry('360x752')

            if previous_geometry == '255x60':
                branch.geometry('360x752+20+40')

            elif re.search('255x60.+', previous_geometry):
                branch.geometry('360x752' + previous_location)

            else:
                branch.geometry(previous_geometry)

            #root.destroy()

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
            option_eleven = tk.OptionMenu(branch, input_eleven, *numbered_metro_list, command=select11)
            option_eleven.config(width=20)
            input_eleven.trace_add("write", scoot10)

            label_eleven = tk.Label(branch, text='11')
            display_eleven = tk.Label(branch, width=10, textvariable=ordertotal_eleven)

            label_eleven.grid(row=10, column=0, padx=5)
            option_eleven.grid(row=10, column=1, padx=5)
            display_eleven.grid(row=10, column=2,columnspan=2)

            ordertotal_twelve = tk.StringVar(branch)
            ordertotal_twelve.set('# of Orders')

            input_twelve = tk.StringVar(branch)
            input_twelve.set(numbered_metro_list[0])
            option_twelve = tk.OptionMenu(branch, input_twelve, *numbered_metro_list, command=select12)
            option_twelve.config(width=20)
            input_twelve.trace_add("write", scoot11)

            label_twelve = tk.Label(branch, text='12')
            display_twelve = tk.Label(branch, width=10, textvariable=ordertotal_twelve)

            label_twelve.grid(row=11, column=0, padx=5)
            option_twelve.grid(row=11, column=1, padx=5)
            display_twelve.grid(row=11, column=2,columnspan=2)

            ordertotal_thirteen = tk.StringVar(branch)
            ordertotal_thirteen.set('# of Orders')

            input_thirteen = tk.StringVar(branch)
            input_thirteen.set(numbered_metro_list[0])
            option_thirteen = tk.OptionMenu(branch, input_thirteen, *numbered_metro_list, command=select13)
            option_thirteen.config(width=20)
            input_thirteen.trace_add("write", scoot12)

            label_thirteen = tk.Label(branch, text='13')
            display_thirteen = tk.Label(branch, width=10, textvariable=ordertotal_thirteen)

            label_thirteen.grid(row=12, column=0, padx=5)
            option_thirteen.grid(row=12, column=1, padx=5)
            display_thirteen.grid(row=12, column=2,columnspan=2)

            ordertotal_fourteen = tk.StringVar(branch)
            ordertotal_fourteen.set('# of Orders')

            input_fourteen = tk.StringVar(branch)
            input_fourteen.set(numbered_metro_list[0])
            option_fourteen = tk.OptionMenu(branch, input_fourteen, *numbered_metro_list, command=select14)
            option_fourteen.config(width=20)
            input_fourteen.trace_add("write", scoot13)

            label_fourteen = tk.Label(branch, text='14')
            display_fourteen = tk.Label(branch, width=10, textvariable=ordertotal_fourteen)

            label_fourteen.grid(row=13, column=0, padx=5)
            option_fourteen.grid(row=13, column=1, padx=5)
            display_fourteen.grid(row=13, column=2,columnspan=2)

            ordertotal_fifteen = tk.StringVar(branch)
            ordertotal_fifteen.set('# of Orders')

            input_fifteen = tk.StringVar(branch)
            input_fifteen.set(numbered_metro_list[0])
            option_fifteen = tk.OptionMenu(branch, input_fifteen, *numbered_metro_list, command=select15)
            option_fifteen.config(width=20)
            input_fifteen.trace_add("write", scoot14)

            label_fifteen = tk.Label(branch, text='15')
            display_fifteen = tk.Label(branch, width=10, textvariable=ordertotal_fifteen)

            label_fifteen.grid(row=14, column=0, padx=5)
            option_fifteen.grid(row=14, column=1, padx=5)
            display_fifteen.grid(row=14, column=2,columnspan=2)

            ordertotal_sixteen = tk.StringVar(branch)
            ordertotal_sixteen.set('# of Orders')

            input_sixteen = tk.StringVar(branch)
            input_sixteen.set(numbered_metro_list[0])
            option_sixteen = tk.OptionMenu(branch, input_sixteen, *numbered_metro_list, command=select16)
            option_sixteen.config(width=20)
            input_sixteen.trace_add("write", scoot15)

            label_sixteen = tk.Label(branch, text='16')
            display_sixteen = tk.Label(branch, width=10, textvariable=ordertotal_sixteen)

            label_sixteen.grid(row=15, column=0, padx=5)
            option_sixteen.grid(row=15, column=1, padx=5)
            display_sixteen.grid(row=15, column=2,columnspan=2)

            ordertotal_seventeen = tk.StringVar(branch)
            ordertotal_seventeen.set('# of Orders')

            input_seventeen = tk.StringVar(branch)
            input_seventeen.set(numbered_metro_list[0])
            option_seventeen = tk.OptionMenu(branch, input_seventeen, *numbered_metro_list, command=select17)
            option_seventeen.config(width=20)
            input_seventeen.trace_add("write", scoot16)

            label_seventeen = tk.Label(branch, text='17')
            display_seventeen = tk.Label(branch, width=10, textvariable=ordertotal_seventeen)

            label_seventeen.grid(row=16, column=0, padx=5)
            option_seventeen.grid(row=16, column=1, padx=5)
            display_seventeen.grid(row=16, column=2,columnspan=2)

            ordertotal_eighteen = tk.StringVar(branch)
            ordertotal_eighteen.set('# of Orders')

            input_eighteen = tk.StringVar(branch)
            input_eighteen.set(numbered_metro_list[0])
            option_eighteen = tk.OptionMenu(branch, input_eighteen, *numbered_metro_list, command=select18)
            option_eighteen.config(width=20)
            input_eighteen.trace_add("write", scoot17)

            label_eighteen = tk.Label(branch, text='18')
            display_eighteen = tk.Label(branch, width=10, textvariable=ordertotal_eighteen)

            label_eighteen.grid(row=17, column=0, padx=5)
            option_eighteen.grid(row=17, column=1, padx=5)
            display_eighteen.grid(row=17, column=2,columnspan=2)

            ordertotal_nineteen = tk.StringVar(branch)
            ordertotal_nineteen.set('# of Orders')

            input_nineteen = tk.StringVar(branch)
            input_nineteen.set(numbered_metro_list[0])
            option_nineteen = tk.OptionMenu(branch, input_nineteen, *numbered_metro_list, command=select19)
            option_nineteen.config(width=20)
            input_nineteen.trace_add("write", scoot18)

            label_nineteen = tk.Label(branch, text='19')
            display_nineteen = tk.Label(branch, width=10, textvariable=ordertotal_nineteen)

            label_nineteen.grid(row=18, column=0, padx=5)
            option_nineteen.grid(row=18, column=1, padx=5)
            display_nineteen.grid(row=18, column=2,columnspan=2)

            ordertotal_twenty = tk.StringVar(branch)
            ordertotal_twenty.set('# of Orders')

            input_twenty = tk.StringVar(branch)
            input_twenty.set(numbered_metro_list[0])
            option_twenty = tk.OptionMenu(branch, input_twenty, *numbered_metro_list, command=select20)
            option_twenty.config(width=20)
            input_twenty.trace_add("write", scoot19)

            label_twenty = tk.Label(branch, text='20')
            display_twenty = tk.Label(branch, width=10, textvariable=ordertotal_twenty)

            label_twenty.grid(row=19, column=0, padx=5)
            option_twenty.grid(row=19, column=1, padx=5)
            display_twenty.grid(row=19, column=2,columnspan=2)

            ordertotal_twentyone = tk.StringVar(branch)
            ordertotal_twentyone.set('# of Orders')

            input_twentyone = tk.StringVar(branch)
            input_twentyone.set(numbered_metro_list[0])
            option_twentyone = tk.OptionMenu(branch, input_twentyone, *numbered_metro_list, command=select21)
            option_twentyone.config(width=20)
            input_twentyone.trace_add("write", scoot20)

            label_twentyone = tk.Label(branch, text='21')
            display_twentyone = tk.Label(branch, width=10, textvariable=ordertotal_twentyone)

            label_twentyone.grid(row=20, column=0, padx=5)
            option_twentyone.grid(row=20, column=1, padx=5)
            display_twentyone.grid(row=20, column=2,columnspan=2)

            ordertotal_twentytwo = tk.StringVar(branch)
            ordertotal_twentytwo.set('# of Orders')

            input_twentytwo = tk.StringVar(branch)
            input_twentytwo.set(numbered_metro_list[0])
            option_twentytwo = tk.OptionMenu(branch, input_twentytwo, *numbered_metro_list, command=select22)
            option_twentytwo.config(width=20)
            input_twentytwo.trace_add("write", scoot21)

            label_twentytwo = tk.Label(branch, text='22')
            display_twentytwo = tk.Label(branch, width=10, textvariable=ordertotal_twentytwo)

            label_twentytwo.grid(row=21, column=0, padx=5)
            option_twentytwo.grid(row=21, column=1, padx=5)
            display_twentytwo.grid(row=21, column=2,columnspan=2)

            ordertotal_twentythree = tk.StringVar(branch)
            ordertotal_twentythree.set('# of Orders')

            input_twentythree = tk.StringVar(branch)
            input_twentythree.set(numbered_metro_list[0])
            option_twentythree = tk.OptionMenu(branch, input_twentythree, *numbered_metro_list, command=select23)
            option_twentythree.config(width=20)
            input_twentythree.trace_add("write", scoot22)

            label_twentythree = tk.Label(branch, text='23')
            display_twentythree = tk.Label(branch, width=10, textvariable=ordertotal_twentythree)

            label_twentythree.grid(row=22, column=0, padx=5)
            option_twentythree.grid(row=22, column=1, padx=5)
            display_twentythree.grid(row=22, column=2,columnspan=2)

            ordertotal_twentyfour = tk.StringVar(branch)
            ordertotal_twentyfour.set('# of Orders')

            input_twentyfour = tk.StringVar(branch)
            input_twentyfour.set(numbered_metro_list[0])
            option_twentyfour = tk.OptionMenu(branch, input_twentyfour, *numbered_metro_list, command=select24)
            option_twentyfour.config(width=20)
            input_twentyfour.trace_add("write", scoot23)

            label_twentyfour = tk.Label(branch, text='24')
            display_twentyfour = tk.Label(branch, width=10, textvariable=ordertotal_twentyfour)

            label_twentyfour.grid(row=23, column=0, padx=5)
            option_twentyfour.grid(row=23, column=1, padx=5)
            display_twentyfour.grid(row=23, column=2,columnspan=2)

            ordertotal_twentyfive = tk.StringVar(branch)
            ordertotal_twentyfive.set('# of Orders')

            input_twentyfive = tk.StringVar(branch)
            input_twentyfive.set(numbered_metro_list[0])
            option_twentyfive = tk.OptionMenu(branch, input_twentyfive, *numbered_metro_list, command=select25)
            option_twentyfive.config(width=20)
            input_twentyfive.trace_add("write", scoot24)

            label_twentyfive = tk.Label(branch, text='25')
            display_twentyfive = tk.Label(branch, width=10, textvariable=ordertotal_twentyfive)

            label_twentyfive.grid(row=24, column=0, padx=5)
            option_twentyfive.grid(row=24, column=1, padx=5)
            display_twentyfive.grid(row=24, column=2,columnspan=2)

            ordertotal_twentysix = tk.StringVar(branch)
            ordertotal_twentysix.set('# of Orders')

            input_twentysix = tk.StringVar(branch)
            input_twentysix.set(numbered_metro_list[0])
            option_twentysix = tk.OptionMenu(branch, input_twentysix, *numbered_metro_list, command=select26)
            option_twentysix.config(width=20)
            input_twentysix.trace_add("write", scoot25)

            label_twentysix = tk.Label(branch, text='26')
            display_twentysix = tk.Label(branch, width=10, textvariable=ordertotal_twentysix)

            label_twentysix.grid(row=25, column=0, padx=5)
            option_twentysix.grid(row=25, column=1, padx=5)
            display_twentysix.grid(row=25, column=2,columnspan=2)

            ordertotal_twentyseven = tk.StringVar(branch)
            ordertotal_twentyseven.set('# of Orders')

            input_twentyseven = tk.StringVar(branch)
            input_twentyseven.set(numbered_metro_list[0])
            option_twentyseven = tk.OptionMenu(branch, input_twentyseven, *numbered_metro_list, command=select27)
            option_twentyseven.config(width=20)
            input_twentyseven.trace_add("write", scoot26)

            label_twentyseven = tk.Label(branch, text='27')
            display_twentyseven = tk.Label(branch, width=10, textvariable=ordertotal_twentyseven)

            label_twentyseven.grid(row=26, column=0, padx=5)
            option_twentyseven.grid(row=26, column=1, padx=5)
            display_twentyseven.grid(row=26, column=2,columnspan=2)

            ordertotal_twentyeight = tk.StringVar(branch)
            ordertotal_twentyeight.set('# of Orders')

            input_twentyeight = tk.StringVar(branch)
            input_twentyeight.set(numbered_metro_list[0])
            option_twentyeight = tk.OptionMenu(branch, input_twentyeight, *numbered_metro_list, command=select28)
            option_twentyeight.config(width=20)
            input_twentyeight.trace_add("write", scoot27)

            label_twentyeight = tk.Label(branch, text='28')
            display_twentyeight = tk.Label(branch, width=10, textvariable=ordertotal_twentyeight)

            label_twentyeight.grid(row=27, column=0, padx=5)
            option_twentyeight.grid(row=27, column=1, padx=5)
            display_twentyeight.grid(row=27, column=2,columnspan=2)

            ordertotal_twentynine = tk.StringVar(branch)
            ordertotal_twentynine.set('# of Orders')

            input_twentynine = tk.StringVar(branch)
            input_twentynine.set(numbered_metro_list[0])
            option_twentynine = tk.OptionMenu(branch, input_twentynine, *numbered_metro_list, command=select29p)
            option_twentynine.config(width=20)
            input_twentynine.trace_add("write", scoot28)

            label_twentynine = tk.Label(branch, text='29')
            display_twentynine = tk.Label(branch, width=10, textvariable=ordertotal_twentynine)

            label_twentynine.grid(row=28, column=0, padx=5)
            option_twentynine.grid(row=28, column=1, padx=5)
            display_twentynine.grid(row=28, column=2,columnspan=2)

            ordertotal_last = tk.StringVar(branch)
            ordertotal_last.set('# of Orders')

            input_last = tk.StringVar(branch)
            input_last.set(numbered_metro_list[-1])
            option_last = tk.OptionMenu(branch, input_last, *numbered_metro_list, command=selectlast)
            option_last.config(width=20)
            input_last.trace_add("write", scoot29p)

            label_last = tk.Label(branch, text='30')
            display_last = tk.Label(branch, width=10, textvariable=ordertotal_last)

            label_last.grid(row=29, column=0, padx=5)
            option_last.grid(row=29, column=1, padx=5)
            display_last.grid(row=29, column=2,columnspan=2)

            def finisher():
                global result

                result = tk.Tk()
                result.title('\U0001F44C Scooted \U0001F44C')

                previous_geometry = branch.winfo_geometry()
                previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
                saver()

                if re.search('360.+', previous_geometry):
                    result.geometry('352x507' + previous_location)
                else:
                    result.geometry(previous_geometry)

                generated_split = ('Distressed Orders: ' + str(sum(order_list[0:-1]) + (order_list[-1])) + '''
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
12. Metro: ''' +   metro_list[numbered_metro_list.index(input_twelve.get())] + ' / Orders: ' + ordertotal_twelve.get() + '''
13. Metro: ''' +   metro_list[numbered_metro_list.index(input_thirteen.get())] + ' / Orders: ' + ordertotal_thirteen.get() + '''
14. Metro: ''' +   metro_list[numbered_metro_list.index(input_fourteen.get())] + ' / Orders: ' + ordertotal_fourteen.get() + '''
15. Metro: ''' +   metro_list[numbered_metro_list.index(input_fifteen.get())] + ' / Orders: ' + ordertotal_fifteen.get() + '''
16. Metro: ''' +   metro_list[numbered_metro_list.index(input_sixteen.get())] + ' / Orders: ' + ordertotal_sixteen.get() + '''
17. Metro: ''' +   metro_list[numbered_metro_list.index(input_seventeen.get())] + ' / Orders: ' + ordertotal_seventeen.get() + '''
18. Metro: ''' +   metro_list[numbered_metro_list.index(input_eighteen.get())] + ' / Orders: ' + ordertotal_eighteen.get() + '''
19. Metro: ''' +   metro_list[numbered_metro_list.index(input_nineteen.get())] + ' / Orders: ' + ordertotal_nineteen.get() + '''
20. Metro: ''' +   metro_list[numbered_metro_list.index(input_twenty.get())] + ' / Orders: ' + ordertotal_twenty.get() + '''
21. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyone.get())] + ' / Orders: ' + ordertotal_twentyone.get() + '''
22. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentytwo.get())] + ' / Orders: ' + ordertotal_twentytwo.get() + '''
23. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentythree.get())] + ' / Orders: ' + ordertotal_twentythree.get() + '''
24. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfour.get())] + ' / Orders: ' + ordertotal_twentyfour.get() + '''
25. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyfive.get())] + ' / Orders: ' + ordertotal_twentyfive.get() + '''
26. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentysix.get())] + ' / Orders: ' + ordertotal_twentysix.get() + '''
27. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyseven.get())] + ' / Orders: ' + ordertotal_twentyseven.get() + '''
28. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentyeight.get())] + ' / Orders: ' + ordertotal_twentyeight.get() + '''
29. Metro: ''' +   metro_list[numbered_metro_list.index(input_twentynine.get())] + ' / Orders: ' + ordertotal_twentynine.get() + '''
30. Metro: ''' +   metro_list[numbered_metro_list.index(input_last.get())] + ' / Orders: ' + ordertotal_last.get() + '''
    ----------------------------------------''')

                display_result = tk.Text(result, width=50, height=36)
                display_result.insert(1.0, generated_split)
                display_result.grid(row=0, column=0)

                half_return_button = tk.Button(result, text='Back', command=return_2)
                half_return_button.grid(row=2, column=0, sticky='w')

                full_return_button = tk.Button(result, text='Home', command=return_1)
                full_return_button.grid(row=2, column=0)

                branch.destroy()
                helper.destroy()

            generate = tk.Button(branch, text='Generate', command=finisher)
            generate.grid(row=30, rowspan=2, column=2)

            reset_number_str = tk.StringVar(branch)
            reset_number_str.set('0')

            return_button = tk.Button(branch, text='Back', command=return_1)
            return_button.grid(row=30, column=1, sticky='w')

            def setter(event):
                global reset_number 

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_twentysix.set(split[25])
                input_twentyseven.set(split[26])
                input_twentyeight.set(split[27])
                input_twentynine.set(split[28])
                input_last.set(split[29])
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1]) + (order_list[-1])))

            reset_options = tk.OptionMenu(branch, reset_number_str, *mode_options, command=setter)
            reset_options.config(width=0)
            reset_options.grid(row=30, column=1, sticky='e')

            if return_check == 'Full':

                reset_number = float(reset_number_str.get())
                splitter()
                input_one.set(split[0])
                input_two.set(split[1])
                input_three.set(split[2])
                input_four.set(split[3])
                input_five.set(split[4])
                input_six.set(split[5])
                input_seven.set(split[6])
                input_eight.set(split[7])
                input_nine.set(split[8])
                input_ten.set(split[9])
                input_eleven.set(split[10])
                input_twelve.set(split[11])
                input_thirteen.set(split[12])
                input_fourteen.set(split[13])
                input_fifteen.set(split[14])
                input_sixteen.set(split[15])
                input_seventeen.set(split[16])
                input_eighteen.set(split[17])
                input_nineteen.set(split[18])
                input_twenty.set(split[19])
                input_twentyone.set(split[20])
                input_twentytwo.set(split[21])
                input_twentythree.set(split[22])
                input_twentyfour.set(split[23])
                input_twentyfive.set(split[24])
                input_twentysix.set(split[25])
                input_twentyseven.set(split[26])
                input_twentyeight.set(split[27])
                input_twentynine.set(split[28])
                input_last.set(split[29])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())]))) 
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))
                ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_twentyseven.get())])))
                ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_twentyeight.get())])))
                ordertotal_twentyeight.set(str(sum(order_list[numbered_metro_list.index(input_twentyeight.get()):numbered_metro_list.index(input_twentynine.get())])))
                ordertotal_twentynine.set(str(sum(order_list[numbered_metro_list.index(input_twentynine.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

            elif return_check == 'Half':

                input_one.set(saved_split[0])
                input_two.set(saved_split[1])
                input_three.set(saved_split[2])
                input_four.set(saved_split[3])
                input_five.set(saved_split[4])
                input_six.set(saved_split[5])
                input_seven.set(saved_split[6])
                input_eight.set(saved_split[7])
                input_nine.set(saved_split[8])
                input_ten.set(saved_split[9])
                input_eleven.set(saved_split[10])
                input_twelve.set(saved_split[11])
                input_thirteen.set(saved_split[12])
                input_fourteen.set(saved_split[13])
                input_fifteen.set(saved_split[14])
                input_sixteen.set(saved_split[15])
                input_seventeen.set(saved_split[16])
                input_eighteen.set(saved_split[17])
                input_nineteen.set(saved_split[18])
                input_twenty.set(saved_split[19])
                input_twentyone.set(saved_split[20])
                input_twentytwo.set(saved_split[21])
                input_twentythree.set(saved_split[22])
                input_twentyfour.set(saved_split[23])
                input_twentyfive.set(saved_split[24])
                input_twentysix.set(saved_split[25])
                input_twentyseven.set(saved_split[26])
                input_twentyeight.set(saved_split[27])
                input_last.set(saved_split[28])
                ordertotal_one.set(str(sum(order_list[numbered_metro_list.index(input_one.get()):numbered_metro_list.index(input_two.get())])))
                ordertotal_two.set(str(sum(order_list[numbered_metro_list.index(input_two.get()):numbered_metro_list.index(input_three.get())]))) 
                ordertotal_three.set(str(sum(order_list[numbered_metro_list.index(input_three.get()):numbered_metro_list.index(input_four.get())])))
                ordertotal_four.set(str(sum(order_list[numbered_metro_list.index(input_four.get()):numbered_metro_list.index(input_five.get())]))) 
                ordertotal_five.set(str(sum(order_list[numbered_metro_list.index(input_five.get()):numbered_metro_list.index(input_six.get())])))
                ordertotal_six.set(str(sum(order_list[numbered_metro_list.index(input_six.get()):numbered_metro_list.index(input_seven.get())])))
                ordertotal_seven.set(str(sum(order_list[numbered_metro_list.index(input_seven.get()):numbered_metro_list.index(input_eight.get())])))
                ordertotal_eight.set(str(sum(order_list[numbered_metro_list.index(input_eight.get()):numbered_metro_list.index(input_nine.get())])))
                ordertotal_nine.set(str(sum(order_list[numbered_metro_list.index(input_nine.get()):numbered_metro_list.index(input_ten.get())])))
                ordertotal_ten.set(str(sum(order_list[numbered_metro_list.index(input_ten.get()):numbered_metro_list.index(input_eleven.get())])))
                ordertotal_eleven.set(str(sum(order_list[numbered_metro_list.index(input_eleven.get()):numbered_metro_list.index(input_twelve.get())])))
                ordertotal_twelve.set(str(sum(order_list[numbered_metro_list.index(input_twelve.get()):numbered_metro_list.index(input_thirteen.get())])))
                ordertotal_thirteen.set(str(sum(order_list[numbered_metro_list.index(input_thirteen.get()):numbered_metro_list.index(input_fourteen.get())])))
                ordertotal_fourteen.set(str(sum(order_list[numbered_metro_list.index(input_fourteen.get()):numbered_metro_list.index(input_fifteen.get())])))
                ordertotal_fifteen.set(str(sum(order_list[numbered_metro_list.index(input_fifteen.get()):numbered_metro_list.index(input_sixteen.get())])))
                ordertotal_sixteen.set(str(sum(order_list[numbered_metro_list.index(input_sixteen.get()):numbered_metro_list.index(input_seventeen.get())])))
                ordertotal_seventeen.set(str(sum(order_list[numbered_metro_list.index(input_seventeen.get()):numbered_metro_list.index(input_eighteen.get())])))
                ordertotal_eighteen.set(str(sum(order_list[numbered_metro_list.index(input_eighteen.get()):numbered_metro_list.index(input_nineteen.get())])))
                ordertotal_nineteen.set(str(sum(order_list[numbered_metro_list.index(input_nineteen.get()):numbered_metro_list.index(input_twenty.get())])))
                ordertotal_twenty.set(str(sum(order_list[numbered_metro_list.index(input_twenty.get()):numbered_metro_list.index(input_twentyone.get())])))
                ordertotal_twentyone.set(str(sum(order_list[numbered_metro_list.index(input_twentyone.get()):numbered_metro_list.index(input_twentytwo.get())]))) 
                ordertotal_twentytwo.set(str(sum(order_list[numbered_metro_list.index(input_twentytwo.get()):numbered_metro_list.index(input_twentythree.get())]))) 
                ordertotal_twentythree.set(str(sum(order_list[numbered_metro_list.index(input_twentythree.get()):numbered_metro_list.index(input_twentyfour.get())])))
                ordertotal_twentyfour.set(str(sum(order_list[numbered_metro_list.index(input_twentyfour.get()):numbered_metro_list.index(input_twentyfive.get())])))  
                ordertotal_twentyfive.set(str(sum(order_list[numbered_metro_list.index(input_twentyfive.get()):numbered_metro_list.index(input_twentysix.get())])))
                ordertotal_twentysix.set(str(sum(order_list[numbered_metro_list.index(input_twentysix.get()):numbered_metro_list.index(input_twentyseven.get())])))
                ordertotal_twentyseven.set(str(sum(order_list[numbered_metro_list.index(input_twentyseven.get()):numbered_metro_list.index(input_twentyeight.get())])))
                ordertotal_twentyeight.set(str(sum(order_list[numbered_metro_list.index(input_twentyeight.get()):numbered_metro_list.index(input_twentynine.get())])))
                ordertotal_twentynine.set(str(sum(order_list[numbered_metro_list.index(input_twentynine.get()):numbered_metro_list.index(input_last.get())])))    
                ordertotal_last.set(str(sum(order_list[numbered_metro_list.index(input_last.get()):-1])+ (order_list[-1])))

        if return_check == 'Half':

            if branch.winfo_screenwidth() - (previous_x + 352 + 395) < 255:
                    helper.geometry('255x330' + helper_location_inverted)

            elif branch.winfo_screenwidth() - (previous_x + 352 + 395) > 255:
                x = branch.winfo_screenwidth() - (branch.winfo_x() + 352 + 395)
                print(x)
                helper.geometry('255x330' + helper_location)

            helper.title('\U0001F916 Handlebars \U0001F916')
            helperdisplay = tk.Text(helper)

            for values in helpertext:
                helperdisplay.insert(tk.END, values + '\n')

            helperdisplay.config(state='disabled')
            helperdisplay.pack()

        try:
            root.winfo_exists()

            if root.winfo_exists():
                root.destroy()

        except: 
            return_check = 'Half'

    global firstchoice    
    firstchoice = ttk.Combobox(root, value=listofoptions, width=10)

    if return_number == 0:
        firstchoice.set('''# of Logi's''')

    else:
        firstchoice.set(numberoflogis_str)

    initialize = tk.Button(root, text='Initialize', command=logi_numerizer, state='normal')

    data_input.grid(row=0, column=0, columnspan=3, pady=5)
    firstchoice.grid(row=1, column=0)
    initialize.grid(row=1, column=2)


def return_1():
    global return_number
    global return_check
    global previous_location

    try:
        branch.winfo_exists()

        if branch.winfo_exists():
            previous_location = '+' + str(branch.winfo_x()) + '+' + str(branch.winfo_y())
            branch.destroy()
            helper.destroy()

    except:
        print('Return to Home from Result screen')
    
    try:
        result.winfo_exists()

        if result.winfo_exists():
            previous_location = '+' + str(result.winfo_x()) + '+' + str(result.winfo_y())
            result.destroy()

    except:
        print('Return to Home from Numerizer screen')

    
    
    return_number += 1
    return_check = 'Full'

    home_screen()

def return_2():
    global return_number
    global return_check
    global previous_location
    global helper_location
    global helper_location_inverted
    global previous_x

    previous_x = int(result.winfo_x())
    previous_location = '+' + str(result.winfo_x()) + '+' + str(result.winfo_y())

    helper_location = '+' + str(result.winfo_x() + 352 + 73) + '+' + str(result.winfo_y() + 100)
    helper_location_inverted = '+' + str(result.winfo_x() - 425) + '+' + str(result.winfo_y() + 100)
    print('Helper Location Inverted:' + helper_location_inverted)
    print(result.winfo_x)

    result.destroy()

    print(previous_input)

    return_number += 1
    return_check = 'Half'

    logi_numerizer()

home_screen()

root.mainloop()