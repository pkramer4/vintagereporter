# Developed by: Preston Kramer
# 7/10/20
# database sorter to find

from tkinter import *
from PIL import Image

import os

# initialize stlye variables to be used throughout project
salmon = '#ff83a1'
home_bg = 'black'
home_fg = 'white'


def session():
    """constructs tkinter gui session"""

    #### sets up application frame, both size and title ####
    screen8 = Toplevel(screen)
    screen8.title('Welcome to the vintage report')
    screen8.geometry('550x520')
    screen8.minsize(width=500, height=450)
    screen8.maxsize(width=800, height=590)

    # sets background image
    imglabel = Label(screen8, image = photo1, width = '600', height = '400')
    imglabel.place(x=0, y=0, relwidth=1, relheight=1)

    # adds title text to root
    title_label = Label(screen8, width = '600', height = '2', text='The Vintage reporter', font = ('calibri', 17), bg = home_bg, fg = home_fg)
    title_label.pack(pady = (0,30))

    #text asking for country/state, puts in input box for answer
    country_label = Label(screen8, bg = home_bg, fg = home_fg, text='Enter your wine\'s country of origin', font = ('calibri', 15))
    country_label.config(width = '30')
    country_label.pack()

    # options for drop down menu
    options_country = ['california', 'oregon']

    clicked_country = StringVar(screen8)
    clicked_country.set('  Pick a country or state  ')
    drop_country = OptionMenu(screen8, clicked_country, *options_country)
    drop_country.config(width=22)
    drop_country.pack(pady = (5,20))



    #text asking for region, puts in input box for answer
    region_label = Label(screen8, width = '30',  bg = home_bg, fg = home_fg, text='Enter your wine\'s region', font = ('calibri', 15))
    region_label.pack()

    # options for drop down menu
    options_region = ['napa', 'willamette valley']

    clicked_region = StringVar(screen8)
    clicked_region.set('        Pick a region        ')
    drop_region = OptionMenu(screen8,  clicked_region, *options_region)#don't forget asterisk
    drop_region.config(width=22)
    drop_region.pack(pady = (5,20))



