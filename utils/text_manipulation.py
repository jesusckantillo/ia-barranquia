from utils import __annotations__


class TextCard:
    def __init__(self, word):
        self.word = word
        self.translations = []
        self.examples = []

class ConvesationManager:
    def __init__(self,input_data) -> None:
        self.text = input_data.text
        self.type = input_data.type
        pass


class TextManipulator:
    def __init__(self):
        pass

    def create_text_card(self,data):
        
        def get_text_card_info(data):
            pass 
        card = TextCard(data)
        return card

    def generate_text_output(self,text_input : ConvesationManager)->None:
        pass

