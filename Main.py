# -*- coding: utf-8 -*-
"""
Program that takes a CSV file chosen by the user of the 500 most valuable 
brands and identifies the prominent colour within their logo and 
summarises trends found.
Created on Fri May  2 11:13:25 2021
Author: Jonathan Coachman
"""

import csv
import matplotlib.pyplot as plt
from PIL import Image
from colour import rgb2hsl


def import_csv(filename):
    """Function that imports a CSV file and returns data as a list
    """
    
    with open("Data/"+filename, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
        
    return(data)


def processing_raw_data(data):
    """Procedure for processing data and returns a list of the brands in the
       order according to their rank.
    """
    
    data_without_header = data[1:]
    clean_data = []
    i = 0
    for single_data in data_without_header:
        clean_data.append(data_without_header[i][0])
        i += 1 
    
    return(clean_data)


def list_of_filenames(data):
    """Procedure for processing list of brand names to a list of filenames
    """
    
    filenames = []
    for single_data in data:
        filename = single_data+".png"
        filenames.append(filename)
    
    return(filenames)


def image_scan(filename):
    """Function that takes an image and identifies the RGBA values for 
       each pixel in the image and returns a list of tuples with RGBA values,
       where transparency (RGBA = (0, 0, 0, 0) and white (RGB = 255, 255, 255))
       is removed.
    """
    

    image = Image.open(filename, mode = "r")
    rgba_values = list(image.getdata())
    
    #Remove all (0, 0, 0, 0) and (255, 255, 255) tuples from list
    rgba_values = [x for x in rgba_values if x != (255, 255, 255) and x != (0, 0, 0, 0)]
    
    return(rgba_values)


def processing_rgba(rgba):
    """Function that processes RGBA values to RGB and then rescales them from
       a range of 0-255 to 0-1 to be readable by "colour" lib
    """
    
    rgba_list = list(rgba)
    rgb_list = rgba_list[0:3]
    rgb_rescaled = [x/255 for x in rgb_list]
    rgb_tuple = tuple(rgb_rescaled)
    
    return(rgb_tuple)


def rgb_to_hsl(rgba_values):
    """Procedure that processes list of RGBA values to HSL values to identify 
       colour hue easier
    """
    
    hsl_list = [rgb2hsl(processing_rgba(x)) for x in rgba_values]
    
    return(hsl_list)


def find_dominant_colour(hsl_list):
    """Function that takes a list of HSL values and identifies and returns 
       the most dominant colour within that list
    """
    
    yellow = 0
    orange = 0
    red = 0
    pink = 0
    blue = 0
    green = 0
    monochrome = 0
    
    for hsl in hsl_list:
    
        if 37.5 < float(hsl[0]*360) < 82.5:
            yellow += 1
        elif 25 < float(hsl[0]*360) < 37.5:
            orange += 1
        elif 0 < float(hsl[0]*360) < 25 or 337.5 < float(hsl[0]*360) < 360:
            red += 1
        elif 262.5 < float(hsl[0]*360) < 337.5:
            pink += 1
        elif 157.5 < float(hsl[0]*360) < 262.5:
            blue += 1
        elif 82.5 < float(hsl[0]*360) < 157.5:
            green += 1
        else:
            monochrome =+ 1
    
    dominant_colour = max(yellow, orange, red, pink, blue, green, monochrome)
    
    if yellow == dominant_colour:
        dominant_colour = "yellow"
    elif orange == dominant_colour:
        dominant_colour = "orange"
    elif red == dominant_colour:
        dominant_colour = "red"
    elif pink == dominant_colour:
        dominant_colour = "pink"
    elif blue == dominant_colour:
        dominant_colour = "blue"
    elif green == dominant_colour:
        dominant_colour = "green"
    elif monochrome == dominant_colour:
        dominant_colour = "monochrome"
    return(dominant_colour)


def process_dominant_colour(filenames):
    """Function that runs
    """
    
    colour_list = []
    for filename in filenames:
        colour_list.append(find_dominant_colour(rgb_to_hsl(image_scan("Assets/"+filename))))
    
    return(colour_list)


def count_occurances(colour_list):
    """Procedure that counts occurances of each colour in a colour list
    """
    
    yellow = colour_list.count("yellow")
    orange = colour_list.count("orange")
    red = colour_list.count("red")
    pink = colour_list.count("pink")
    blue = colour_list.count("blue")
    green = colour_list.count("green")
    monochrome = colour_list.count("monochrome")
    
    count = [yellow, orange, red, pink, blue, green, monochrome]
    return(count)


def create_pie_chart(count):
    """Procedure that creates a pie chart from the count of occurances
    """
    
    labels = 'Yellow', 'Orange', 'Red', 'Pink', 'Blue', 'Green', 'Monochrome'
    sizes = count
    colours = {'Yellow': 'yellow',
           'Orange': 'orange',
           'Red': 'red',
           'Pink': 'pink',
           'Blue': 'blue',
           'Green': 'green',
           'Monochrome': 'gray'}
    
    explode = (0, 0, 0, 0, 0.1, 0, 0)
    fig1, ax = plt.subplots()
    
    ax.pie(sizes, labels = labels, explode = explode, autopct='%1.1f%%',
          colors = [colours[key] for key in labels])
    ax.axis('equal')
    plt.show()
 
    
def lookup_by_rank(rank):
    """Procedure that displays image of given index and its dominant colour, 
       as analysed by the programme
    """
    
    print("-" *50)
    index = rank - 1
    with Image.open("Assets/"+filenames[index]) as image:
        image.show()
    print(f"""
          The number {index+1} most valuable brand in the world is: {brands[index]}
          The dominant colour identified by the programme is: {colour_list[index]}
          """)
    menu()


def lookup_by_name(name):
    """Function that looks up a brands rank by its name and identifies its 
       logo's dominant colour, as analysed by the programme
    """
    
    print("-" *50)
    if name in brands:
        index = brands.index(name)
    with Image.open("Assets/"+filenames[index]) as image:
        image.show()
    print(f"""
          {name} rank in the 500 most valuable brand in the world is: {index+1}
          The dominant colour identified by the programme is: {colour_list[index]}
          """)
    menu()
    
        
def secondary(year):
    """Summary function executing other functions and procedures
    """
    
    raw_data = import_csv(year)
    
    global brands
    brands = processing_raw_data(raw_data)
    
    global filenames
    filenames = list_of_filenames(brands)
    
    global colour_list
    colour_list = process_dominant_colour(filenames)
    
    global count
    count = (count_occurances(colour_list))
    

def initial_data_selection():
    """Programm that asks user for a data set ranging from 2011-2021
    """
    
    print("-" *50)
    print("""
    Start by selecting what year you're interested in?
          2021
          2020
          2019
          2018
          2017
          2016
          2015
          2014
          2013
          2012
          2011""")
    prompt_data = ('Enter the year: ')
    year = int(input(prompt_data))
    while not 2011 <= year <= 2021:
        print(f"You selected: {year}")
        year = int(input(prompt_data))
    if year == 2021:
        yearfile = "brandirectory-ranking-data-global-2021.csv"
    elif year == 2020:
        yearfile = "brandirectory-ranking-data-global-2020.csv"
    elif year == 2019:
        yearfile = "brandirectory-ranking-data-global-2019.csv"
    elif year == 2018:
        yearfile = "brandirectory-ranking-data-global-2018.csv"
    elif year == 2017:
        yearfile = "brandirectory-ranking-data-global-2017.csv"
    elif year == 2016:
        yearfile = "brandirectory-ranking-data-global-2016.csv"
    elif year == 2015:
        yearfile = "brandirectory-ranking-data-global-2015.csv"
    elif year == 2014:
        yearfile = "brandirectory-ranking-data-global-2014.csv"
    elif year == 2013:
        yearfile = "brandirectory-ranking-data-global-2013.csv"
    elif year == 2012:
        yearfile = "brandirectory-ranking-data-global-2012.csv"
    elif year == 2011:
        yearfile = "brandirectory-ranking-data-global-2011.csv"

    
    print("-" *50)
    print("""
    Please hold on while the program analyses each logo pixel by pixel
    (This may take 1 minute to process)
    """)
    secondary(yearfile)
    print(f"""
          Out of the 500 most valuable brands in {year}, 
          {count[0]} had a yellow logo that conveys optimism,
          {count[1]} had an orange logo that conveys friendliness,
          {count[2]} had a red logo logo that conveys excitement,
          {count[3]} had a pink logo that conveys creativeness,
          {count[4]} had a blue logo that conveys trust,
          {count[5]} had a green logo that conveys peacefulness,
          {count[6]} had a monochrome logo that conveys balance.
    """)
    print("    (Either below or as a popup is a break down of the data by percentage)")
    create_pie_chart(count)


def menu():
    """Function that creates an interactive menu
    """
    
    print("-" *50)
    print("""
    What would you like to do next?
          1: Look up a logo and identify its colour by rank
          2: Look up a brand's rank and colour by name
          3: Try a different year
          4: Exit""")
          
    prompt_menu = ('Enter your selection (1-4): ')
    selection = int(input(prompt_menu))
    while not 1 <= selection <= 4:
        print(f"You selected: {selection}")
        selection = int(input(prompt_menu))
    if selection == 1:
        prompt_rank = ('Enter your rank selection (1-500): ')
        rank_selection = int(input(prompt_rank))
        while not 1 <= selection <= 500:
            print(f"You selected: {rank_selection}")
            selection = int(input(prompt_rank))
        lookup_by_rank(rank_selection)  
    elif selection == 2:
        prompt_name = ('Enter your brand name here (eg. Apple): ')
        name_selection = str(input(prompt_name))
        while not name_selection in brands:
            print(f"""
                  We couldn't find {name_selection}.
                  Make sure your spelling is correct
                  """)
            name_selection = input(prompt_name)
        lookup_by_name(name_selection)
    elif selection == 3:
        main()
    elif selection == 4:
        raise SystemExit
    
    
def main():
    """Main function executing other functions and procedures
    """
    
    print("""
    Welcome to my program
    This program analyses the colours of logos used by the 500 most valuable brands
    """)
    
    initial_data_selection()
        
    menu()
    
    
main()

