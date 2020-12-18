import pyfiglet


class Prompter:
    
    def __init__(self, welcome_message: str = ''):
        self._print_welcome_message(welcome_message)

    def _print_welcome_message(self, message: str):
        if not message:
            raise ValueError('Welcome message cannot be empty!')

        out = pyfiglet.figlet_format(message, font="slant")
        print(out)

    def prompt(self, message: str, answer_type: str = str, answer_length: int = 50):
        if not message:
            raise ValueError('Prompt message cannot be empty!')
        
        while True:
            try:
                value = input(message)
                value = answer_type(value)
            except ValueError:
                print('Invalid input, lets try again!')
                continue
            else:
                break
        
        return value

if __name__ == '__main__':

    p = Prompter(welcome_message='Home Finder')
    city = p.prompt('Name of the city: ', answer_length=20)
    bedrooms = p.prompt('Number of bedrooms: ', answer_type=int)
    assert isinstance(city, str)
    assert isinstance(bedrooms, int)
