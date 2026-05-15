from tkinter import *
import tkinter.messagebox

class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Spot the Difference - Group 2")
        master.geometry("1050x650")
        
        self.top_frame = Frame(master, pady=10)
        self.top_frame.pack(side=TOP, fill=X)
        
        self.bottom_frame = Frame(master, pady=10)
        self.bottom_frame.pack(side=BOTTOM, expand=True, fill=BOTH)

        self.load_btn = Button(self.top_frame, text="Load Image", width=15, bg="lightgray")
        self.load_btn.pack(side=LEFT, padx=20)
        
        self.reveal_btn = Button(self.top_frame, text="Reveal Differences", width=15, bg="lightgray")
        self.reveal_btn.pack(side=LEFT, padx=10)
        
        self.remain_label = Label(self.top_frame, text="Differences Remaining: 5", font=("Arial", 12, "bold"))
        self.remain_label.pack(side=LEFT, padx=40)
        
        self.mistake_label = Label(self.top_frame, text="Mistakes: 0 / 3", font=("Arial", 12, "bold"), fg="red")
        self.mistake_label.pack(side=LEFT, padx=10)

        self.canvas_left = Canvas(self.bottom_frame, width=500, height=500, bg="gray", relief=SUNKEN, bd=2)
        self.canvas_left.pack(side=LEFT, padx=10)
        
        self.canvas_right = Canvas(self.bottom_frame, width=500, height=500, bg="gray", relief=SUNKEN, bd=2, cursor="crosshair")
        self.canvas_right.pack(side=LEFT, padx=10)
        
        self.canvas_right.bind("<Button-1>", self.on_canvas_click)
        
        self.tk_img_left = None
        self.tk_img_right = None

    def on_canvas_click(self, event):
        print(f"Click registered at x={event.x}, y={event.y}")

    def update_score(self, remaining, mistakes):
        self.remain_label.config(text=f"Differences Remaining: {remaining}")
        self.mistake_label.config(text=f"Mistakes: {mistakes} / 3")

    def update_images(self, img_left, img_right):
        self.tk_img_left = img_left
        self.tk_img_right = img_right
        self.canvas_left.delete("all")
        self.canvas_right.delete("all")
        self.canvas_left.create_image(0, 0, anchor=NW, image=self.tk_img_left)
        self.canvas_right.create_image(0, 0, anchor=NW, image=self.tk_img_right)

    def show_game_over(self):
        tkinter.messagebox.showinfo("Game Over", "You made 3 mistakes! Load a new image to try again.")

    def show_victory(self):
        tkinter.messagebox.showinfo("Winner!", "You found all 5 differences! Great job.")