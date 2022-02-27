from tkinter import *
from PIL import ImageTk, Image
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import font
from data import *

root = Tk()
root.iconbitmap('Img/Logo2.ico')
root.title('Ticket Machine Pythonland')
root.configure(bg='#d4e783')
root.geometry('500x910')
root.resizable(False, False)

# Labels for layout (application title, Phytonland logo, snake image)
title_text = ImageTk.PhotoImage(Image.open('Img/Titel.jpg'))
app_title = Label(image=title_text, borderwidth=0)
app_title.place(x=10, y=20)

logo_pythonland = ImageTk.PhotoImage(Image.open('Img/Logo.jpg'))
app_logo = Label(image=logo_pythonland, borderwidth=0)
app_logo.place(x=360, y=-20)

img_snake = ImageTk.PhotoImage(Image.open('Img/Snake.jpg'))
app_image = Label(image=img_snake, borderwidth=0)
app_image.place(x=300, y=370)

# Lists for total visitors and total price 
visitors = []
price = []

# Labels for description age groups visitors + age limits
description_toddler = Label(root, text='- KLeine kinderen jonger dan ' + 
                            str(LIMIT_TODDLER) + ' jaar:', 
                            font='Consolas 10 italic', bg='#d4e783')
description_child = Label(root, text='- Kinderen vanaf ' + str(LIMIT_TODDLER) + 
                          ' jaar t/m ' + str(LIMIT_CHILD) + ' jaar:', 
                          font='Consolas 10 italic', bg='#d4e783')
description_adult = Label(root, text='- Volwassenen vanaf ' +  str(LIMIT_CHILD) +
                          ' t/m ' + str(LIMIT_ADULT) + ' jaar:', 
                          font='Consolas 10 italic', bg='#d4e783')
description_senior = Label(root, text='- Senioren vanaf ' + str(LIMIT_ADULT) + 
                           ' jaar en ouder:', font='Consolas 10 italic', 
                           bg='#d4e783')
description_discount = Label(root, text='- Korting voor elke ' + 
                             str(LIMIT_DISCOUNT) +'e betalende bezoeker',
                             font='Consolas 10 italic bold', bg='#d4e783')

# Labels for entrance fees visitor age groups
entrance_toddler = Label(root, text='\N{euro sign} '+
                         "{:.2f}".format(PRICE_TODDLER).replace(".", ","),
                         font='Consolas 10 bold', bg='#d4e783')
entrance_child = Label(root, text='\N{euro sign} '+
                       "{:.2f}".format(PRICE_CHILD).replace(".", ","),
                       font='Consolas 10 bold', bg='#d4e783')
entrance_adult = Label(root, text='\N{euro sign} '+
                       "{:.2f}".format(PRICE_ADULT).replace(".", ","),
                       font='Consolas 10 bold', bg='#d4e783')
entrance_senior = Label(root, text='\N{euro sign} '+
                        "{:.2f}".format(PRICE_SENIOR).replace(".", ","),
                        font='Consolas 10 bold', bg='#d4e783')
entrance_discount = Label(root, text='\N{euro sign} '+
                          "{:.2f}".format(PRICE_DISCOUNT).replace(".", ","),
                          font='Consolas 10 bold', bg='#d4e783')

description_toddler.place(x=10, y=110)
description_child.place(x=10, y=140)
description_adult.place(x=10, y=170)
description_senior.place(x=10, y=200)
description_discount.place(x=10, y=240)

entrance_toddler.place(x=400, y=110)
entrance_child.place(x=400, y=140)
entrance_adult.place(x=400, y=170)
entrance_senior.place(x=400, y=200)
entrance_discount.place(x=400, y=240)

# Create listbox for showing list of entered visitors
visitors_list = Listbox(root, font="Consolas 8", width=25, height=25)
visitors_list.place(x=10, y=350)

# Create listbox to display list entered prices
prices_list = Listbox(root, font="Consolas 8", width=15, height=25)
prices_list.place(x=180, y=350)

# Labels for totals at bottom digital receipt
entrance_total = Listbox(root, font="Verdana 12", fg="red4", width=8, 
                         height=1)
entrance_total.place(x=10, y=760)

discount_total = Listbox(root, font="Verdana 12", fg="green4", width=8, 
                        height=1)
discount_total.place(x=10, y=790)

price_total = Listbox(root, font="Verdana 16", width=8, height=1)
price_total.place(x=10, y=820)

###############################################################################

# Function to start application + input number of visitors

