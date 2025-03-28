import tkinter as tk
import random
from tkinter import messagebox

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("400x550")
root.configure(bg="white")

# Biến toàn cục
player = "X"
mode = "PvP"
difficulty = "Dễ"
board = [""] * 9
buttons = []
scores = {"PvP": {"X": 0, "O": 0}, "PvE": {"Player": 0, "AI": 0}}

def update_score():
    if mode == "PvP":
        score_label.config(text=f"PvP - X: {scores['PvP']['X']} | O: {scores['PvP']['O']}")
    else:
        score_label.config(text=f"PvE - Player: {scores['PvE']['Player']} | AI: {scores['PvE']['AI']}")

def check_winner():
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for (i, j, k) in win_conditions:
        if board[i] == board[j] == board[k] and board[i] != "":
            return board[i]
    return None

def handle_winner(winner):
    if mode == "PvP":
        scores["PvP"][winner] += 1
    else:
        if winner == "X":
            scores["PvE"]["Player"] += 1
        else:
            scores["PvE"]["AI"] += 1
    messagebox.showinfo("Kết quả", f"Người chơi {winner} thắng!")
    reset_board()
    update_score()

def on_click(index):
    global player
    if board[index] == "":
        board[index] = player
        buttons[index].config(text=player, state="disabled")
        winner = check_winner()
        if winner:
            handle_winner(winner)
            return
        if "" not in board:
            messagebox.showinfo("Kết quả", "Trò chơi hòa!")
            reset_board()
            return
        player = "O" if player == "X" else "X"
        if mode == "PvE" and player == "O":
            root.after(500, ai_move)

def ai_move():
    if difficulty == "Dễ":
        empty_cells = [i for i in range(9) if board[i] == ""]
        if empty_cells:
            on_click(random.choice(empty_cells))
    elif difficulty == "Vừa":
        best_move = find_best_move()
        if best_move is not None:
            on_click(best_move)
    elif difficulty == "Khó":
        best_move = minimax(board, "O")[1]
        if best_move is not None:
            on_click(best_move)
    winner = check_winner()
    if winner:
        handle_winner(winner)

def find_best_move():
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner() == "O":
                board[i] = ""
                return i
            board[i] = "X"
            if check_winner() == "X":
                board[i] = ""
                return i
            board[i] = ""
    empty_cells = [i for i in range(9) if board[i] == ""]
    return random.choice(empty_cells) if empty_cells else None

def minimax(state, current_player):
    winner = check_winner()
    if winner == "O":
        return (1, None)
    if winner == "X":
        return (-1, None)
    if "" not in state:
        return (0, None)
    best = (-2, None) if current_player == "O" else (2, None)
    for i in range(9):
        if state[i] == "":
            state[i] = current_player
            score, _ = minimax(state, "X" if current_player == "O" else "O")
            state[i] = ""
            if current_player == "O":
                if score > best[0]:
                    best = (score, i)
            else:
                if score < best[0]:
                    best = (score, i)
    return best

def reset_board():
    global board, player
    board = [""] * 9
    player = "X"
    for btn in buttons:
        btn.config(text="", state="normal")

def change_mode(new_mode):
    global mode
    mode = new_mode
    mode_selection_frame.pack_forget()
    game_frame.pack()
    if mode == "PvE":
        difficulty_label.pack(pady=10)
        difficulty_button.pack()
    update_score()
    reset_board()

def change_difficulty(new_difficulty):
    global difficulty
    difficulty = new_difficulty
    difficulty_label.config(text=f"Độ khó: {difficulty}")
    reset_board()

def start_game():
    start_frame.pack_forget()
    mode_selection_frame.pack()

def back_to_mode_selection():
    game_frame.pack_forget()
    mode_selection_frame.pack()

# Tạo frame cho giao diện bắt đầu
start_frame = tk.Frame(root, bg="white")
start_frame.pack(fill="both", expand=True)

title_label = tk.Label(start_frame, text="Tic Tac Toe", font=("Arial", 30), bg="white")
title_label.pack(pady=50)

subtitle_label = tk.Label(start_frame, text="Game hay nhất năm 2025", font=("Arial", 14), fg="gray", bg="white")
subtitle_label.pack(pady=10)

start_button = tk.Button(start_frame, text="Bắt đầu", font=("Arial", 20), command=start_game, bg="lightgray", fg="black")
start_button.pack(pady=20)

# Tạo frame cho giao diện chọn chế độ
mode_selection_frame = tk.Frame(root, bg="white")

mode_label = tk.Label(mode_selection_frame, text="Chọn chế độ chơi", font=("Arial", 20), bg="white")
mode_label.pack(pady=20)

pvp_button = tk.Button(mode_selection_frame, text="PvP", font=("Arial", 16), width=10, command=lambda: change_mode("PvP"), bg="lightgray", fg="black")
pvp_button.pack(pady=10)

pve_button = tk.Button(mode_selection_frame, text="PvE", font=("Arial", 16), width=10, command=lambda: change_mode("PvE"), bg="lightgray", fg="black")
pve_button.pack(pady=10)

# Tạo frame cho giao diện chơi game
game_frame = tk.Frame(root, bg="white")

score_label = tk.Label(game_frame, text="PvP - X: 0 | O: 0", font=("Arial", 14), bg="white")
score_label.pack(pady=10)

frame = tk.Frame(game_frame, bg="black")
frame.pack()
for i in range(3):
    for j in range(3):
        index = i * 3 + j
        btn = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2,
                        command=lambda idx=index: on_click(idx), bg="lightgray", fg="black")
        btn.grid(row=i, column=j, padx=2, pady=2)
        buttons.append(btn)

mode_label = tk.Label(game_frame, text="Chế độ: PvP", font=("Arial", 12), bg="white")
mode_label.pack(pady=10)

back_button = tk.Button(game_frame, text="Quay lại", font=("Arial", 12), command=back_to_mode_selection, bg="lightgray", fg="black")
back_button.pack(pady=10)

difficulty_label = tk.Label(game_frame, text="Độ khó: Dễ", font=("Arial", 12), bg="white")
difficulty_button = tk.Button(game_frame, text="Chọn độ khó", font=("Arial", 12), command=lambda: show_difficulty_options(), bg="lightgray", fg="black")

def show_difficulty_options():
    difficulty_window = tk.Toplevel(root)
    difficulty_window.title("Chọn độ khó")
    difficulty_window.geometry("200x150")
    difficulty_window.configure(bg="white")

    easy_button = tk.Button(difficulty_window, text="Dễ", font=("Arial", 12), width=10, command=lambda: [change_difficulty("Dễ"), difficulty_window.destroy()], bg="lightgray", fg="black")
    easy_button.pack(pady=10)

    medium_button = tk.Button(difficulty_window, text="Vừa", font=("Arial", 12), width=10, command=lambda: [change_difficulty("Vừa"), difficulty_window.destroy()], bg="lightgray", fg="black")
    medium_button.pack(pady=10)

    hard_button = tk.Button(difficulty_window, text="Khó", font=("Arial", 12), width=10, command=lambda: [change_difficulty("Khó"), difficulty_window.destroy()], bg="lightgray", fg="black")
    hard_button.pack(pady=10)

root.mainloop()