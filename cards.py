#!/usr/bin/python
import random

class Card(object):
    def __init__(self, rank, suit):
        self.Rank = rank
        self.Suit = suit
        self.LowValue, self.HighValue = self._Values()
        self.Held = False

    def Hold(self):
        self.Held = not self.Held

    def __str__(self):
        return self.Rank + " of " + self.Suit + ", values: " + str(self._Values()) + " " + str(self.Held)

class AceCard(Card):
    def _Values(self):
        return 1, 14

class NumberCard(Card):
    def _Values(self):
        return int(self.Rank), int(self.Rank)

class FaceCard(Card):
    def _Values(self):
        if self.Rank == "J":
            return 11, 11
        if self.Rank == "Q":
            return 12, 12
        if self.Rank == "K":
            return 13, 13

#=============================================================
# Factory Function for building a deck of 52 cards 
#=============================================================
def card(rank, suit):
    suit = {"H": "Hearts", "S": "Spades", "D": "Diamonds", "C": "Clubs"}[suit]
    if rank == 1: return AceCard("A", suit)
    if rank < 11: return NumberCard(str(rank), suit)
    return FaceCard({11: "J", 12: "Q", 13: "K"}[rank], suit)

class Deck(object):
    def __init__(self):
        self.Cards = []
        for s in ("H", "S", "D", "C"):
            for r in range(13):
                self.Cards.append(card(r+1,s))
        random.shuffle(self.Cards)

    def DealCard(self):
        return self.Cards.pop()

    def Display(self):
        print ""
        for c in self.Cards:
            print c

class Hand(object):
    def __init__(self, deck):
        self.Cards = []
        for i in range(self._NumberOfCards()):
            self.Cards.append(deck.DealCard())

    def Display(self):
        print ""
        for c in self.Cards:
            print c

class VideoPokerHand(Hand):
    def _NumberOfCards(self):
        return 5

    def Hold(self, i):
        self.Cards[i].Hold()

    def Draw(self, deck):
        for i in range(len(self.Cards)):
            if not self.Cards[i].Held:
                self.Cards[i] = deck.DealCard()
            else:
                self.Hold(i)

    #For DrawPoker and VideoPoker it's simple just call the EvaluatePokerHand and pass the 5 cards 
    def EvaluatePokerHand(self):
        return EvaluatePokerHand(self.Cards)

#===============================================================================================
# Poker Hand Evaluation functions... this function takes 5 figures out the poker hand
# was gonna put this in a class but they can be reused by multiple different Poker Hand Classes
# Note: Each indifidual hand check is called only after the higher level has been ruled out
# this makes the logic for each individual hand type easier
#===============================================================================================
def EvaluatePokerHand(cards):
    #Get some information from the list of cards
    LowValues = []
    HighValues = []
    Suits = []
    ValueCounts = {}
    for c in cards: 
        if c.Suit not in Suits:
            Suits.append(c.Suit)
        LowValues.append(c.LowValue)
        HighValues.append(c.HighValue)
        if c.HighValue not in ValueCounts:
            ValueCounts[c.HighValue] = 1
        else:
            ValueCounts[c.HighValue] += 1
    LowValues=sorted(LowValues)
    HighValues=sorted(HighValues)

    #We can now evaluate the poker hand
    if IsRoyalFlush(Suits, LowValues, HighValues): return "Royal Flush"
    if IsStraightFlush(Suits, LowValues, HighValues): return "Straight Flush"
    if IsFourOfAKind(ValueCounts): return "Four of a Kind"
    if IsFullHouse(ValueCounts): return "Full House"
    if IsFlush(Suits): return "Flush"
    if IsStraight(LowValues, HighValues): return "Straight"
    if IsThreeOfAKind(ValueCounts): return "Three of a Kind"
    if IsTwoPair(ValueCounts): return "Two Pair"
    if IsJacksOrBetter(ValueCounts): return "Jacks or Better"
    return "Nothing"

def IsRoyalFlush(suits, lowValues, highValues): 
    if highValues[4] == 14 and IsStraightFlush(suits, lowValues, highValues): return True
    return False

def IsStraightFlush(suits, lowValues, highValues):
    if IsStraight(lowValues, highValues) and IsFlush(suits): return True
    return False

def IsFourOfAKind(valueCounts):
    for v,c in valueCounts.iteritems():
        if c == 4: return True
    return False

def IsFullHouse(valueCounts):
    PairFound = False
    TripFound = False
    for v,c in valueCounts.iteritems():
        if c == 2: PairFound = True
        if c == 3: TripFound = True
    if PairFound and TripFound: return True
    return False

def IsFlush(suits):
    if len(suits) == 1: return True
    return False

def IsStraight(lowValues, highValues):
    if IsStraightSequence(lowValues): return True
    if IsStraightSequence(highValues): return True
    return False
  
def IsStraightSequence(values):
    for i in range(len(values)-1):
        if values[i]+1 != values[i+1]:
            return False
    return True

def IsThreeOfAKind(valueCounts):
    for v,c in valueCounts.iteritems():
        if c == 3: return True
    return False

def IsTwoPair(valueCounts):
    PairCount = 0
    for v,c in valueCounts.iteritems():
        if c == 2: PairCount += 1
    if PairCount == 2: return True
    return False

def IsJacksOrBetter(valueCounts):
    for v,c in valueCounts.iteritems():
        if v < 11: continue #only take Jacks or Better
        if c == 2: return True
    return False

class HoldemHand(Hand):
    def _NumberOfCards(self):
        return 2

class OmahaHand(Hand):
    def _NumberOfCards(self):
        return 4