def start_tickets():

    global number
    number = simpledialog.askstring("Aantal bezoekers", "Uit hoeveel " + 
                                    "bezoekers bestaat de groep?")

    if number == None:
        root.mainloop

    else:

        try:
            int(number)

            number = int(number)

            if number == 0:
                start_tickets()

            elif number > 25 and number <= 999:
                messagebox.showerror("Aantal bezoeker",
                                    "In verband met het Coronavirus vragen "  
                                    "wij u voor groepen groter dan 25 personen " 
                                    "eerst telefonisch contact met ons op te nemen")

            elif number > 999:
                root.quit()

            else:
                cover_age.lower()
                button_tickets.lower()

                button_recover.config(state=NORMAL)

                input_age.focus()

        except ValueError :
                start_tickets()

# Calculation total entry fee without discounts

def calculate_entrance():

    global entrance
    entrance = sum(price)

    entrance_total.delete(0, END)
    entrance_total.insert(END, "\N{euro sign} {:.2f}".format(entrance))

# Calculation total discount

# Discount is over every paid visiter. So if a toddler is free then this should 
# be excluded from the calculation

def calculate_discount():

    if PRICE_TODDLER == 0.00:
        x = visitors.count("klein kind")

    else:
        x = 0

    global discount
    discount = ((len(visitors) - x) // 5) * PRICE_DISCOUNT

    discount_total.delete(0, END)
    discount_total.insert(END, "\N{euro sign}-{:.2f}".format(discount))

# # Calculation total discount

def calculate_price():

    global total
    total = entrance - discount

    price_total.delete(0, END)
    price_total.insert(END, "\N{euro sign} {:.2f}".format(total))

# Function to enter age + add visitor age group and visitor price to both lists
# + show all entries on the digital receipt 

def enter_age():

    age = input_age.get()

    try:

        age = int(age)

        if age < LIMIT_TODDLER:
            visitors.append("klein kind")
            price.append(PRICE_TODDLER)


        elif age >= LIMIT_TODDLER and age < LIMIT_CHILD:
            visitors.append("kind")
            price.append(PRICE_CHILD)


        elif age >= LIMIT_CHILD and age <= LIMIT_ADULT:
            visitors.append("volwassene")
            price.append(PRICE_ADULT)


        else:
            visitors.append("senior")
            price.append(PRICE_SENIOR)


        visitors_list.delete(0, END)
        for x in visitors:
            visitors_list.insert(END, x + '\n')

        prices_list.delete(0, END)
        for x in price:
            prices_list.insert(END, '\N{euro sign} ' "{:.2f}".format(x) + '\n')


        input_age.delete(0, END)
        calculate_entrance()
        calculate_discount()
        calculate_price()

        if (len(visitors)) >= number:
            cover_age.lower()
            button_tickets.lower()
            input_age.config(state=DISABLED)
            button_age.lower()
            button_restart.lower()

    except ValueError: input_age.delete(0, END)

#  Function for possible recovery of incorrect last entered age of visitor 

def recover_age():

    if len(visitors) > 0:

        visitors.pop()
        price.pop()

        visitors_list.delete(0, END)
        for x in visitors:
            visitors_list.insert(END, x + '\n')

        prices_list.delete(0, END)
        for x in price:
            prices_list.insert(END, '\N{euro sign} ' "{:.2f}".format(x) + '\n')

        input_age.config(state=NORMAL)
        cover_age.lower()
        button_tickets.lower()
        button_sort_out.lower()
        button_restart.lower()
        button_confirm.lower()

        calculate_entrance()
        calculate_discount()
        calculate_price()

    else:
        pass

# Function to calculate + format + show all totals on the digital receipt

def sort_out():

    visitors_list.delete(0, END)
    prices_list.delete(0, END)

    visitors_list.config(font="Consolas 9", width=21, height=21)
    prices_list.config(font="Consolas 9 bold", width=13, height=21)

    toddler_number = visitors.count("klein kind")
    toddler_total = (price.count(PRICE_TODDLER)) * PRICE_TODDLER

    visitors_list.insert(END, "Totaal klein kind " + str(toddler_number) + 
                         '\n')
    prices_list.insert(END, '\N{euro sign}  ' "{:.2f}".format(toddler_total) 
                       + '\n')

    child_number = visitors.count("kind")
    child_total = (price.count(PRICE_CHILD)) * PRICE_CHILD

    visitors_list.insert(END, "Totaal kind       " + str(child_number) + '\n')
    prices_list.insert(END, '\N{euro sign}  ' "{:.2f}".format(child_total) + 
                       '\n')

    adult_number = visitors.count("volwassene")
    adult_total = (price.count(PRICE_ADULT)) * PRICE_ADULT

    visitors_list.insert(END, "Totaal volwassene " + str(adult_number) + '\n')
    prices_list.insert(END, '\N{euro sign}  ' "{:.2f}".format(adult_total) + 
                       '\n')

    senior_number = visitors.count("senior")
    senior_total = (price.count(PRICE_SENIOR)) * PRICE_SENIOR

    visitors_list.insert(END, "Totaal senior     " + str(senior_number) + '\n')
    prices_list.insert(END, '\N{euro sign}  ' "{:.2f}".format(senior_total) + '\n')

    visitors_list.insert(END, '' + '\n')
    prices_list.insert(END, '' + '\n')

    visitors_list.insert(END, "Totaal entree" + '\n')
    prices_list.insert(END, '\N{euro sign}  {:.2f}'.format(entrance))

    visitors_list.insert(END, "Totaal korting" + '\n')
    prices_list.insert(END, '\N{euro sign} -{:.2f}'.format(discount))

    visitors_list.insert(END, '' + '\n')
    prices_list.insert(END, '' + '\n')

    visitors_list.insert(END, "Totaal prijs" + '\n')
    prices_list.insert(END, '\N{euro sign}  {:.2f}'.format(total))

    button_recover.config(state=DISABLED)

    cover_age.lower()
    button_tickets.lower()
    button_age.lower()
    button_recover.lower()
    button_sort_out.lower()
    cover_confirm.lower()

# Function to delete all entries and restart program in case of any mistake made
# by user

def restart():

    visitors.clear()
    price.clear()

    visitors_list.delete(0, END)
    prices_list.delete(0, END)

    entrance_total.delete(0, END)
    discount_total.delete(0, END)
    price_total.delete(0, END)

    cover_age.lower()
    age_visitors.lower()
    input_age.lower()

    button_age.lower()
    button_sort_out.lower()
    button_restart.lower()
    button_confirm.lower()

    input_age.config(state=NORMAL)

    visitors_list.config(font="Consolas 8", width=25, height=25)
    prices_list.config(font="Consolas 8", width=15, height=25)

    start_tickets()

# Function to confirm the entry and ordering the tickets

def confirm():

    visitors.clear()
    price.clear()

    visitors_list.delete(0, END)
    prices_list.delete(0, END)

    entrance_total.delete(0, END)
    discount_total.delete(0, END)
    price_total.delete(0, END)

    cover_age.lower()
    age_visitors.lower()
    input_age.lower()

    button_age.lower()
    button_sort_out.lower()
    button_restart.lower()
    button_confirm.lower()

    input_age.config(state=NORMAL)
    button_recover.config(state=DISABLED)

    visitors_list.config(font="Consolas 8", width=25, height=25)
    prices_list.config(font="Consolas 8", width=15, height=25)

###############################################################################

# Images with text for buttons
button_text_1 = ImageTk.PhotoImage(Image.open('Img/Foto1.jpg'))
button_text_2 = ImageTk.PhotoImage(Image.open('Img/Foto2.jpg'))
button_text_3 = ImageTk.PhotoImage(Image.open('Img/Foto3.jpg'))
button_text_4 = ImageTk.PhotoImage(Image.open('Img/Foto4.jpg'))
button_text_5 = ImageTk.PhotoImage(Image.open('Img/Foto5.jpg'))
button_text_6 = ImageTk.PhotoImage(Image.open('Img/Foto6.jpg'))
button_text_7 = ImageTk.PhotoImage(Image.open('Img/Foto7.jpg'))

# Label to ask age visitors
age_visitors = Label(image=button_text_2, borderwidth=0)
age_visitors.place(x=10, y=290)

# Input for age visitors
input_age = Entry(root, width=3, font='Consolas 14', justify='center')
input_age.place (x=305, y=290)

# Buttons
button_restart = Button(root, image = button_text_5, bg='#4caf50', 
                        relief=RAISED, bd=6, command=restart)
button_restart.place(x=360, y=281)

button_sort_out = Button(root, image = button_text_4, bg='#4caf50', 
                        relief=RAISED, bd=6, command=sort_out)
button_sort_out.place(x=360, y=281)

button_age = Button(root, image = button_text_3, bg='#4caf50', 
                         relief=RAISED, bd=6, command=enter_age)
button_age.place(x=360, y=281)

button_confirm = Button(root, image= button_text_7, bg='#9ddc38', 
                       relief=RAISED, bd=8, command=confirm)
button_confirm.place(x=160, y=815)

button_recover = Button(root, image = button_text_6, bg='#4caf50', 
                        relief=RAISED, bd=6, state=DISABLED, command=recover_age)
button_recover.place(x=160, y=760)

# Covers to hide buttons when they are not needed 
cover_age = Label(root, text='                                                                                 '
                             , font='Verdana 40 bold', bg='#d4e783')
cover_age.place(x=10, y=270)

cover_confirm = Label(root, text='                                                                                 '
                             , font='Verdana 50 bold', bg='#d4e783')
cover_confirm.place(x=160, y=815)

# Button to start app
button_tickets = Button(root, image = button_text_1, bg='#9ddc38', 
                        relief=RAISED, bd=6, command=start_tickets)
button_tickets.place(x=135, y=272)

root.mainloop()