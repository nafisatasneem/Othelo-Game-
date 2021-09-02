
import tkinter
import random
from time import sleep 

REFRESH = 30

class Othello:
    def __init__(self):
        self.board = Board()
        self.view = TkView(self.board)
        self.view.players = {}
    
    def play_game(self):
        self.view.init_window()
        self.view.choice_attack()
        self.random = RandomPlayer(self.view)
        self.board.coord_to_piece = self.view.coord_to_piece 

        self.view_loop()
        self.hit_loop()
        self.view.mainloop()

    def view_loop(self):
            
            if "wait" not in self.view.players.keys():
                pass
            elif self.view.players[self.board.turn] == "Before the game starts":
                self.board.turn = "first"  
                self.view.clicked_tag = "null"   
            elif self.view.players[self.board.turn] == "human" and self.view.set_flag == False:
                turn_num = self.board.turn
                if turn_num == "first":
                    piece_color = "Black piece"
                elif turn_num == "second":
                    piece_color = "White piece"
                else:
                    piece_color = ""        
                
                self.view.player_info = tkinter.Label(self.view.window, text='Turn of Human:  ' + piece_color, bg='#008080', fg='#000000', width=30)
                self.view.player_info.place(x=20, y=self.view.WINDOW_SIZE + 20)
                self.view.set_flag = True

               
            elif self.view.players[self.board.turn] == "random" or self.view.players[self.board.turn] == "random_2" or self.view.players[self.board.turn] == "random_3" and self.view.set_flag == False:
                turn_num = self.board.turn
                if turn_num == "first":
                    piece_color = "Black piece"
                elif turn_num == "second":
                    piece_color = "White piece"
                else:
                    piece_color = ""  

                
                if self.view.players[self.board.turn] == "random":
                    self.view.player_info = tkinter.Label(self.view.window, text='Turn of CPU(weak):  ' + piece_color, bg='#008080', fg='#000000', width=30)

                elif self.view.players[self.board.turn] == "random_2":
                    self.view.player_info = tkinter.Label(self.view.window, text='Turn of CPU(little strong):  ' + piece_color, bg='#008080', fg='#000000', width=30)

                elif self.view.players[self.board.turn] == "random_3":
                    self.view.player_info = tkinter.Label(self.view.window, text='Turn of CPU(strong):  ' + piece_color, bg='#008080', fg='#000000', width=30)
                
                self.view.player_info.place(x=20, y=self.view.WINDOW_SIZE + 20)
                self.view.set_flag = True
            
            if self.view.restart_flag:
                return
            else:                  
                return self.view.window.after(REFRESH, self.view_loop)

    def hit_loop(self):
        if self.board.finish_flag:
            pass
        else:         
            self.board.finish_game()
        if self.board.finish_flag:
            self.board.get_result(self.view)
            self.view.alert_finish(self.board)
            if self.view.restart_flag:
                self.view.window.destroy()
                play_othello()
        if self.board.hit == False and self.board.finish_flag != True:
            if self.board.search_flag == False and self.board.turn != "wait":
                self.search_avalable_cell()
                if len(self.board.search_hit_list_coord) != 0:
                    for cell in self.board.search_hit_list_coord:
                        self.view.draw_avalable_cell(cell)
            if self.view.clicked_tag != "null":
                if self.board.turn != "wait" and self.view.players[self.board.turn] == "human":
                    coord = self.view.tag_to_coord[self.view.clicked_tag]
                    self.board.check_avalable_hit(coord, self.view) 
                    if self.board.avalable_hit:
                        self.board.dohit(coord)

                        self.board.reverse_piece(coord,self.view)

                        if self.board.turn == "first":
                            self.view.draw_piece_black(coord)
   
                        elif self.board.turn == "second":
                            self.view.draw_piece_white(coord)
                          
                        self.view.clicked_tag = "null"

                        self.board.hit = True
                        
                        if self.view.alert_flag == True:
                            self.view.delete_alert()
                        else:
                            pass    
                        if len(self.board.search_hit_list_coord) != 0:
                                for cell in self.board.search_hit_list_coord:
                                    self.view.delete_avalable_cell(cell)

                        self.board.change_turn()

                        if self.view.set_flag:
                            self.view.player_info.destroy()
                        self.view.set_flag = False
        
                    else:
                        self.view.alert_message_human()
        
            if self.board.turn != "wait" and self.view.players[self.board.turn] == "random":
                    self.random_hit_1()
            elif self.board.turn != "wait" and self.view.players[self.board.turn] == "random_2":
                    self.random_hit_2()   
            elif self.board.turn != "wait" and self.view.players[self.board.turn] == "random_3":
                    self.random_hit_3()
        return self.view.window.after(500, self.hit_loop)
    def search_avalable_cell(self):
        self.board.search_hit_list_coord = []
        self.board.search_hit_list_tag = []
        self.board.search_flag = True
        self.random.search_hit(self.board)
        for tag in self.board.search_hit_list_tag:
            coord = self.view.tag_to_coord[tag]
            piece_count = self.board.coord_to_piece[coord]
            if piece_count == 0:
                self.board.search_hit_list_coord.append(coord) 

    def random_avalable_cell(self):
        self.board.random_hit_list_coord = []
        self.board.random_hit_list_tag = []
        self.random.random_hit(self.board)
        for tag in self.board.random_hit_list_tag:
            coord = self.view.tag_to_coord[tag]
            piece_count = self.board.coord_to_piece[coord]
            if piece_count == 0:
                self.board.random_hit_list_coord.append(coord)  
    
    def random_hit_1(self):
        self.view.alert_message_random()
        self.search_avalable_cell()
        self.random_avalable_cell()
        hit_count = len(self.board.random_hit_list_coord)

        if hit_count == 0 and self.board.finish_flag == False:
            
            self.pass_count += 1
            if self.pass_count == 2:
                self.board.finish_flag = True
                print("clogging")
                     
            self.board.change_turn()  
        else:
            self.pass_count = 0

            if hit_count == 1:
                coord_list_idx = 0
            else:
                coord_list_idx = random.randint(0,hit_count-1)
            coord = self.board.random_hit_list_coord[coord_list_idx]
            self.common_hit(coord)

    def random_hit_2(self):
        self.view.alert_message_random()
        self.search_avalable_cell()
        self.random_avalable_cell()
        hit_count = len(self.board.random_hit_list_coord)
        if hit_count == 0 and self.board.finish_flag == False:
            self.pass_count += 1
            if self.pass_count == 2:
                self.board.finish_flag = True
                print("clogging")

            self.board.change_turn() 
        else:
            self.pass_count = 0

            if hit_count == 1:
                coord_list_idx = 0
            else:
                for x in range(0,8,7):
                    for y in range(0,8,7):
                        for dx in range(-1,2,1):
                            for dy in range(-1,2,1):
                                around_tag = str(x+dx) + "_" + str(y+dy)
                                if around_tag != "0_0" and around_tag != "7_7" and around_tag != "7_0" and around_tag != "0_7":

                                    for ran_coord in self.board.random_hit_list_coord:
                                        random_tag = self.view.coord_to_tag[ran_coord]
                                        
                                        if around_tag == random_tag and len(self.board.random_hit_list_coord) != 1:
                                            around_idx = self.board.random_hit_list_coord.index(ran_coord)
                                            self.board.random_hit_list_coord.pop(around_idx)
                
                hit_count = len(self.board.random_hit_list_coord)
                if hit_count == 1:
                    coord_list_idx = 0
                else:      
                    coord_list_idx = random.randint(0,hit_count-1)
    
                for coord in self.board.random_hit_list_coord:
                    random_tag = self.view.coord_to_tag[coord]

                    if random_tag == "0_0" or random_tag == "0_7" or random_tag == "7_0" or random_tag == "7_7":
                        coord_list_idx = self.board.random_hit_list_coord.index(coord)
                                       
            coord = self.board.random_hit_list_coord[coord_list_idx]
            self.common_hit(coord)
    
    def random_hit_3(self):
        self.view.alert_message_random()
        self.search_avalable_cell()
        self.random_avalable_cell()
        hit_count = len(self.board.random_hit_list_coord)
        if hit_count == 0 and self.board.finish_flag == False:
            
            self.pass_count += 1
            if self.pass_count == 2:
                self.board.finish_flag = True
                print("clogging")

            self.board.change_turn()
            # self.view.set_flag = False    
        else:
            if hit_count == 1:
                coord_list_idx = 0
            else:
                for x in range(0,8,7):
                    for y in range(0,8,7):
                        for dx in range(-1,2,1):
                            for dy in range(-1,2,1):
                                around_tag = str(x+dx) + "_" + str(y+dy)
                                if around_tag != "0_0" and around_tag != "7_7" and around_tag != "7_0" and around_tag != "0_7":

                                    for ran_coord in self.board.random_hit_list_coord:
                                        random_tag = self.view.coord_to_tag[ran_coord]
                                        
                                        if around_tag == random_tag and len(self.board.random_hit_list_coord) != 1:
                                            around_idx = self.board.random_hit_list_coord.index(ran_coord)
                                            self.board.random_hit_list_coord.pop(around_idx)
                 
                hit_count = len(self.board.random_hit_list_coord)
                if hit_count == 1:
                    coord_list_idx = 0
                else:
                    max_eval_coord = ""
                    max_eval_score = -100000
                    for coord in self.board.random_hit_list_coord:
                        random_tag = self.view.coord_to_tag[coord]
                        random_evalvalue = self.board.tag_to_evalvalue[random_tag]
                        if random_evalvalue > max_eval_score:
                            max_eval_score = random_evalvalue
                            max_eval_coord = coord
                    coord_list_idx = self.board.random_hit_list_coord.index(max_eval_coord)

                    for coord in self.board.random_hit_list_coord:  
                        random_tag = self.view.coord_to_tag[coord]

                    if random_tag == "0_0" or random_tag == "0_7" or random_tag == "7_0" or random_tag == "7_7":
                        coord_list_idx = self.board.random_hit_list_coord.index(coord)
                                       
            coord = self.board.random_hit_list_coord[coord_list_idx]
            self.common_hit(coord)
    
    def common_hit(self, coord):
        self.board.dohit(coord)
        self.board.reverse_piece(coord,self.view)

        if self.board.turn == "first":
            self.view.draw_piece_black(coord)
   
        elif self.board.turn == "second":
            self.view.draw_piece_white(coord)
            
        self.board.hit = True
        
        if self.view.alert_flag == True:                    
            self.view.delete_alert()
        else:
            pass    
        if len(self.board.search_hit_list_coord) != 0:
                for cell in self.board.search_hit_list_coord:
                    self.view.delete_avalable_cell(cell)
        self.board.change_turn()
        
        self.view.set_flag = False                    

