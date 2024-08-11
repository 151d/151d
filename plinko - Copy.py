import tkinter as tk
import random

class PlinkoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Plinko Game - Two Player Mode")
        
        # Set up game variables
        self.slots = 9
        self.rows = 12
        self.current_player = 1
        self.scores = {1: 0, 2: 0}

        # Create the board
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=20)
        self.create_board()

        # Player label and score
        self.player_label = tk.Label(self.root, text="Player 1's turn", font=("Arial", 16))
        self.player_label.pack()

        self.score_label = tk.Label(self.root, text="Player 1: 0 | Player 2: 0", font=("Arial", 14))
        self.score_label.pack()

        # Drop button
        self.drop_button = tk.Button(self.root, text="Drop", command=self.drop_disc, font=("Arial", 14))
        self.drop_button.pack(pady=20)

    def create_board(self):
        self.board = []
        for i in range(self.rows):
            row = []
            for j in range(self.slots):
                cell = tk.Label(self.board_frame, text="O", width=4, height=2, borderwidth=1, relief="solid")
                cell.grid(row=i, column=j)
                row.append(cell)
            self.board.append(row)
        self.slot_labels = []
        for j in range(self.slots):
            slot_label = tk.Label(self.board_frame, text=f"{j}", width=4, height=2, borderwidth=1, relief="ridge", bg="lightgray")
            slot_label.grid(row=self.rows, column=j)
            self.slot_labels.append(slot_label)

    def drop_disc(self):
        position = self.slots // 2  # Start in the middle
        for row in range(self.rows):
            self.root.update()
            self.board[row][position].config(bg="yellow")
            self.root.after(200)
            self.board[row][position].config(bg="white")
            move = random.choice([-1, 1])  # Move left or right
            position += move
            position = max(0, min(self.slots - 1, position))

        self.update_score(position)
        self.switch_player()

    def update_score(self, position):
        points = [100, 500, 1000, 0, 10000, 0, 1000, 500, 100]
        score = points[position]
        self.scores[self.current_player] += score
        self.score_label.config(text=f"Player 1: {self.scores[1]} | Player 2: {self.scores[2]}")
        self.slot_labels[position].config(bg="yellow")

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
        self.player_label.config(text=f"Player {self.current_player}'s turn")
        self.slot_labels[position].config(bg="lightgray")

if __name__ == "__main__":
    root = tk.Tk()
    game = PlinkoGame(root)
    root.mainloop()
