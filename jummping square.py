import tkinter as tk
import random

class JumpingSquareGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jumping Square Game")
        self.root.geometry("800x600")
        self.full_screen = False
        self.score = 0
        self.create_main_menu()

    def toggle_full_screen(self, event=None):
        self.full_screen = not self.full_screen
        self.root.attributes("-fullscreen", self.full_screen)
        if self.full_screen:
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        else:
            self.root.geometry("800x600")

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(self.main_menu_frame, text="Welcome to the Jumping Square Game!", font=("Arial", 20))
        self.title_label.pack(pady=20)

        self.start_button = tk.Button(self.main_menu_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(self.main_menu_frame, text="Quit", command=self.quit_game)
        self.quit_button.pack(pady=10)

    def start_game(self):
        self.main_menu_frame.pack_forget()
        self.create_game_window()

    def quit_game(self):
        self.root.quit()

    def create_game_window(self):
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.game_frame, width=800, height=600, bg='black')
        self.canvas.pack()

        self.player_size = 50
        self.player = self.canvas.create_rectangle(375, 500, 425, 550, fill="white")
        self.mouth = self.canvas.create_rectangle(385, 525, 415, 540, fill="black")
        self.tongue = self.canvas.create_rectangle(400, 550, 400, 550, fill="red")

        self.star_size = 30
        self.star = self.create_new_star()

        self.enemy_size = 50
        self.enemy = self.create_new_enemy()

        self.score_label = tk.Label(self.game_frame, text=f"Score: {self.score}", font=("Arial", 14), fg="blue")
        self.score_label.place(x=10, y=10)

        self.instructions_label = tk.Label(self.game_frame, text="Use W to Jump, A to Move Left, D to Move Right, S to Fly, E to Stop Flying", font=("Arial", 12), fg="white")
        self.instructions_label.pack(pady=10)

        self.root.bind("<KeyPress-w>", self.jump)
        self.root.bind("<KeyPress-a>", self.move_left)
        self.root.bind("<KeyPress-d>", self.move_right)
        self.root.bind("<KeyPress-s>", self.fly)
        self.root.bind("<KeyPress-e>", self.stop_flying)
        self.root.bind("<F11>", self.toggle_full_screen)

        self.game_loop()

    def game_loop(self):
        if self.score >= 5:
            self.display_win_message()
            return

        self.move_star()
        self.move_enemy()
        self.check_collision_with_star()
        self.check_collision_with_enemy()
        self.score_label.config(text=f"Score: {self.score}")
        self.root.after(100, self.game_loop)

    def move_left(self, event):
        self.canvas.move(self.player, -20, 0)

    def move_right(self, event):
        self.canvas.move(self.player, 20, 0)

    def jump(self, event):
        current_coords = self.canvas.coords(self.player)
        if current_coords[1] == 500:
            self.animate_jump()

    def animate_jump(self):
        self.open_mouth()
        for _ in range(10):
            self.canvas.move(self.player, 0, -5)
            self.canvas.move(self.mouth, 0, -5)
            self.canvas.move(self.tongue, 0, -5)
            self.root.update()

        self.root.after(100)

        for _ in range(10):
            self.canvas.move(self.player, 0, 5)
            self.canvas.move(self.mouth, 0, 5)
            self.canvas.move(self.tongue, 0, 5)
            self.root.update()

        self.check_collision_with_star()

    def open_mouth(self):
        self.canvas.coords(self.mouth, 385, 525, 415, 540)
        self.canvas.coords(self.tongue, 400, 550, 400, 600)

    def check_collision_with_star(self):
        player_coords = self.canvas.coords(self.player)
        star_coords = self.canvas.coords(self.star)

        if (player_coords[2] > star_coords[0] and player_coords[0] < star_coords[2] and
            player_coords[3] > star_coords[1] and player_coords[1] < star_coords[3]):
            self.canvas.delete(self.star)
            self.star = self.create_new_star()
            self.score += 1

    def move_star(self):
        player_coords = self.canvas.coords(self.player)
        star_coords = self.canvas.coords(self.star)

        if player_coords[0] < star_coords[0]:
            self.canvas.move(self.star, -5, 0)
        elif player_coords[0] > star_coords[0]:
            self.canvas.move(self.star, 5, 0)
        if player_coords[1] < star_coords[1]:
            self.canvas.move(self.star, 0, -5)
        elif player_coords[1] > star_coords[1]:
            self.canvas.move(self.star, 0, 5)

    def create_new_star(self):
        x = random.randint(100, 700)
        y = random.randint(100, 500)
        return self.canvas.create_oval(x, y, x + self.star_size, y + self.star_size, fill="yellow")

    def move_enemy(self):
        player_coords = self.canvas.coords(self.player)
        enemy_coords = self.canvas.coords(self.enemy)

        if player_coords[0] < enemy_coords[0]:
            self.canvas.move(self.enemy, -5, 0)
        elif player_coords[0] > enemy_coords[0]:
            self.canvas.move(self.enemy, 5, 0)
        if player_coords[1] < enemy_coords[1]:
            self.canvas.move(self.enemy, 0, -5)
        elif player_coords[1] > enemy_coords[1]:
            self.canvas.move(self.enemy, 0, 5)

    def create_new_enemy(self):
        x = random.randint(100, 700)
        y = random.randint(100, 500)
        return self.canvas.create_rectangle(x, y, x + self.enemy_size, y + self.enemy_size, fill="red")

    def check_collision_with_enemy(self):
        player_coords = self.canvas.coords(self.player)
        enemy_coords = self.canvas.coords(self.enemy)

        if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and
            player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
            self.respawn_player()

    def respawn_player(self):
        self.canvas.coords(self.player, 375, 500, 425, 550)
        self.score = 0

    def fly(self, event):
        self.canvas.move(self.player, 0, -10)

    def stop_flying(self, event):
        self.canvas.move(self.player, 0, 10)

    def display_win_message(self):
        win_window = tk.Toplevel(self.root)
        win_window.title("Victory!")
        win_window.geometry("400x200")
        win_window.configure(bg="black")

        msg = tk.Label(win_window, text="You Win!", font=("Arial", 24), fg="white", bg="black")
        msg.pack(pady=30)

        play_again_btn = tk.Button(win_window, text="Play Again", command=lambda: self.restart_game(win_window))
        play_again_btn.pack(pady=10)

        quit_btn = tk.Button(win_window, text="Quit", command=self.root.quit)
        quit_btn.pack()

    def restart_game(self, win_window):
        win_window.destroy()
        self.game_frame.destroy()
        self.score = 0
        self.create_game_window()

if __name__ == "__main__":
    root = tk.Tk()
    game = JumpingSquareGame(root)
    root.mainloop()
