# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 09:50:48 2021

@author: 07062962468
"""

import tkinter as tk
import random

def load_images(card_images):
    suits=['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']
    
    extension = 'ppm'
        
    #for each suit, retrieve the image for the card
    for suit in suits:
        #first the number cards 1 - 10
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tk.PhotoImage(file=name)
            card_images.append((card, image,))
            
        #the face cards
        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tk.PhotoImage(file=name)
            card_images.append((10, image,))

def deal_card(frame):
    #pop the next card off the deck
    next_card = deck.pop(0)
    deck.append(next_card)
    #add the image to a Label and Dislay the label
    tk.Label(frame, image=next_card[1], relief='raised' ).pack(side='left')
    #now return the card's face value
    return next_card

def score_hand(hand):
    #Calculate the total score of all cards in the list
    #Only one ace can have the value 11, and this will reduce to 1 if the hand would burst
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        #if we would bust, check if there is an ace and subtract 10
        if score >21 and ace:
            score -= 10
            ace = False
    return score

def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)
    
    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set('Dealer wins!')
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set('player wins!')
    elif dealer_score > player_score:
        result_text.set('Dealer wins!')
    else:
        result_text.set('Draw!')
            
    
def deal_player():
    player_hand.append(deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    dealer_score = score_hand(dealer_hand)
    
    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set('Dealer Wins!')
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set('player wins!')
    elif dealer_score > player_score:
        result_text.set('Dealer wins!')
    else:
        result_text.set('Draw!')

def restart_game():
    global dealer_hand
    global player_hand
    global dealer_card_frame
    global player_card_frame
    dealer_card_frame.destroy()
    player_card_frame.destroy()
    dealer_card_frame = tk.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    player_card_frame = tk.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)
    player_hand.clear()
    dealer_hand.clear()
    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()
    random.shuffle(deck)

    
def end_game():
    mainwindow.destroy()   

mainwindow = tk.Tk()
mainwindow.title('Black Jack')
mainwindow.geometry('640x480')
mainwindow.configure(background='green')

result_text = tk.StringVar()
result = tk.Label(mainwindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)
card_frame = tk.Frame(mainwindow, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealer_score_label = tk.IntVar()
tk.Label(card_frame, text='Dealer', background='green', fg='white').grid(row=0, column=0)
tk.Label(card_frame, textvariable = dealer_score_label, background='green', fg='white').grid(row=1, column=0)

#embedded frame to hold the card images
dealer_card_frame = tk.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

player_score_label = tk.IntVar()
# player_score = 0
# player_ace = False

tk.Label(card_frame, text='Player', background='green', fg='white').grid(row=2, column=0)
tk.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)

#embedded frame to hold the card images
player_card_frame = tk.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = tk.Frame(mainwindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

dealer_button = tk.Button(button_frame, text='Dealer', command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tk.Button(button_frame, text='Player', command=deal_player)
player_button.grid(row=0, column=1)

restart_button = tk.Button(button_frame, text='Restart', command=restart_game)
restart_button.grid(row=0, column=2)

end_button = tk.Button(button_frame, text='End Game', command=end_game)
end_button.grid(row=0, column=3)

cards = []
load_images(cards)
# print(cards)
#Create a new deck of cards and shuffle them
deck = list(cards)
random.shuffle(deck)

#create list to stor dealer's and player's hands
dealer_hand = []
player_hand = []

deal_player()
dealer_hand.append(deal_card(dealer_card_frame))
dealer_score_label.set(score_hand(dealer_hand))
deal_player()

mainwindow.mainloop()
