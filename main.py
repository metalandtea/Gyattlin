

digits = (
    0,1,2,3,4,5,6,7,8,9
)

tokens = {
    "MARRIED",
    "DIVORCED",
    "LIKED",
    "HATED",
    "IS"
}

variable_lookup = {}

##----- ERROR CODES -----##

ERR_WRONG_DATATYPE = 1
ERR_NOT_FOUND = 2
ERR_VARIABLE_NOT_DEFINED = 3


##----- CLASSES -----##
class Token:
    
    def __init__(self,_type,_value):
        self.value = _value
        self.type = _type

class Lexer:

    def __init__(self, _text):
        self.text_array = _text.split()

    def parse(self):
        for slot, item in enumerate(self.text_array):
            # noinspection PyBroadException
            try:
                self.text_array[slot] = int(item)
            except BaseException:
                pass
        return self.text_array









class Error:

    def __init__(self,_error_type,_error_info = None):

        if _error_type == ERR_WRONG_DATATYPE:
            print( f"Wrong Datatype. Expected int, got {_error_info[0]}")

        elif _error_type == ERR_NOT_FOUND:
            print(f"Error finding datatype.")


###                             ###
###         INTERPRETER         ###
###                             ###

class Interpreter:

    def __init__(self,_token_array):
        self.token_array = _token_array

    def run(self):
        for token_place, token in enumerate(self.token_array):

            # MULTIPLICATION

            if token == "MARRIED":

                if token_place + 1 >= len(self.token_array) or token_place - 1 < 0:
                    Error(ERR_NOT_FOUND)

                elif type(self.token_array[token_place + 1]) is not int or type(
                    self.token_array[token_place - 1]) is not int:
                    Error(ERR_WRONG_DATATYPE, [type(self.token_array[token_place + 1])])

                else:
                    self.token_array[token_place + 1] = self.token_array[token_place - 1] * self.token_array[token_place + 1]
                    print(self.token_array[token_place + 1])

            # DIVISION

            if token == "DIVORCED":

                if token_place + 1 >= len(self.token_array) or token_place - 1 < 0:
                    Error(ERR_NOT_FOUND)

                elif type(self.token_array[token_place + 1]) is not int or type(self.token_array[token_place - 1]) is not int:
                    Error(ERR_WRONG_DATATYPE, [type(self.token_array[token_place + 1])])

                else:
                    self.token_array[token_place + 1] = self.token_array[token_place - 1] // self.token_array[token_place + 1]
                    print(self.token_array[token_place + 1])

            elif token == "LIKED":

                if token_place + 1 >= len(self.token_array) or token_place - 1 < 0:
                    Error(ERR_NOT_FOUND)

                elif type(self.token_array[token_place + 1]) is not int or type(self.token_array[token_place - 1]) is not int:
                    Error(ERR_WRONG_DATATYPE, [type(self.token_array[token_place + 1])])

                else:
                    self.token_array[token_place + 1] = self.token_array[token_place - 1] + self.token_array[token_place + 1]
                    print(self.token_array[token_place + 1])

            elif token == "HATED":

                if token_place + 1 >= len(self.token_array) or token_place - 1 < 0:
                    Error(ERR_NOT_FOUND)

                elif type(self.token_array[token_place + 1]) is not int or type(self.token_array[token_place - 1]) is not int:
                    Error(ERR_WRONG_DATATYPE, [type(self.token_array[token_place + 1])])

                else:
                    self.token_array[token_place + 1] = self.token_array[token_place - 1] - self.token_array[token_place + 1]
                    print(self.token_array[token_place + 1])

            elif token == "IS":
                if token_place + 1 >= len(self.token_array) or token_place - 1 < 0:
                    Error(ERR_NOT_FOUND)
                else:
                    previous_val = self.token_array[token_place - 1]
                    for i, item in enumerate(self.token_array):
                        if item == previous_val:
                            self.token_array[i] = self.token_array[token_place + 1]
                            print(self.token_array)




with open("Test.gyatt") as file:
    lex_string = file.read()

lex = Lexer(lex_string)
print(lex.parse())
inter = Interpreter(lex.parse())

inter.run()


