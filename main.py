from tkinter import *
rows, cols = 65, 65

# Function to start the game after entering player names
def start_game():
    global player1_name, player2_name
    player1_name = player1_entry.get()
    player2_name = player2_entry.get()
    
    if player1_name and player2_name:
        setup_frame.pack_forget()
        game_frame.pack()

        l1.config(text=f"{player1_name} vs {player2_name}")
        l2.config(text=f"{player1_name}: 0")
        l3.config(text=f"{player2_name}: 0")
        l4.config(text=f"{player1_name}'s TURN !!!", fg="blue")
    else:
        error_label.config(text="Please enter both player names")

# Function to restart the game
def restart_game():
    global matrix, queue, user, flag, red_count, blue_count
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    queue = []
    user = 1
    flag = [0, 0]
    red_count = 0
    blue_count = 0

    can_widget.delete("all")
    for i in range(3):
        for j in range(3):
            can_widget.create_oval(offset * i + margin,
                                   offset * j + margin,
                                   offset * i + margin + dotsize,
                                   offset * j + margin + dotsize,
                                   fill="black")
    l2.config(text=f"{player1_name}: 0")
    l3.config(text=f"{player2_name}: 0")
    l4.config(text=f"{player1_name}'s TURN !!!", fg="blue")

# select user chance
def user_chance(event):
    global user
    change = 0
    x_coordinate = event.x
    y_coordinate = event.y
    for i in range(3):
        for j in range(3):
            if y_coordinate >= offset * i + margin - 2 and y_coordinate <= offset * i + margin + dotsize + 2:
                if x_coordinate >= offset * j + margin + dotsize / 2 and x_coordinate <= offset * (j + 1) + margin + dotsize / 2 and j != 7:
                    dot_1 = j + i * 8 + 1
                    dot_2 = j + i * 8 + 2
                    change = 1
            if x_coordinate >= offset * i + margin - 2 and x_coordinate <= offset * i + margin + dotsize + 2:
                if y_coordinate >= offset * j + margin + dotsize / 2 and y_coordinate <= offset * (j + 1) + margin + dotsize / 2 and j != 7:
                    dot_1 = i + j * 8 + 1
                    dot_2 = i + j * 8 + 9
                    change = 1
    if change != 0 and matrix[dot_1][dot_2] != 1:
        if user == 1:
            l4.config(text=f"{player2_name}'s TURN !!!", fg="red")
            l4.pack()
        else:
            l4.config(text=f"{player1_name}'s TURN !!!", fg="blue")
            l4.pack()
        make_line(x_coordinate, y_coordinate)

# make lines between dots
def make_line(x_coordinate, y_coordinate):
    global user, change
    change = 0
    m = 0
    for i in range(3):
        for j in range(3):
            if y_coordinate >= offset * i + margin - 2 and y_coordinate <= offset * i + margin + dotsize + 2:
                if x_coordinate >= offset * j + margin + dotsize / 2 and x_coordinate <= offset * (j + 1) + margin + dotsize / 2 and j != 7:
                    can_widget.create_line(offset * j + margin + dotsize / 2,
                                           offset * i + margin + dotsize / 2,
                                           offset * (j + 1) + margin + dotsize / 2,
                                           offset * i + margin + dotsize / 2)
                    dot_1 = j + i * 8 + 1
                    dot_2 = j + i * 8 + 2
                    m = m + 1
                    break
            if x_coordinate >= offset * i + margin - 2 and x_coordinate <= offset * i + margin + dotsize + 2:
                if y_coordinate >= offset * j + margin + dotsize / 2 and y_coordinate <= offset * (j + 1) + margin + dotsize / 2 and j != 7:
                    can_widget.create_line(offset * i + margin + dotsize / 2,
                                           offset * j + margin + dotsize / 2,
                                           offset * i + margin + dotsize / 2,
                                           offset * (j + 1) + margin + dotsize / 2)
                    dot_1 = i + j * 8 + 1
                    dot_2 = i + j * 8 + 9
                    m = m + 1
                    break
        if m != 0:
            break
    if m != 0:
        if flag[user - 1] == 1:
            flag[user - 1] = 0
        if user == 1:
            user = 2
        else:
            user = 1
        check_box(dot_1, dot_2)

# check if box is formed or not
def check_box(x, y):
    matrix[x][y] = 1
    matrix[y][x] = 1
    diff = y - x
    if diff == 1:
        opposite = -8
        traverse(diff, opposite, x, y)
        opposite = 8
        traverse(diff, opposite, x, y)
    elif diff == 8:
        opposite = -1
        traverse(diff, opposite, x, y)
        opposite = 1
        traverse(diff, opposite, x, y)

