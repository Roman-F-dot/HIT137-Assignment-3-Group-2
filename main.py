import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

from image_processor import ImageProcessor
from GameManager import GameManager
from gui import GameGUI

class GameApp:
    def __init__(self, root):
        self.root = root

        # init backend files
        self.processor = ImageProcessor()
        self.logic = GameManager()
        self.gui = GameGUI(root)

        self.gui.load_btn.config(command=self.load_new_image)
        self.gui.reveal_btn.config(command=self.reveal_all)
        self.gui.canvas_right.bind("<Button-1>", self.handle_canvas_click)

        self.image_loaded = False

    def load_new_image(self):
        filepath = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )

        if not filepath:
            return 

        # reset the game state
        self.logic.reset_game()
        self.gui.update_score(5, 0)

        # process the image through mahmuds code
        self.processor.load_image(filepath)
        self.processor.alter_image() 

        self.image_loaded = True
        self.refresh_displays()

    def refresh_displays(self):
        # cv2 uses bgr, tkinter needs rgb
        orig_cv = self.processor.original_image
        mod_cv = self.processor.modified_image

        orig_rgb = cv2.cvtColor(orig_cv, cv2.COLOR_BGR2RGB)
        mod_rgb = cv2.cvtColor(mod_cv, cv2.COLOR_BGR2RGB)

        # resize to fit kellys canvas size
        orig_pil = Image.fromarray(orig_rgb).resize((500, 500))
        mod_pil = Image.fromarray(mod_rgb).resize((500, 500))

        tk_orig = ImageTk.PhotoImage(image=orig_pil)
        tk_mod = ImageTk.PhotoImage(image=mod_pil)

        self.gui.update_images(tk_orig, tk_mod)

    def handle_canvas_click(self, event):
        if self.image_loaded == True:
            # math to scale the click back to the original image size
            orig_h, orig_w = self.processor.original_image.shape[:2]
            real_x = int((event.x / 500.0) * orig_w)
            real_y = int((event.y / 500.0) * orig_h)

            targets = self.processor.get_altered_regions()
            result = self.logic.check_click(real_x, real_y, targets)

            status = result["status"]

            if status == "hit":
                idx = result["index"]
                box = targets[idx]

                #Draw green circles on BOTH images
                self.processor.draw_circle_on_found(self.processor.original_image, box[0], box[1], box[2], box[3])
                self.processor.draw_circle_on_found(self.processor.modified_image, box[0], box[1], box[2], box[3])

                self.refresh_displays()
                self.gui.update_score(5 - result["found"], self.logic.mistakes)

                if result["game_won"]:
                    self.gui.show_victory()

            elif status == "miss":
                self.gui.update_score(5 - self.logic.found, result["mistakes"])

                if result["game_over"]:
                    self.gui.show_game_over()

    def reveal_all(self):
        if not self.image_loaded or self.logic.game_over or self.logic.game_won:
            return

        targets = self.processor.get_altered_regions()
        found_list = self.logic.found_indices

        for i in range(len(targets)):
            if i not in found_list:
                rx, ry, rw, rh = targets[i]
                cx = rx + rw // 2
                cy = ry + rh // 2
                rad = 40

                cv2.circle(self.processor.original_image, (cx, cy), rad, (255, 0, 0), 3)
                cv2.circle(self.processor.modified_image, (cx, cy), rad, (255, 0, 0), 3)

        self.refresh_displays()
        self.logic.game_over = True 

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()