### This implementation is not yet hashed out ###
#     #text asking for subregion, put in input box for answer
#     subregion_label = Label(screen8, text='Enter your wine\'s sub region (type "none" if none listed)').pack()
#     options_subregion = ['california', 'oregon']
#     clicked_subregion = StringVar(screen8)
#     clicked_subregion.set('Pick a country or state')
#     drop_subregion = OptionMenu(screen8, clicked_subregion, *options_subregion)#don't forget asterisk
#     drop_subregion.pack()


    #text asking for variety, put in input box for answer
    variety_label = Label(screen8,width = 30,fg = home_fg,  bg = home_bg, text='Enter your wine\'s variety or color', font = ('calibri', 15))
    variety_label.pack()

    # options for drop down menu region
    options_variety = ['chardonnay', 'pinot noir', 'cabernet sauvignon']

    clicked_variety = StringVar(screen8)
    clicked_variety.set('       Pick a Variety        ')
    drop_variety = OptionMenu(screen8, clicked_variety, *options_variety)#don't forget asterisk
    drop_variety.config(width=22)
    drop_variety.pack(pady = (5,20))



    #text asking for year, put in input box for answer
    year_label = Label(screen8, width = '30',fg = home_fg,  bg = home_bg, text='Enter your wine\'s vintage', font = ('calibri', 15))
    year_label.pack()

    # these are the only years in db so far
    options_year = ['1995', '1997','1998','1999','2000',
                    '2001','2002','2003','2004','2005',
                   '2006','2007','2008','2009','2010',
                   '2011','2012','2013','2014','2015','2016']

    clicked_year = StringVar(screen8)
    clicked_year.set('         Pick a year         ')
    drop_year = OptionMenu(screen8, clicked_year, *options_year)#don't forget asterisk
    drop_year.config(width=22)
    drop_year.pack(pady = (5,20))

    def parse():
        """
        reads database csv into pandas dataframe,
        then finds a wine from given selecitons from drop down menus
        """

        global testlabel
        global testlabel2
        global refresh_button

        import pandas as pd
        vintagechart = 'vintages-4.csv'
        df = pd.read_csv(vintagechart)

        # Removes extra columns from dataframe
        df = df[['Country/State', 'Region', 'Sub Region', 'Variety or color', 'Vintage','Score', 'Ideal years']]

        # Changes vintages row to strings
        df["Vintage"] = df["Vintage"].astype(str)

        # gets options from home drop down menus
        state = clicked_country.get()
        region = clicked_region.get()
        #subregion = clicked_subregion.get()
        variety = clicked_variety.get()
        year = clicked_year.get()



        #reduces options for correct wine by Country/State
        df2=df[df['Country/State']==state]

        # further reduces options for correct wine by Region
        df3=df2[df2['Region']==region]

    #     #Pulls further by sub Region
    #    df4=df3[df3['Sub Region']==subregion]

        # further reduces options for correct wine by Region
        df4=df3[df3['Variety or color']==variety]

        #Saves index of the answer row as an int to be used later
        index = df4[df4['Vintage']==year].index.tolist()

        if index == []:
            status = 'This wine is not in our databases'

            #creates enter another wine button
            testlabel2 = Label(screen8, text = status, width = '500',bg = home_bg, fg = home_fg)
            testlabel2.pack(pady = (5,10))
            refresh_button = Button(screen8, text = 'Enter another wine', height = '2', command = again)
            refresh_button.pack()
        else:
            index = index[0]

            df5=df4[df4['Vintage']==year]

            df6 = df5.to_dict()

            #Pulls score from secondary index dictionary
            df7 = df6['Score']
            score = df7[index]

            #Pulls ideal drinking years from dictionary
            df8 = df6['Ideal years']
            df9 = df8[index]

            #makes years range into int, spearates, and stores each as values
            list1 = df9.split(':')
            for i in range(0, len(list1)):
                list1[i] = int(list1[i])
            listearly=list1[0]
            listlate=list1[1]


            # provides status of wine based on wine vintage and ideal years
            if int(year) >= listearly and int(year) <=listlate:
                status = 'Your wine is ready to drink!'
            elif int(year) <= listlate:
                status = 'your wine might be a little old\nthe ideal drinking years: ' + str(listearly)+'-'+str(listlate)
            else:
                status = 'your wine is still too young\nthe ideal drinking years: ' + str(listearly)+'-'+str(listlate)


            # display score to screen
            try:
                testlabel = Label(screen8, text = 'this vintage has a score of '+ str(score), width = '500', bg = home_bg, fg = home_fg)
                testlabel.pack()
            except:
                pass

            testlabel2 = Label(screen8, text = status, width = '500', bg = home_bg, fg = home_fg)
            testlabel2.pack()
            refresh_button = Button(screen8, text = 'Enter another wine', command = again)
            refresh_button.pack()


    Button(screen8, text = 'Is your wine ready to drink?', height = '2', width = '30', command = parse).pack()


def again():
    """function called when entering another wine to remove screen elements"""
    global testlabel
    global testlabel2
    global refresh_button
    testlabel.pack_forget()
    refresh_button.pack_forget()
    testlabel2.pack_forget()

# registration protocol
def register_user():
    """
    Adds user to registered user database
    returns error message if passwords do not match
    """
    password_check1 = password.get()
    password_check2 = password2.get()

    if password_check1 == password_check2:

        username_info = username.get()
        password_info = password.get()

        file = open(username_info, 'w')
        file.write(username_info + '\n')
        file.write(password_info)
        file.close()


        Label(screen1, text = 'Registration successful', fg = 'green', font = ('calibri', 11)).pack()

    else:
        Label(screen1, text = 'Passwords do not match, try again', fg = 'red', font = ('calibri', 11)).pack()

    username_entry.delete(0, END)
    password_entry.delete(0, END)
    password_entry2.delete(0, END)



def register():
    """
    creates user registration window,
    contains username entry field and two password entry fields
    """

    global screen1
    screen1 = Toplevel(screen)
    screen1.title('Register')
    screen1.geometry('300x300')

    global username_entry
    global password_entry
    global username
    global password
    global password2
    global password_entry2
    username = StringVar()
    password = StringVar()
    password2 = StringVar()

    Label(screen1, text = 'Please enter information below').pack()
    Label(screen1, text = 'Username *').pack()

    username_entry = Entry(screen1, textvariable = username)
    username_entry.pack()
    Label(screen1, text = '').pack()   # blank line

    Label(screen1, text = 'Password *').pack()
    password_entry = Entry(screen1, show = '*', textvariable = password)
    password_entry.pack()
    Label(screen1, text = '').pack() # blank line

    Label(screen1, text = 'Confirm password *').pack()
    password_entry2 = Entry(screen1, show = '*', textvariable = password2)
    password_entry2.pack()
    Label(screen1, text = '').pack() # blank line

    Button(screen1, text = 'Register', width = '10', height = '2', command = register_user).pack()