class TkView:
    def __init__(self, board):

        self.WINDOW_SIZE = 590
        self.CELL_SIZE = 70
        self.BOARD_OFFSET = 15
        self.set_flag = False
        self.alert_flag = False
        self.board = board
        self.restart_flag = False
        self.restart_flag_alert = False
        self.pass_flag_alert = False

    def init_window(self):
        self.window = tkinter.Tk()
        self.window.title("Othello")
        self.window.resizable(width=False, height=False)
        self.window.attributes("-topmost", True)

        self.canvas = tkinter.Canvas(
            self.window,
            width=self.WINDOW_SIZE,
            height=self.WINDOW_SIZE  + 80
            )

        self.canvas.create_rectangle(
            0, 0, self.WINDOW_SIZE, self.WINDOW_SIZE, fill="blue")

        self.canvas.create_rectangle(
            0, self.WINDOW_SIZE, self.WINDOW_SIZE, self.WINDOW_SIZE - self.BOARD_OFFSET + 100 , fill="white")
        self.cells_tag = []
        self.tag_to_coord = {}
        self.coord_to_tag = {}
        self.clicked_tag = "null"
        self.coord_to_piece = {}

        i = 0
        for h in range(
                self.BOARD_OFFSET,
                self.WINDOW_SIZE -
                self.BOARD_OFFSET,
                self.CELL_SIZE):
   
            j = 0
            for v in range(
                    self.BOARD_OFFSET,
                    self.WINDOW_SIZE -
                    self.BOARD_OFFSET,
                    self.CELL_SIZE):

                tag = "{}_{}".format(i, j)
                coord = (h, v, h + self.CELL_SIZE, v + self.CELL_SIZE)
                self.canvas.create_rectangle(*coord, fill="blue", tags=tag)
                self.cells_tag.append(tag)
                self.tag_to_coord[tag] = coord
                self.coord_to_tag[coord] = tag

                if j == 3 and i == 3 or j == 4 and i == 4:
                    self.coord_to_piece[coord] = 1
                    self.canvas.create_oval(*coord, fill="black", tags=tag)

                elif j == 3 and i == 4 or j == 4 and i == 3:
                    self.coord_to_piece[coord] = 2
                    self.canvas.create_oval(*coord, fill="white", tags=tag)
  

                else:
                    self.coord_to_piece[coord] = 0
                j += 1   
            i += 1

        self.canvas.pack()
        for tag in self.cells_tag:
            self.canvas.tag_bind(tag, "<ButtonPress-1>", self.check_click)

    def check_click(self, event):
        for h in range(
                self.BOARD_OFFSET,
                self.WINDOW_SIZE -
                self.BOARD_OFFSET,
                self.CELL_SIZE):
            for v in range(
                    self.BOARD_OFFSET,
                    self.WINDOW_SIZE -
                    self.BOARD_OFFSET,
                    self.CELL_SIZE):
                coord = (h, v, h + self.CELL_SIZE, v + self.CELL_SIZE)
                if h <= event.x <= h + self.CELL_SIZE and v <= event.y <= v + self.CELL_SIZE:
                    self.clicked_tag = self.coord_to_tag[coord]
    
    def choice_attack(self):
        self.describe = tkinter.Label(self.window, text='Mode', bg='#008080', fg='#000000', width=10)
        self.describe.place(x=20, y=self.WINDOW_SIZE + 10)

        # mode_1 (human vs human)
        self.mode_1_button =  tkinter.Button(self.window, text='Human vs Human', bg='#008080', fg='#000000', width=20, command=self.mode_1_clicked)
        self.mode_1_button.place(x=20, y=self.WINDOW_SIZE + 50)

        # mode_2(human vs random)
        self.mode_2_button =  tkinter.Button(self.window, text='Human vs CPU', bg='#008080', fg='#000000', width=20, command=self.mode_2_clicked)
        self.mode_2_button.place(x=200, y=self.WINDOW_SIZE + 50)

        # mode_3(random vs random)
        self.mode_3_button =  tkinter.Button(self.window, text='CPU vs CPU', bg='#008080', fg='#000000', width=20, command=self.mode_3_clicked)
        self.mode_3_button.place(x=380, y=self.WINDOW_SIZE + 50)

    def mode_1_clicked(self):
        self.mode_destory()

        self.players["first"] = "human"
        self.players["second"] = "human"
        self.players["wait"] = "Before the game starts"
    
    def mode_2_clicked(self):
        self.mode_destory()
        self.before_button = tkinter.Button(self.window, text='Going first:Black piece', bg='#008080', fg='#000000', width=20, command=self.before_clicked)
        self.before_button.place(x=20, y=self.WINDOW_SIZE + 20)
        self.after_button = tkinter.Button(self.window, text='Second attack:White piece', bg='#008080', fg='#000000', width=20, command=self.after_clicked)
        self.after_button.place(x=200, y=self.WINDOW_SIZE + 20)
    def mode_3_clicked(self):
        self.mode_destory()

        self.describe = tkinter.Label(self.window, text='Choice strength(Going first)', bg='#008080', fg='#000000', width=25)
        self.describe.place(x=20, y=self.WINDOW_SIZE + 10)

        self.before_computer_1 = tkinter.Button(self.window, text='Weak', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked(0))
        self.before_computer_1.place(x=20, y=self.WINDOW_SIZE + 50)
        
        self.before_computer_2 = tkinter.Button(self.window, text='Little strong', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked(1))
        self.before_computer_2.place(x=200, y=self.WINDOW_SIZE + 50)
        
        self.before_computer_3 = tkinter.Button(self.window, text='Strong', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked(2))
        self.before_computer_3.place(x=380, y=self.WINDOW_SIZE + 50)

    def mode_destory(self):
        self.mode_1_button.destroy()
        self.mode_2_button.destroy()
        self.mode_3_button.destroy()
        self.describe.destroy()
            
    def before_clicked(self):
        self.before_button.destroy()
        self.after_button.destroy()
        self.players["first"] = "human"
        self.after_computer()

    def after_clicked(self):
        self.before_button.destroy()
        self.after_button.destroy()
        self.players["second"] = "human"
        self.before_computer()
    
    def before_computer(self):
        self.describe.destroy()

        self.describe = tkinter.Label(self.window, text='Choice strength(Going first)', bg='#008080', fg='#000000', width=25)
        self.describe.place(x=20, y=self.WINDOW_SIZE + 10)

        self.before_computer_1 = tkinter.Button(self.window, text='Weak', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked_human(0))
        self.before_computer_1.place(x=20, y=self.WINDOW_SIZE + 50)
        
        self.before_computer_2 = tkinter.Button(self.window, text='Little strong', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked_human(1))
        self.before_computer_2.place(x=200, y=self.WINDOW_SIZE + 50)
        
        self.before_computer_3 = tkinter.Button(self.window, text='Strong', bg='#008080', fg='#000000', width=20, command= lambda: self.before_computer_clicked_human(2))
        self.before_computer_3.place(x=380, y=self.WINDOW_SIZE + 50)

    def before_computer_clicked_human(self, id_num):
        if id_num == 0:
            self.players["first"] = "random"
        elif id_num == 1:
            self.players["first"] = "random_2"
        elif id_num == 2:
            self.players["first"] = "random_3"
        
        self.players["wait"] = "Before the game starts"
        self.before_computer_1.destroy()
        self.before_computer_2.destroy()
        self.before_computer_3.destroy()
        self.describe.destroy()

    def before_computer_clicked(self, id_num):        
        if id_num == 0:
            self.players["first"] = "random"

        elif id_num == 1:
            self.players["first"] = "random_2"
        
        elif id_num == 2:
            self.players["first"] = "random_3"
      
        self.before_computer_1.destroy()
        self.before_computer_2.destroy()
        self.before_computer_3.destroy()
        self.after_computer()

    def after_computer(self):
        self.describe.destroy()

        self.describe = tkinter.Label(self.window, text='Choice strength(second attack)', bg='#008080', fg='#000000', width=25)
        self.describe.place(x=20, y=self.WINDOW_SIZE + 10)

        self.after_computer_1 = tkinter.Button(self.window, text='Weak', bg='#008080', fg='#000000', width=20, command= lambda: self.after_computer_clicked(0))
        self.after_computer_1.place(x=20, y=self.WINDOW_SIZE + 50)
        
        self.after_computer_2 = tkinter.Button(self.window, text='Little strong', bg='#008080', fg='#000000', width=20, command= lambda: self.after_computer_clicked(1))
        self.after_computer_2.place(x=200, y=self.WINDOW_SIZE + 50)
    
        self.after_computer_3 = tkinter.Button(self.window, text='Strong', bg='#008080', fg='#000000', width=20, command= lambda: self.after_computer_clicked(2))
        self.after_computer_3.place(x=380, y=self.WINDOW_SIZE + 50)
    
    def after_computer_clicked(self, id_num):
        if id_num == 0:
            self.players["second"] = "random"

        elif id_num == 1:
            self.players["second"] = "random_2"
        
        elif id_num == 2:
            self.players["second"] = "random_3"

        self.players["wait"] = "Before the game starts"
        self.after_computer_1.destroy()
        self.after_computer_2.destroy()
        self.after_computer_3.destroy()
        self.describe.destroy()

    def draw_piece_black(self, coord):
        tag = self.coord_to_tag[coord]
        self.canvas.create_oval(*coord, fill="black", tags=tag)

    def draw_piece_white(self, coord):
        tag = self.coord_to_tag[coord]
        self.canvas.create_oval(*coord, fill="white", tags=tag)

    def draw_avalable_cell(self,coord):
        tag = self.coord_to_tag[coord]
        tag = tag + "arc"
        self.canvas.create_oval(*coord,outline="red", tags=tag)

    def delete_avalable_cell(self,coord):
        tag = self.coord_to_tag[coord]
        tag = tag + "arc"
        self.canvas.delete(tag)
               
    def alert_message_human(self):
        if self.alert_flag == False:
            self.alert = tkinter.Label(self.window, text="Don't hit there", bg='#008080', fg='#000000', width=20)
            self.alert.place(x=300, y=self.WINDOW_SIZE + 20)
            self.alert_flag = True

        else:
            pass    
    def alert_message_random(self):
        if self.alert_flag == False:
            self.alert = tkinter.Label(self.window, text='Thinking', bg='#008080', fg='#000000', width=20)
            self.alert.place(x=300, y=self.WINDOW_SIZE + 20)
            self.alert_flag = True
        else:
            pass

    def alert_pass(self):
        if self.pass_flag_alert == False:
            self.alert_pass_button = tkinter.Button(self.window, text='Pass your turn', bg='#008080', fg='#000000', width=20, command=self.turn_pass)
            self.pass_flag_alert = True
        self.alert_pass_button.place(x=200, y=self.WINDOW_SIZE + 50)
        self.alert_flag = True

    def turn_pass(self):
        self.alert_pass_button.destroy()
        self.alert_flag = False
        self.pass_flag_alert = False
        self.board.change_turn()

    def delete_alert(self):
        self.alert.destroy()
        self.alert_flag = False
      
    def alert_finish(self, board):
        black_count = board.result_count[0]
        white_count = board.result_count[1]
        
        self.alert = tkinter.Label(self.window, text='Finish game', bg='#008080', fg='#000000', width=40)
        if self.restart_flag_alert == False:
            self.alert_restart = tkinter.Button(self.window, text='Play again', bg='#008080', fg='#000000', width=20, command=self.restart_game)
            self.restart_flag_alert = True
        self.result = tkinter.Label(self.window, text="Going fisrt(Black piece):" + str(black_count) + "\n" + "Second attack(White piece):" + str(white_count), bg='#008080', fg='#000000', width=40)

        self.alert.place(x=250, y=self.WINDOW_SIZE + 20)
        self.alert_restart.place(x=20, y=self.WINDOW_SIZE + 50)
        self.result.place(x=250, y=self.WINDOW_SIZE + 40)
    
    def restart_game(self):
        self.restart_flag = True

    def mainloop(self):
        self.window.mainloop()

