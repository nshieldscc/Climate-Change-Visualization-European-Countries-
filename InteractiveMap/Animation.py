import pandas as pd
import pygame
import time
import pickle
import math

#import sys to break for loop
import sys
import matplotlib.pyplot as plt

#import the data that has already been parsed
file = open('countrytempdata', 'rb')
annual_averages_12monthyears = pickle.load(file)

#dictionary of pixel coordinates of countries
locations = {
    "Iceland":(120, 63),
    "Norway":(291, 149),
    "Sweden":(356, 124),
    "Finland":(445, 113),
    "United Kingdom":(161, 271),
    "Ireland":(105, 252),
    "Portugal":(27, 487),
    "Spain":(86, 494),
    "France":(194, 391),
    "Belgium":(234, 316),
    "Netherlands":(247, 285),
    "Germany":(299, 324),
    "Switzerland":(266, 391),
    "Italy":(325, 462),
    "Poland":(414, 292),
    "Austria":(353, 378),
    "Slovakia":(420, 351),
    "Hungary":(417, 384),
    "Slovenia":(359, 405),
    "Croatia":(373, 419),
    "Bosnia And Herzegovina":(407, 438),
    "Serbia":(447, 434),
    "Romania":(495, 399),
    "Bulgaria":(510, 458),
    "Czech Republic":(366, 334),
    "Estonia":(462, 170),
    "Latvia":(465, 198),
    "Lithuania":(456, 227),
    "Belarus":(507, 255),
    "Moldova":(543, 361),
    "Ukraine":(555,319),
    "Denmark":(296, 222),
    "Montenegro":(428, 464),
    "Albania":(440, 495),
    "Greece":(470, 523),
    "Turkey":(646, 487)
    }

#given a year, return a dictionary of "country":temperature
def get_countries(annual_averages, countries, in_year):
    temps = {}
    #iterate through each country
    for country in annual_averages:
        #iterate through each year of every country
        for year, temp in annual_averages[country].items():
            #add temperature to dicitonary
            if year == str(in_year):
                if country in countries:
                    temps[country] = str(temp)
    return temps

#given the temperatures and the pixel coords render the circles
def make_circles(rads, surface, locations):
    #perform the same action for every country
    for country, rad in rads.items():
        #get pixel coords
        x, y = locations[country]
        rad = float(rad)
        #draw circles in red if greater than 0 or blue if less than 0
        if rad <= 0:
            pygame.draw.circle(surface, (0,0,int(250-rad*(-4))), (x,y), \
                               rad*(-2), width = 2)
        else:
            pygame.draw.circle(surface, (int(250-rad*4),0,0),(x,y), \
                               rad*2, width = 2)
    pygame.display.flip()

#draw the circles that stay on the stay on the map
#same as make_circles() but fill in the circles and change color to gray
def baseline_circles(rads, surface, locations):
    for country, rad in rads.items():
        x, y = locations[country]
        rad = float(rad)
        if rad <= 0:
            pygame.draw.circle(surface, (128, 128, 155), (x,y), rad*(-2))
        else:
            pygame.draw.circle(surface, (128, 128, 155),(x,y), rad*2)
    pygame.display.flip()

#load the background image, baseline circles, and text onto the display
def load_Europe(surface, width, height):
    surface.fill("WHITE")
    #load the image
    image = pygame.image.load("Europe.GIF")
    background  = pygame.transform.scale(image, (width, height))
    display = surface.blit(background, (0,0))
    #print the title
    F = pygame.font.Font(size = 50)
    text = F.render("Yearly Avg. Temperature for European Nations", \
                    True, "BLACK", "WHITE")
    screen.blit(text, dest = (20,10))
    pygame.display.flip()
    #load the baseline circles
    baseline_circles(get_countries(annual_averages_12monthyears, \
                    locations.keys(), 1810), surface, locations)
    return display

#display the text the click a country
def display_clickcountry():
    F = pygame.font.Font(size = 50)
    text = F.render("Click a Country", True, "BLUE")
    screen.blit(text, dest = (290,775))
    pygame.display.flip()
    
