from tkinter import *
import random


class Ball:
    def __init__(self, canvas, paddle, color, speed):
        self.canvas = canvas
        self.paddle = paddle
        self.score = 0
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.x = random.choice([-3, -2, -1, 1, 2, 3])
        self.y = -speed
        self.canvas_height = 400
        self.canvas_width = 500
        self.hit_bottom = False
        self.display_score = canvas.create_text(
            445, 20, text=f'Score: {self.score}', fill='Black', font=('Helvetica', 10)
        )

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.x *= -1
        if self.hit_paddle(pos):
            self.y *= -1
            self.score += 1
            self.canvas.itemconfig(self.display_score, text=f'Score: {self.score}')
        if pos[1] <= 0:
            self.y = abs(self.y)
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        return (
            pos[2] >= paddle_pos[0]
            and pos[0] <= paddle_pos[2]
            and pos[3] >= paddle_pos[1]
            and pos[3] <= paddle_pos[3]
            and self.y > 0
        )


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 85, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = 500
        self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        self.canvas.bind_all('<KeyPress-Right>', self.move_right)
        self.canvas.bind_all('<KeyRelease-Left>', self.stop)
        self.canvas.bind_all('<KeyRelease-Right>', self.stop)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.x = 0

    def move_left(self, event):
        self.x = -4

    def move_right(self, event):
        self.x = 4

    def stop(self, event):
        self.x = 0


def start_game():
    global speed, paddle, ball, countdown_text

    try:
        speed = int(speed_entry.get())
        if not 1 <= speed <= 10:
            raise ValueError
    except ValueError:
        speed_label.config(text='Please enter a number from 1 to 10.')
        return

    speed_label.pack_forget()
    speed_entry.pack_forget()
    start_button.pack_forget()

    paddle = Paddle(canvas, 'Blue')
    ball = Ball(canvas, paddle, 'Red', speed)
    countdown_text = canvas.create_text(
        250, 190, text='', fill='Red', font=('Helvetica', 48, 'bold')
    )
    countdown(3)


def countdown(number):
    if number > 0:
        canvas.itemconfig(countdown_text, text=str(number))
        tk.after(1000, countdown, number - 1)
    else:
        canvas.itemconfig(countdown_text, text='')
        game_loop()


def game_loop():
    if ball.hit_bottom:
        canvas.itemconfig(game_over_text, state='normal')
        canvas.itemconfig(final_score_text, text=f'Your Score: {ball.score}', state='normal')
        return

    ball.draw()
    paddle.draw()
    tk.after(10, game_loop)


tk = Tk()
tk.title('Bounce Game')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)

speed_label = Label(tk, text='Which speed from 1 to 10?', font=('Helvetica', 12))
speed_label.pack(pady=(10, 5))

speed_entry = Entry(tk, width=10, font=('Helvetica', 12))
speed_entry.pack()
speed_entry.focus_set()

start_button = Button(tk, text='Start Game', command=start_game)
start_button.pack(pady=10)

canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()

paddle = None
ball = None
countdown_text = None
game_over_text = canvas.create_text(
    250, 150, text='GAME OVER', fill='Red', font=('Helvetica', 30), state='hidden'
)
final_score_text = canvas.create_text(
    250, 200, text='', fill='Black', font=('Helvetica', 12), state='hidden'
)

tk.mainloop()