class Player:
    def __init__(self, *args, **kargs):
        pass

    def __str__(self):
        return 'super player'

    def play(self, board):
        pass

class HumanPlayer(Player):
    def __init__(self, view):
        self.view = view

class RandomPlayer(Player):
    def __init__(self, view):
        self.view = view
        
    def random_hit(self, board):

        for x in range(0,8):
            for y in range(0,8):
                random_tag = str(x) + "_" + str(y)
                coord = self.view.tag_to_coord[random_tag]
                piece_count = board.coord_to_piece[coord]

                board.check_random_hit(coord, self.view)  
      
    def search_hit(self, board):
        for x in range(0,8):
            for y in range(0,8):
                random_tag = str(x) + "_" + str(y)
                coord = self.view.tag_to_coord[random_tag]
                board.check_search_hit(coord, self.view)                        
class Board:
    def __init__(self):
        self.turn = "wait"
        self.count = 0
        self.hit = False
        self.avalable_hit = False
        self.reverse_dic = {}

        self.turn_to_piece = {}
        self.turn_to_piece["first"] = 1
        self.turn_to_piece["second"] = 2

        self.random_hit_list_tag = []
        self.random_hit_list_coord = []
        
        self.search_hit_list_tag = []
        self.search_hit_list_coord = []

        self.pass_count = 0
        self.finish_flag = False 
        self.result_count = []
        self.restart_flag = False
        self.search_flag = False

        self.tag_to_evalvalue = {}
        self.tag_to_evalvalue["0_0"] = 30
        self.tag_to_evalvalue["0_1"] = -12
        self.tag_to_evalvalue["0_2"] = 0
        self.tag_to_evalvalue["0_3"] = -1
        self.tag_to_evalvalue["0_4"] = -1
        self.tag_to_evalvalue["0_5"] = 0
        self.tag_to_evalvalue["0_6"] = -12
        self.tag_to_evalvalue["0_7"] = 30
        self.tag_to_evalvalue["1_0"] = -12
        self.tag_to_evalvalue["1_1"] = -15
        self.tag_to_evalvalue["1_2"] = -3
        self.tag_to_evalvalue["1_3"] = -3
        self.tag_to_evalvalue["1_4"] = -3
        self.tag_to_evalvalue["1_5"] = -3
        self.tag_to_evalvalue["1_6"] = -15
        self.tag_to_evalvalue["1_7"] = -12
        self.tag_to_evalvalue["2_0"] = 0
        self.tag_to_evalvalue["2_1"] = -3
        self.tag_to_evalvalue["2_2"] = 0
        self.tag_to_evalvalue["2_3"] = -1
        self.tag_to_evalvalue["2_4"] = -1
        self.tag_to_evalvalue["2_5"] = 0
        self.tag_to_evalvalue["2_6"] = -3
        self.tag_to_evalvalue["2_7"] = 0
        self.tag_to_evalvalue["3_0"] = -1
        self.tag_to_evalvalue["3_1"] = -3
        self.tag_to_evalvalue["3_2"] = -1
        self.tag_to_evalvalue["3_3"] = -1
        self.tag_to_evalvalue["3_4"] = -1
        self.tag_to_evalvalue["3_5"] = -1
        self.tag_to_evalvalue["3_6"] = -3
        self.tag_to_evalvalue["3_7"] = -1
        self.tag_to_evalvalue["4_0"] = -1
        self.tag_to_evalvalue["4_1"] = -3
        self.tag_to_evalvalue["4_2"] = -1
        self.tag_to_evalvalue["4_3"] = -1
        self.tag_to_evalvalue["4_4"] = -1
        self.tag_to_evalvalue["4_5"] = -1
        self.tag_to_evalvalue["4_6"] = -3
        self.tag_to_evalvalue["4_7"] = -1
        self.tag_to_evalvalue["5_0"] = 0
        self.tag_to_evalvalue["5_1"] = -3
        self.tag_to_evalvalue["5_2"] = 0
        self.tag_to_evalvalue["5_3"] = -1
        self.tag_to_evalvalue["5_4"] = -1
        self.tag_to_evalvalue["5_5"] = 0
        self.tag_to_evalvalue["5_6"] = -3
        self.tag_to_evalvalue["5_7"] = 0
        self.tag_to_evalvalue["6_0"] = -12
        self.tag_to_evalvalue["6_1"] = -15
        self.tag_to_evalvalue["6_2"] = -3
        self.tag_to_evalvalue["6_3"] = -3
        self.tag_to_evalvalue["6_4"] = -3
        self.tag_to_evalvalue["6_5"] = -3
        self.tag_to_evalvalue["6_6"] = -15
        self.tag_to_evalvalue["6_7"] = -12
        self.tag_to_evalvalue["7_0"] = 30
        self.tag_to_evalvalue["7_1"] = -12
        self.tag_to_evalvalue["7_2"] = 0
        self.tag_to_evalvalue["7_3"] = -1
        self.tag_to_evalvalue["7_4"] = -1
        self.tag_to_evalvalue["7_5"] = 0
        self.tag_to_evalvalue["7_6"] = -12
        self.tag_to_evalvalue["7_7"] = 30

    def check_avalable_hit(self, coord, view):

        x = 0
        y = 0
        if self.coord_to_piece.get(coord) != "default":
            if self.coord_to_piece[coord] == 0:
                tag = view.coord_to_tag[coord]
                x = tag.split("_")[0]
                y = tag.split("_")[1]
        self.check_piece_around(int(x), int(y), view)
    def check_random_hit(self, coord, view):
        x = 0
        y = 0
        if self.coord_to_piece.get(coord) != "default":
            if self.coord_to_piece[coord] == 0:
                tag = view.coord_to_tag[coord]
                x = tag.split("_")[0]
                y = tag.split("_")[1]
                self.check_piece_around(int(x), int(y), view)
    def check_search_hit(self, coord, view):
        x = 0
        y = 0
        if self.coord_to_piece.get(coord) != "default":
            if self.coord_to_piece[coord] == 0:
                tag = view.coord_to_tag[coord]
                x = tag.split("_")[0]
                y = tag.split("_")[1]
                self.check_search_around(int(x), int(y), view)
    
    def check_search_around(self, x, y, view):

        if self.turn == "first":
            my_color_num = 1
        elif self.turn == "second":
            my_color_num = 2
        else:
            my_color_num = 0    
        for dx in range(-1,2,1):  
            for dy in range(-1,2,1):
                if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
                    if not (dx == 0 and dy == 0):

                        maked_tag = str(x + dx) + "_" + str(y + dy) 
                        piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
                        if piece_color_num == 0 :
                            pass
                        elif piece_color_num == my_color_num:
                            pass       
                        elif piece_color_num != my_color_num:
                            hit_flag = self.check_search_around_2(x + dx, y + dy, dx, dy, view)
                            if hit_flag:
                                self.search_hit_list_tag.append(str(x) + "_" + str(y))               
    
    def check_search_around_2(self,x,y,dx,dy,view):
        if self.turn == "first":
            my_color_num = 1
        elif self.turn == "second":
            my_color_num = 2
        else:
            my_color_num = 0    

        if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
            maked_tag = str(x + dx) + "_" + str(y + dy)
            piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
            if piece_color_num == 0 :
                pass               
            elif piece_color_num == my_color_num:
                return True
   
            elif piece_color_num != my_color_num:
                return self.check_search_around_2(x + dx, y + dy, dx, dy, view)
                
    def check_piece_around(self, x, y, view):

        avalable_flag = False
        if self.turn == "first":
            my_color_num = 1
        elif self.turn == "second":
            my_color_num = 2
        else:
            my_color_num = 0    
  
        for dx in range(-1,2,1):  
            for dy in range(-1,2,1):
                if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
                    if not (dx == 0 and dy == 0):
                        maked_tag = str(x + dx) + "_" + str(y + dy) 
                        piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
                        if piece_color_num == 0 :
                            pass
                        elif piece_color_num == my_color_num:
                            pass       
                        elif piece_color_num != my_color_num:
                            hit_flag = self.check_piece_around_2(x + dx, y + dy, dx, dy, view)
                            if hit_flag:
                                self.random_hit_list_tag.append(str(x) + "_" + str(y)) 

                else:
                    pass               
    def check_piece_around_2(self,x,y,dx,dy,view):
        if self.turn == "first":
            my_color_num = 1
        elif self.turn == "second":
            my_color_num = 2
        else:
            my_color_num = 0    

        if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
  
            maked_tag = str(x + dx) + "_" + str(y + dy)
            piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]
            if piece_color_num == 0 :
                pass                
            elif piece_color_num == my_color_num:
                self.avalable_hit = True
                return True
    
            elif piece_color_num != my_color_num:
                return self.check_piece_around_2(x + dx, y + dy, dx, dy, view)
  
    def dohit(self, coord):
        if self.turn == "first":
            self.coord_to_piece[coord] = 1
               
        else:
            self.coord_to_piece[coord] = 2
    
    def reverse_piece(self,coord,view):
        tag = view.coord_to_tag[coord]
        x = int(tag.split("_")[0])
        y = int(tag.split("_")[1])
        self.reverse_piece_around(int(x), int(y), view)
        for finish_point, dx_dy in self.reverse_dic.items():
            dx = int(dx_dy.split("_")[0])
            dy = int(dx_dy.split("_")[1])
            finish_x = int(finish_point.split("_")[0])
            finish_y = int(finish_point.split("_")[1])
        
            reverse_x = x + dx
            reverse_y = y + dy
            count = 1
            while(reverse_x != finish_x or reverse_y != finish_y):
                reverse_x = x + dx * count
                reverse_y = y + dy * count
                reverse_tag = str(reverse_x) + "_" + str(reverse_y)

                self.coord_to_piece[view.tag_to_coord[reverse_tag]] = self.turn_to_piece[self.turn]
                if self.turn == "first":
                    view.draw_piece_black(view.tag_to_coord[reverse_tag])
                elif self.turn == "second":
                    view.draw_piece_white(view.tag_to_coord[reverse_tag])
                count += 1    
 
    def reverse_piece_around(self, x, y, view):
        if self.turn == "first":
            my_color_num = 1
        elif self.turn == "second":
            my_color_num = 2

        for dx in range(-1,2,1):  
            for dy in range(-1,2,1):
                if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:
                    if not (dx == 0 and dy == 0):

                        maked_tag = str(x + dx) + "_" + str(y + dy) 
                        piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]   
                        if piece_color_num != my_color_num and piece_color_num != 0:
                            self.reverse_piece_around_2(x + dx, y + dy, dx, dy, view)
                else:
                    pass               
    
    def reverse_piece_around_2(self,x,y,dx,dy,view):
        if self.turn == "first":
            my_color_num = 1
        elif self.turn == "second":
            my_color_num = 2
        if x + dx != -1 and x + dx != 8 and y + dy != -1 and y + dy != 8:

            maked_tag = str(x + dx) + "_" + str(y + dy) 
            piece_color_num = self.coord_to_piece[view.tag_to_coord[maked_tag]]             
            if piece_color_num == my_color_num:
                dx_dy = str(dx) + "_" + str(dy)
                self.reverse_dic[maked_tag] = dx_dy
  
            elif piece_color_num != my_color_num and piece_color_num != 0:
                return self.reverse_piece_around_2(x + dx, y + dy, dx, dy, view)

    def change_turn(self):
        if self.turn == "first":
            self.turn = "second"    
        elif self.turn == "second":
            self.turn = "first"
        self.hit = False 
        self.avalable_hit = False
        self.reverse_dic = {}
        self.search_flag = False
        self.result_write_flag = False

    def finish_game(self):
        finish_flag = True

        for count in self.coord_to_piece.values():
            if count == 0:
                finish_flag = False

        self.finish_flag = finish_flag

    def get_result(self,view):
        black_count = 0
        white_count = 0
 
        for piece in self.coord_to_piece.values():
            if piece == 1:
                black_count += 1
            elif piece == 2:
                white_count += 1
        
        result_count = [black_count,white_count]
        self.result_count = result_count
        
        first_player = view.players["first"]
        second_player = view.players["second"]
        
        result_message = "first: " + first_player + ": " + str(black_count) + ", "
        result_message += "second: " + second_player + ": " + str(white_count) + "\n"
        
      
def play_othello():
    othello = Othello()
    othello.play_game()

if __name__ == "__main__":
    play_othello()
