import random
import getch
from termcolor import colored
from os import system as x

class Field2048:

    PROBABILITY_OF_FOUR=0.1

    def __init__(self):
        self.state=[[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
        self.create_set_of_empty()
        self.legal_move=False
        self.score=0
        
        
    def create_set_of_empty(self):
        self.empty=set()
        for i in range(4):
            for j in range(4):
                if not self.state[i][j]:
                    self.empty.add((i,j))

    def add_tile(self):
        try:
            add_field=random.choice(tuple(self.empty))
        except IndexError:
            print("Gameover")
            exit()
        key=random.random()
        if key<self.PROBABILITY_OF_FOUR:
            current_add=4
        else:
            current_add=2
        self.state[add_field[0]][add_field[1]]=current_add

    
    def sweep_row(self,input_list):
        return_list=[x for x in input_list if x]
        for i in range(len(return_list)-1):
            if return_list[i]==return_list[i+1]:
                return_list[i]*=2
                self.score+=return_list[i]
                return_list[i+1]=None
        return_list=[x for x in return_list if x]
        while len(return_list)<4:
            return_list.append(None)
        if input_list==return_list:
            return False
        else:
            return return_list
    
    @staticmethod
    def make_field_from_rows(lst1,lst2,lst3,lst4):
        return[lst1,lst2,lst3,lst4]
    
    @staticmethod
    def make_field_from_columns(*args):
        field=[]
        for i in range(4):
            cur_row=[]
            for j in range(4):
                cur_row.append(args[j][i])
            field.append(cur_row)
        return field
    
    def make_columns_from_field(self):
        columns=[]
        for i in range(4):
            cur_col=[]
            for j in range(4):
                cur_col.append(self.state[j][i])
            columns.append(cur_col)
        return columns
    
    def move_up(self):
        columns=[]
        
        for column in self.make_columns_from_field():
            new_column=self.sweep_row(column)
            if not new_column:
                columns.append(column)
            else:
                columns.append(new_column)
                self.legal_move=True
        self.state=self.make_field_from_columns(*columns)

    def move_down(self):
        columns=[]
        for column in self.make_columns_from_field():
            new_column=self.sweep_row(column[::-1])
            if not new_column:
                columns.append(column)
            else:
                columns.append(new_column[::-1])
                self.legal_move=True
        self.state=self.make_field_from_columns(*columns)

    def move_left(self):
        rows=[]
        for row in self.state:
            new_row=self.sweep_row(row)
            if not new_row:
                rows.append(row)
            else:
                rows.append(new_row)
                self.legal_move=True
        self.state=rows

    def move_right(self):
        rows=[]
        for row in self.state:
            new_row=self.sweep_row(row[::-1])
            if not new_row:
                rows.append(row)
            else:
                rows.append(new_row[::-1])
                self.legal_move=True   
        self.state=rows

    def make_move(self):
        
        move=getch.getch().lower()
        if move=="w":
            self.move_up()
        if move=="a":
            self.move_left()
        if move=="d":
            self.move_right()
        if move=="s":
            self.move_down()
        if move=="x":
            return move
    
    @staticmethod
    def print_cell(i):
        if i==None:
            return "     "
        elif i==2:
            return colored("  2  ","black", "on_white")
        elif i==4:
            return colored("  4  ","black", "on_light_grey")
        elif i==8:
            return colored("  8  ","black", "on_light_yellow")
        elif i==16:
            return colored("  16 ","black", "on_yellow")
        elif i==32:
            return colored("  32 ","white", "on_light_red")
        elif i==64:
            return colored("  64 ","white", "on_red")
        elif i==128 or i==256 or i==512:
            return colored(f" {i} ","white", "on_green")
        else:
            return colored(f"{i}".center(5),"white","on_blue")
        
        
    def print_field(self):
        top="┌─────┬─────┬─────┬─────┐\n"
        middle="├─────┼─────┼─────┼─────┤\n"
        bottom="└─────┴─────┴─────┴─────┘"
        field=f"Use a,s,d,w to play        Score: {self.score}\n\n"+top
        for i in range(4):
            for j in range(4):
                field+="│"+self.print_cell(self.state[i][j])
            field+="│\n"
            field+=middle*int(i<3)
        field+=bottom
        x("clear")
        print(field)


    def play(self):
        while True:
            self.add_tile()
            self.print_field()
            while not self.legal_move:
                if self.make_move()=="x":
                    exit()
            self.legal_move=False
            self.create_set_of_empty()

game=Field2048()
game.play()






    