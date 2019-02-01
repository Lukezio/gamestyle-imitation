import configparser
import sys

class Configuration:

    CURRENT_SELECTED_GAME = None
    CONFIGURATION_FILE_PATH = 'app/configuration.ini'

    PARSER = None

    @staticmethod
    def load():
        Configuration.PARSER = configparser.SafeConfigParser()
        Configuration.PARSER.read(Configuration.CONFIGURATION_FILE_PATH)        

        #cur = configparser.ConfigParser()
        #cur.read(Configuration.CONFIGURATION_FILE_PATH)        
        #cur.

    @staticmethod
    def game_profile_exists(game_name):
        return game_name in [tup[1] for tup in Configuration.PARSER.items('game-names')]

    @staticmethod
    def add_game_profile(game_name):
        number_of_games = len(Configuration.PARSER.items('game-names'))
        Configuration.PARSER.set('game-names', 'game_' + str(number_of_games + 1), str(game_name))
        with open(Configuration.CONFIGURATION_FILE_PATH, "w") as configuration_file:
            Configuration.PARSER.write(configuration_file)
        print('done')

    @staticmethod
    def set_selected_game(game_name):
        Configuration.CURRENT_SELECTED_GAME = game_name

    @staticmethod
    def get_selected_game():
        return Configuration.CURRENT_SELECTED_GAME

    @staticmethod
    def get_all_games():
        return [tup[1] for tup in Configuration.PARSER.items('game-names')]