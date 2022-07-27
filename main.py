import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_Learn = {}

# Language FLASH CARD program
# UDEMY 100 days of PYTHON 2022 course
# David King July 22-27, 2022


#  setup data file for training.  "to_learn" .
try:  # try to open the data file for use.
    data = pandas.read_csv("data/words_to_learn.csv")
    # data is now a pandas dataframe
except FileNotFoundError:  # the try failed, file not there. Use default language file.
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
    #  to_learn is now a python List of Dictionaries
else:  # the try worked , the file exists, convert to disc for use.
    to_learn = data.to_dict(orient="records")
    #  to_learn is now a python List of Dictionaries


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)  # cancel timer if running
    current_card = random.choice(to_learn)  # get a random card from the list, set variables appropriately (pointer in
    # dct)
    canvas.itemconfig(card_title, text="French", fill="black")  # set Language on screen
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")  # set French word on screen
    canvas.itemconfig(card_background, image=card_front_img)  # set the background image on screen
    flip_timer = window.after(3000, func=flip_card)  # setup new timer for this click


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")  # set Language title on screen
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")  # set lang word on screen
    canvas.itemconfig(card_background, image=card_back_img)  # set the background image on screen


def is_known():
    to_learn.remove(current_card)  # if check button clicked, card is known, remove word from dict.
    #  word is now removed from the "current" file of words to learn.
    #  now we have to REMAKE the list of words to learn.
    data = pandas.DataFrame(to_learn)  # convert smaller (word removed) Python List to pandas dataframe
    data.to_csv("data/words_to_learn.csv", index=False)  # convert# convert dataframe back to csv format file and save.
    #  index=False removes the line number from each line of the data file output.
    #  1 french, english becomes french,english
    next_card()  # select a new random word from the dict.


# create program window

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=526, highlightthickness=0)

#  After window creation, wait 3 sec then do flip_card
flip_timer = window.after(3000, func=flip_card)

#  create canvas window


card_front_img = PhotoImage(file="images/card_front.png")  # convert the png to Tkinter format
# the 400 and 263 are X and Y positions on the canvas
card_background = canvas.create_image(400, 263,
                                      image=card_front_img)  # put the image on the canvas at the x y given / CENTER or 1/2
card_back_img = PhotoImage(file="images/card_back.png")  # convert the png to Tkinter format
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))  # Create 'title' holder for canvas
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))  # Create 'word' holder for canvas
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)  # set background color of CANVAS image, remove borderline
canvas.grid(row=0, column=0, columnspan=2)  # position of canvas in Grid

# create and place buttons

cross_image = PhotoImage(file="images/wrong.png")  # convert the png to Tkinter format
unknown_button = Button(image=cross_image, highlightthickness=0,
                        command=next_card)  # create the button with the image on it
unknown_button.grid(row=1, column=0)  # Place the button in the grid

check_image = PhotoImage(file="images/right.png")  # convert the png to Tkinter format
known_button = Button(image=check_image, highlightthickness=0,
                      command=is_known)  # create the button with the image on it
known_button.grid(row=1, column=1)  # Place the button in the grid

next_card()  # update screen with Title and first word

window.mainloop()  # keep window open