def delete2():
    """destroy password not recognized window on successful login"""
    screen3.destroy()

def login_success():
    """destroy login window on successful login, begin search session"""

    screen2.destroy()
    session()


def password_not_recognized():
    """creates window to display incorrect password message"""
    global screen3
    screen3 = Toplevel(screen)
    screen3.title('Incorrect password')
    screen3.geometry('150x100')

    Label(screen3, text = 'Incorrect password').pack()
    Button(screen3, text = 'OK', command = delete2).pack()

def user_not_found():
    """creates window to display user not found message"""
    global screen3
    screen3 = Toplevel(screen)
    screen3.title('success')
    screen3.geometry('150x100')

    Label(screen3, text = 'Username not found').pack()
    Button(screen3, text = 'OK', command = delete2).pack()


def login_verify():
    """verifies login info is correct for a registered user"""
    username1 = username_verify.get()
    password1 = password_verify.get()

    # clear text boxes in login page
    username_entry1.delete(0, END)
    password_entry1.delete(0, END)

    # gets filenames in current directory (corresponds to username)
    list_of_files = os.listdir()

    if username1 in list_of_files:
        file1 = open(username1, 'r')
        verify = file1.read().splitlines()

        if password1 in verify:
            login_success()

        else:
            password_not_recognized()

    else:
        user_not_found()



def login():
    """creates login window with username and password fields"""

    global screen2
    screen2 = Toplevel(screen)
#     screen2.title('Login')
#     screen2.geometry('300x250')
    global username_verify
    global password_verify
    global username_entry1
    global password_entry1

    username_verify = StringVar()
    password_verify = StringVar()

    Label(screen2, text = 'Please enter information below', bg = home_bg, height = '2', fg = home_fg).pack(fill = BOTH, expand = True)

    # create username field and label
    Label(screen2, text = 'Username *').pack(pady = (10,0))
    username_entry1 = Entry(screen2, textvariable = username_verify)
    username_entry1.pack()
    Label(screen2, text = '').pack()

    # create password field and label
    Label(screen2, text = 'Password *').pack()
    password_entry1 = Entry(screen2, show = '*', textvariable = password_verify)
    password_entry1.pack()
    Label(screen2, text = '').pack()

    Button(screen2, text= 'login', width = '10', height = '2', command = login_verify).pack()

def instructions():
    """create instructions label to pop up on home window if query button pushed"""
    ins = Label(screen, font = ('cambria', 14), bg = home_bg, fg = home_fg, text = "Finding how good your wine bottle will be is simple.\n Login, then enter the details on your wine's label. \nThe tracker will give you the score for that vintage and the ideal years to drink it", width = '500')
    ins.pack(side=BOTTOM)

def main_screen():
    """creates home window"""

    global screen
    screen = Tk()
    screen.geometry('600x400')
    screen.title('T h e  V i n t a g e  R e p o r t')
    screen.aspect(3,2,3,2)
    screen.minsize(width=600, height=400)
    screen.maxsize(width=800, height=533)

    # load background image
    global photo1
    photo1 = PhotoImage(file = 'images/grapes2.png')
    imglabel = Label(screen, image = photo1, width = '600', height = '400')
    imglabel.place(x=0, y=0, relwidth=1, relheight=1)

    Label(text = 'T h e    V i n t a g e    R e p o r t', width = '375', height = '2', font = ('calibri', 23), bg = 'black', fg = 'white').pack()

    Label(text = 'Welcome to the vintage report\na database that can help you pick the best wine vintages', width = '375', fg = 'white', bg = 'black', font = ('calibri', 18)).pack()
    Button(text = "Log in", height = '2', width = '30', command = login).pack(pady = '20')

    Button(text = 'Sign up', height = '2', width = '30', command = register).pack(pady = '20')

    Button(text = 'How does it work?', height = '2', width = '30', command = instructions).pack(pady = '20')

    screen.mainloop()

main_screen()