# for traversing the path
def traverse(a, b, c, d):
    global user
    m = 0
    queue.append(c)
    X = c + b
    if X > 0 and X < 65:
        if matrix[c][X] == 1:
            queue.append(X)
            if matrix[X][X + a] == 1:
                X = X + a
                queue.append(X)
                if matrix[X][X - b] == 1:
                    X = X - b
                    queue.append(X)
                    m = 1
    if m == 1:
        if user == 1:
            user = 2
        else:
            user = 1
        if user == 1:
            l4.config(text=f"{player1_name}'s TURN !!!", fg="blue")
            l4.pack()
        else:
            l4.config(text=f"{player2_name}'s TURN !!!", fg="red")
            l4.pack()
        flag[user - 1] = 0
        user_color()

    del queue[0:]

    check_endgame()

# color the user boxes and update scores
def user_color():
    global red_count, blue_count
    a = queue[3]
    b = queue[1]
    if user == 1:
        color = "SteelBlue2"
        blue_count += 1
        l2.config(text=f"{player1_name}: {blue_count}")
        l2.pack()
    else:
        color = "firebrick1"
        red_count += 1
        l3.config(text=f"{player2_name}: {red_count}")
        l3.pack()
    if a % 8 != 0:
        x1 = (a % 8 - 1) * offset + margin + dotsize / 2
    else:
        x1 = 7 * offset + margin + dotsize / 2
    y1 = int(a / 8.1) * offset + margin + dotsize / 2
    if b % 8 != 0:
        x2 = (b % 8 - 1) * offset + margin + dotsize / 2
    else:
        x2 = 7 * offset + margin + dotsize / 2
    y2 = int(b / 8.1) * offset + margin + dotsize / 2
    can_widget.create_rectangle(x1, y1, x2, y2, fill=color)

# check if the game has ended
def check_endgame():
    global blue_count, red_count
    total_boxes = blue_count + red_count
    if total_boxes == 4:  # since it's a 2x2 grid of boxes
        if blue_count > red_count:
            result = f"{player1_name} wins!"
        elif red_count > blue_count:
            result = f"{player2_name} wins!"
        else:
            result = "TIE!!!!!"
        l4.config(text=result, fg="black")
        l4.pack()

# Initial Setup
root = Tk()
root.geometry("600x450")
root.resizable(width=False, height=False)
root.title("Dots and Boxes - (Game)")

# Frames
setup_frame = Frame(root)
setup_frame.pack()

game_frame = Frame(root)

# Player Name Entries
Label(setup_frame, text="Enter Player 1 Name:").pack(pady=5)
player1_entry = Entry(setup_frame)
player1_entry.pack(pady=5)

Label(setup_frame, text="Enter Player 2 Name:").pack(pady=5)
player2_entry = Entry(setup_frame)
player2_entry.pack(pady=5)

error_label = Label(setup_frame, text="", fg="red")
error_label.pack(pady=5)

Button(setup_frame, text="Start Game", command=start_game).pack(pady=20)

# Game Canvas and Labels
canvas_width = 600
canvas_height = 500
offset = 150
margin = 50
dotsize = 10

f1 = Frame(game_frame, bg="coral", borderwidth=5, relief=SUNKEN)
f1.pack(side=RIGHT, padx=5, pady=5, fill="y", anchor=NE)

f2 = Frame(game_frame, bg="OliveDrab1", borderwidth=5, relief=RIDGE)
f2.pack(side=TOP, padx=5, fill="x", anchor=N)

l4 = Label(f2, text="PLAYER 1 TURN !!!", font="Verdana 10", fg="blue", bg="OliveDrab1")
l4.pack(padx=10)

l1 = Label(f1, text="Players:-", font="Verdana 20 bold", fg="white", bg="coral", padx=10)
l1.pack(pady=20)

score1 = "Player 1: 0"
l2 = Label(f1, text=score1, font="Verdana 12", borderwidth=5, relief="ridge", fg="blue", bg="azure2", padx=3, pady=3)
l2.pack(pady=15)

score2 = "Player 2: 0"
l3 = Label(f1, text=score2, font="Verdana 12", borderwidth=5, relief="ridge", fg="red", bg="azure2", padx=3, pady=3)
l3.pack(pady=15)

Button(f1, text="Restart Game", command=restart_game).pack(pady=20)

# create canvas
can_widget = Canvas(game_frame, width=canvas_width, height=canvas_height, bg="azure2", borderwidth=3, relief=SOLID)
can_widget.pack(pady=5, padx=5)

# Bind canvas
can_widget.bind("<Button-1>", user_chance)

# dots plotting
for i in range(3):
    for j in range(3):
        can_widget.create_oval(offset * i + margin,
                               offset * j + margin,
                               offset * i + margin + dotsize,
                               offset * j + margin + dotsize,
                               fill="black")

root.mainloop()
