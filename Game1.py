import tkinter as tk
import math
import winsound

board = [" " for _ in range(9)]
buttons = []
game_over = False

# Score
player_score = 0
ai_score = 0
draw_score = 0

# Colors
BG_COLOR = "#1e1e2f"
BTN_COLOR = "#2d2d44"
HOVER_COLOR = "#3e3e5c"
TEXT_COLOR = "#ffffff"
X_COLOR = "#4cc9f0"
O_COLOR = "#f72585"

def play_click_sound():
    winsound.Beep(600, 100)

def play_win_sound():
    winsound.Beep(1000, 200)

def check_winner(b, player):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    return any(b[a]==b[b1]==b[c]==player for a,b1,c in wins)

def empty_cells(b):
    return [i for i in range(9) if b[i] == " "]

def minimax(b, is_max):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if not empty_cells(b):
        return 0

    if is_max:
        best = -math.inf
        for i in empty_cells(b):
            b[i] = "O"
            best = max(best, minimax(b, False))
            b[i] = " "
        return best
    else:
        best = math.inf
        for i in empty_cells(b):
            b[i] = "X"
            best = min(best, minimax(b, True))
            b[i] = " "
        return best

def ai_move():
    global game_over
    best_score = -math.inf
    move = None

    for i in empty_cells(board):
        board[i] = "O"
        score = minimax(board, False)
        board[i] = " "
        if score > best_score:
            best_score = score
            move = i

    if move is not None:
        board[move] = "O"
        buttons[move].config(text="O", fg=O_COLOR)
        play_click_sound()

    check_game_end()

def click(i):
    global game_over
    if board[i] == " " and not game_over:
        board[i] = "X"
        buttons[i].config(text="X", fg=X_COLOR)
        play_click_sound()

        if not check_game_end():
            ai_move()

def check_game_end():
    global game_over, player_score, ai_score, draw_score

    if check_winner(board, "X"):
        status.config(text="🎉 You Win!")
        player_score += 1
        play_win_sound()
        game_over = True

    elif check_winner(board, "O"):
        status.config(text="🤖 AI Wins!")
        ai_score += 1
        play_win_sound()
        game_over = True

    elif not empty_cells(board):
        status.config(text="😐 Draw!")
        draw_score += 1
        game_over = True

    update_score()
    return game_over

def update_score():
    score_label.config(
        text=f"You: {player_score} | AI: {ai_score} | Draw: {draw_score}"
    )

def restart_game():
    global board, game_over
    board = [" " for _ in range(9)]
    game_over = False
    status.config(text="Your Turn")

    for btn in buttons:
        btn.config(text=" ", fg=TEXT_COLOR)

def on_enter(e):
    e.widget['bg'] = HOVER_COLOR

def on_leave(e):
    e.widget['bg'] = BTN_COLOR

# GUI
root = tk.Tk()
root.title("Tic Tac Toe AI")
root.configure(bg=BG_COLOR)

frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(pady=10)

for i in range(9):
    btn = tk.Button(frame, text=" ", font=("Arial", 24, "bold"),
                    width=5, height=2, bg=BTN_COLOR, fg=TEXT_COLOR,
                    activebackground=HOVER_COLOR, bd=0,
                    command=lambda i=i: click(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    buttons.append(btn)

status = tk.Label(root, text="Your Turn", font=("Arial", 16),
                  bg=BG_COLOR, fg=TEXT_COLOR)
status.pack(pady=10)

score_label = tk.Label(root, text="You: 0 | AI: 0 | Draw: 0",
                       font=("Arial", 14),
                       bg=BG_COLOR, fg="#ffd166")
score_label.pack()

restart_btn = tk.Button(root, text="Restart 🔄", font=("Arial", 12, "bold"),
                        bg="#06d6a0", fg="black", padx=10, pady=5,
                        command=restart_game)
restart_btn.pack(pady=10)

root.mainloop()