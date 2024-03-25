### NOTE FOR FUTURE ME: REMEMBER TO CHANGE THE ERROR STATES TO ENUMS AT SOME POINT ###


import sys

## DATATYPES ##

DT_INT = "DT_INT"
DT_NONE = "DT_NONE"
DT_STR = "DT_STR"

NONE_VAL = "NONE"

tokens = {
    ### MATH OPERATIONS ###

    "MARRIED", # Multiplication
    "DIVORCED", # Division
    "LIKED", # Addition
    "HATED", # Subtraction

    ### ASSIGNMENT ###

    "IS", # assignment: val -> x

    ### PRINTING ###

    "MANSPLAIN", # print with a new line after
    "MANSPLAIN_INLINE", #print without new line after
    "PERSONAL_SPACE", #newline
    
    ### LOOPING ###
    
    "END", # signifies the end of a loop
    "RUN_IT_DOWN", # Repeat (x) times

}

## Token Class

class Token:

    def __init__(self,_type,_value = None):
        self.value = _value
        self.type = _type

    def __repr__(self):
        return f"{self.type} : {self.value}" if self.value else f"{self.type}"

##----- ERROR CODES -----##

ERR_WRONG_DATATYPE = 0
ERR_NOT_FOUND = 1
ERR_VARIABLE_NOT_DEFINED = 2

# Variable Errors

ERR_NOT_VARIABLE = 4

##-----#|  VARIABLE FUNCTIONS |#-----##

def is_var(token):
    if isinstance(token, Token) and isinstance(token.value,Token):
        return True

    return False

def get_value(variable):
    if is_var(variable):
        return variable.value

    return variable

def get_type(variable):
    if is_var(variable):
        return variable.value.type

    return variable.type

def set_var(var_1,value):
    if is_var(value):
        var_1.value = value.value
    else:
        var_1.value = value

def check_for_error(error_code,check = None,*check_info):

    # WRONG DATATYPE
    # Checks individual elements and sees if they are the correct datatype

    if error_code == ERR_WRONG_DATATYPE:
        for info in check_info:
            if get_type(info) != check:
                Error(ERR_WRONG_DATATYPE,info.type)


    # NOT FOUND
    # Checks specifically indexes and sees if their out of bound(check)

    if error_code == ERR_NOT_FOUND:
        for info in check_info:
            if info > len(check)-1 or info < 0:
                Error(ERR_NOT_FOUND)

    # NOT VARIABLE
    # checks if item is a variable or nor

    if error_code == ERR_NOT_VARIABLE:
        for info in check_info:
            if not is_var(info):
                Error(ERR_NOT_VARIABLE)

    if error_code == ERR_VARIABLE_NOT_DEFINED:
        for info in check_info:
                if get_value(info).type is DT_NONE:
                    Error(ERR_VARIABLE_NOT_DEFINED,info.type)

## Error Class

class Error:

    def __init__(self,_error_type,_error_info = None):

        if _error_type == ERR_WRONG_DATATYPE:
            print( f"Error: Wrong Datatype. Expected int, got {_error_info}")

        elif _error_type == ERR_NOT_FOUND:
            print(f"Error: Not Found.")

        elif _error_type == ERR_VARIABLE_NOT_DEFINED:
            print(f"Error: Variable -[  {_error_info}  ]- Not Defined")

        elif _error_type == ERR_NOT_VARIABLE:
            print(f"Error: Expected Variable")

        sys.exit()


###                     ###
###         LEXER       ###
###                     ###

class Lexer:

    def __init__(self, _text):
        self.text_array = _text.split()

    def parse(self):

        self.del_in_parens()

        print(self.text_array)

        for slot, item in enumerate(self.text_array):

            if item in tokens:
                self.text_array[slot] = Token(item,None)
            else:
                try:
                    self.text_array[slot] = Token(DT_INT, int(item))
                except (Exception,):
                    if not isinstance(self.text_array[slot], Token):


                        if '"' in self.text_array[slot]:
                            self.text_array[slot] = Token(DT_STR,item)
                            self.text_array[slot].value = item.replace('"','')
                        else:
                            self.text_array[slot] = Token(item, Token(DT_NONE, NONE_VAL))

                        pass

        return self.text_array

    def del_in_parens(self):
        for i in range(len(self.text_array)):
            if self.text_array[i] == '-[':
                self.find_other_paren(i)

        self.text_array = [i for i in self.text_array if i != "NULL"]


    def find_other_paren(self,index):
        for j in range(index, len(self.text_array)):
            if self.text_array[j] == ']-':
                self.text_array[index:j + 1] = ['NULL' for k in range(len(self.text_array)) if k >= index and k <= j]
                break

