class GameNameUtils:
    @staticmethod
    def normalized_name(name):
        return name.strip().lower().replace(' ', '_')
