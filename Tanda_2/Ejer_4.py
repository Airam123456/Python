import pickle
import xml.sax

class Olimpiada():
    def __init__(self, game, year, season, city):
        self.game = game
        self.year = year
        self.season = season
        self.city = city

    def __str__(self):
        return "Game: " + self.game + "Year: " + self.year + "Season: " + self.season + "City: " + self.city

class Han