###                             ###
###         INTERPRETER         ###
###                             ###

class Interpreter:

    def __init__(self,_token_array):
        self.token_array = _token_array
        self.loop_amt = 0
        self.loop_start_pos = 0
        self.looping = False

    def run(self):
        ###TOKEN ARRAY###
        token_read = self.token_array

        place = -1

        while place < len(token_read)-1:
            place += 1
            token = token_read[place]

            #print(token_read) # Just to do debugging

            ## Variables

            prev_place = place -1
            next_place = place + 1

            ## IS token

            if token.type == "IS":

                check_for_error(ERR_NOT_FOUND,token_read,prev_place,next_place)
                check_for_error(ERR_VARIABLE_NOT_DEFINED,None, token_read[prev_place])
                #check_for_error(ERR_WRONG_DATATYPE,DT_INT, token_read[prev_place])
                check_for_error(ERR_NOT_VARIABLE,None, token_read[next_place])

                new_var = token_read[prev_place]
                prev_var = token_read[next_place]

                for i in range(len(token_read)):
                    if token_read[i].type == prev_var.type:
                        set_var(token_read[i], new_var)

            ## MANSPLAIN token

            elif token.type == "MANSPLAIN":
                check_for_error(ERR_NOT_FOUND, token_read, next_place)

                print(get_value(token_read[next_place]).value)

            elif token.type == "MANSPLAIN_INLINE":
                check_for_error(ERR_NOT_FOUND, token_read, next_place)

                print(get_value(token_read[next_place]).value, end=" ")

            elif token.type == "PERSONAL_SPACE":
                print("\n")

            ##                          ###
            ##      MATH OPERATIONS     ###
            ##                          ###

            ##ADDITION
            elif token.type == "LIKED":
                check_for_error(ERR_NOT_FOUND,token_read,prev_place,next_place)
                check_for_error(ERR_WRONG_DATATYPE,DT_INT,token_read[prev_place],token_read[next_place])

                val_1 = get_value(token_read[next_place])
                val_2 = get_value(token_read[prev_place])

                set_var(token_read[next_place],Token(DT_INT, int(val_1.value + val_2.value)))

            elif token.type == "HATED":
                check_for_error(ERR_NOT_FOUND,token_read,prev_place,next_place)
                check_for_error(ERR_WRONG_DATATYPE,DT_INT,token_read[prev_place],token_read[next_place])

                val_1 = get_value(token_read[next_place])
                val_2 = get_value(token_read[prev_place])

                set_var(token_read[next_place],Token(DT_INT, int(val_1.value - val_2.value)))

            elif token.type == "MARRIED":
                check_for_error(ERR_NOT_FOUND,token_read,prev_place,next_place)
                check_for_error(ERR_WRONG_DATATYPE,DT_INT,token_read[prev_place],token_read[next_place])

                val_1 = get_value(token_read[next_place])
                val_2 = get_value(token_read[prev_place])

                set_var(token_read[next_place],Token(DT_INT, int(val_1.value * val_2.value)))

            elif token.type == "DIVORCED":
                check_for_error(ERR_NOT_FOUND,token_read,prev_place,next_place)
                check_for_error(ERR_WRONG_DATATYPE,DT_INT,token_read[prev_place],token_read[next_place])

                val_1 = get_value(token_read[next_place])
                val_2 = get_value(token_read[prev_place])

                set_var(token_read[next_place],Token(DT_INT, int(val_1.value // val_2.value)))

            elif token.type == "RUN_IT_DOWN":

                check_for_error(ERR_NOT_FOUND,token_read,next_place)
                check_for_error(ERR_WRONG_DATATYPE,DT_INT,token_read[next_place])

                self.loop_start_pos = place
                self.loop_amt = get_value(token_read[next_place].value) - 1
                self.looping = True

            elif token.type == "END":

                if self.looping is True:
                    place = self.loop_start_pos
                    self.loop_amt -= 1

                    if self.loop_amt == 0:
                        self.looping = False
                        self.loop_start_pos = 0


##################################################################
##################################################################
##################################################################


with open("Test.gyatt") as file:
    lex_string = file.read()

lex = Lexer(lex_string)
print(f"\n Token List is: {lex.parse()} \n")
print("RUNNING...")
print("______________________________\n")

inter = Interpreter(lex.parse())

inter.run()

#a = get_type(Token())

print()