#given mouse location and country locations detect if user clicked on a country
def detect_country_click(x, y, locations):
    ret_country = 'n/a'
    #check against every country
    for country, coords in locations.items():
        if x<coords[0]+10 and x>coords[0]-10 and \
        y<coords[1]+10 and y>coords[1]-10:
            ret_country = country
    return ret_country

#import and display moving average plot
def display_plot(country):
    image = pygame.image.load(f"{country}.png")
    image = pygame.transform.scale(image, (800, 400))
    screen.blit(image, dest=(0,600))
    return image

#set up pygame
pygame.init()
scr_width = 800
scr_height = 1000
map_width = 800
map_height = 600

pygame.font.init()
screen = pygame.display.set_mode((scr_width, scr_height))
disp = load_Europe(screen, map_width, map_height)

plot_check = False
country_click = False
no_country = False

temp_data = {}


#display every year sequentially
running = True
for x in range(214):
    year = 1800+x
    #get the temperature for that year
    radii = get_countries(annual_averages_12monthyears, locations.keys(), year)
    #print the circles with given temps
    make_circles(radii, screen, locations)
    #display the year in the corner
    F = pygame.font.Font(size = 50)
    text = F.render(str(year), True, "BLUE")
    screen.blit(text, dest = (675,50))
    pygame.display.flip()
    #add a buffer so that the image hangs on the screen
    #before 1980 the buffer is shorter than after
    start = time.time()
    if int(year)<1980:
        while time.time() < start+0.2:
            pass
        
    elif int(year)>=1980:
        while time.time() <start+0.4:
            pass
    
    #reset the background    
    background = load_Europe(screen, map_width, map_height)
    
    #detext whether the user wants to quit
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
    #add the moving average plots below the map        
    for event in events:
        #detect mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            country_click = True
            
            #specify the country based on the click location
            mouse_x, mouse_y = pygame.mouse.get_pos()
            country = detect_country_click(mouse_x, mouse_y, locations)
            
            #change variables depending on whether a country was clicked
            if country == 'n/a':
                no_country = True
                
            #get the image file from display_plot function
            else:
                no_country = False
                image = display_plot(country)
                plot_check = True

    #blit the plot onto the map            
    if plot_check:
        screen.blit(image, dest=(0,600))

    #change text to prompt user to actually click on a country if they didn't before    
    if no_country:
        plot_check = False
        F = pygame.font.Font(size = 50)
        text = F.render("No country found. Click again!", True, "BLUE")
        screen.blit(text, dest = (200,775))
        pygame.display.flip()

    #display "click a country" if one has not been clicked yet    
    if not country_click:
        display_clickcountry()


running = True
check = True
displayed = False

#after running the animation
while running:
    #set the display: print the circles and year
    for i in range(0,1):
        make_circles(get_countries(annual_averages_12monthyears, \
                                   locations.keys(), 2012), screen, locations)
        text = F.render(str(2013), True, "BLUE")
        screen.blit(text, dest = (675,50))
        pygame.display.flip()
    
    #repeat all earlier logic for closing the window and country clicking/plot displaying
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            country_click = True
            
            #specify the country based on the click location
            mouse_x, mouse_y = pygame.mouse.get_pos()
            country = detect_country_click(mouse_x, mouse_y, locations)
            
            if country == 'n/a':
                no_country = True
                
            #get the image file from display_plot function
            else:
                no_country = False
                image = display_plot(country)
                plot_check = True
                
    if plot_check:
        screen.blit(image, dest=(0,600))
        
    if no_country:
        plot_check = False
        text = F.render("No country found. Click again!", True, "BLUE")
        screen.blit(text, dest = (200,775))
        pygame.display.flip()
        load_Europe(screen, map_width, map_height)
        
    if not country_click:
        display_clickcountry()
    
#quitting sequence for pygame
pygame.display.quit()
pygame.quit()
