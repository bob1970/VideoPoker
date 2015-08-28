#!/usr/bin/python
from cards import Deck
from cards import VideoPokerHand
from cards import HoldemHand

print "Test Hand Number: 1"
d = Deck()
#d.Display()
h = VideoPokerHand(d)
h.Display()
print h.EvaluatePokerHand()

#Hold 2 cards
h.Hold(0)
h.Hold(4)
h.Display()
print h.EvaluatePokerHand()

#Draw New Cards... 
h.Draw(d)
h.Display()
print h.EvaluatePokerHand()

print ""
print "Test Texas Holdem Hand:"
d = Deck()
h = HoldemHand(d)
h.Display()

