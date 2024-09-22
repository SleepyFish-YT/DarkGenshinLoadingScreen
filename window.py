import tkinter as tk
from PIL import ImageGrab
import util
import variables
import os

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pixel Color Checker")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.config(takefocus=0)
        self.root.wm_attributes("-transparentcolor", variables.ignoreColor)
        self.root.configure(bg=variables.ignoreColor)

        self.middle_coords = (self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight() // 2)
        self.root.geometry(f"{self.middle_coords[0]*2}x{self.middle_coords[1]*2}")

        self.finalOverlay = tk.Canvas(self.root, width=(self.middle_coords[0]*2), height=(self.middle_coords[1]*2), bg=variables.ignoreColor)
        self.finalOverlay.config(cursor="none", bd=0, highlightthickness=0, relief='ridge', takefocus=0)
        self.finalOverlay.pack()

        self.center_coords_0 = (self.middle_coords[0], 0)
        self.center_coords_1 = (self.middle_coords[0] - 250, 0)
        self.center_coords_2 = (self.middle_coords[0] + 250, 0)

        self.top_left_coords = (0, 0)
        self.top_right_coords = (self.middle_coords[0]*2 - 1, 0)

        util.log("Info: Created overlay!")
        self.loadedImages = False

        if variables.renderMeme:
            current_directory = os.getcwd()
            image_path = os.path.join(current_directory, "memes")

            util.log(f"Info: Loading memes...")

            try:
                self.meme1 = tk.PhotoImage(file=image_path+"1.png")
                self.meme2 = tk.PhotoImage(file=image_path+"2.png")
                self.meme3 = tk.PhotoImage(file=image_path+"3.png")
                self.meme4 = tk.PhotoImage(file=image_path+"4.png")
                self.meme5 = tk.PhotoImage(file=image_path+"5.png")
                self.meme6 = tk.PhotoImage(file=image_path+"6.png")
                self.meme7 = tk.PhotoImage(file=image_path+"7.png")
                self.meme8 = tk.PhotoImage(file=image_path+"8.png")
                self.meme9 = tk.PhotoImage(file=image_path+"9.png")
                util.log("Info: Memes loaded!")
                self.allowNewMeme = True
                self.loadedImages = True
                self.loadNewMeme()
            except Exception as e:
                util.log(f"Error: Failed to load memes! {e}")
                self.allowNewMeme = False
                pass
            pass

        self.check_pixel_and_render_text()
        self.root.mainloop()
    pass

    def loadNewMeme(self):
        if self.allowNewMeme:
            randomNumber = util.getRandomNumber(1, 9)
            if randomNumber == 1:
                self.currentMeme = self.meme1
            elif randomNumber == 2:
                self.currentMeme = self.meme2
            elif randomNumber == 3:
                self.currentMeme = self.meme3
            elif randomNumber == 4:
                self.currentMeme = self.meme4
            elif randomNumber == 5:
                self.currentMeme = self.meme5
            elif randomNumber == 6:
                self.currentMeme = self.meme6
            elif randomNumber == 7:
                self.currentMeme = self.meme7
            elif randomNumber == 8:
                self.currentMeme = self.meme8
            elif randomNumber == 9:
                self.currentMeme = self.meme9
                pass

            self.allowNewMeme = False
            pass
        pass
    pass

    def are_pixels_white(self):
        screenshot = ImageGrab.grab(bbox=(0, 0, self.middle_coords[0]*2, self.middle_coords[1]*2))

        center_pixel0_white = screenshot.getpixel(self.center_coords_0) == (255, 255, 255)
        center_pixel1_white = screenshot.getpixel(self.center_coords_1) == (255, 255, 255)
        center_pixel2_white = screenshot.getpixel(self.center_coords_2) == (255, 255, 255)
        topCheck1 = center_pixel0_white and center_pixel1_white and center_pixel2_white

        top_left_pixel_white = screenshot.getpixel(self.top_left_coords) == (255, 255, 255)
        top_right_pixel_white = screenshot.getpixel(self.top_right_coords) == (255, 255, 255)
        topCheck2 = top_left_pixel_white and top_right_pixel_white

        return topCheck1 or topCheck2
    pass

    def check_pixel_and_render_text(self):
        if self.are_pixels_white():
            self.loadNewMeme()
            self.render_overlay_with_holes()
            self.root.after(variables.tickUpdateOngoingTimeMilliseconds, self.check_pixel_and_render_text)
        else:
            self.allowNewMeme = True
            self.finalOverlay.delete("all")
            self.finalOverlay.config(bg=variables.ignoreColor)
            self.root.after(variables.tickUpdateNormalTimeMilliseconds, self.check_pixel_and_render_text)
    pass

    def render_overlay_with_holes(self):
        self.finalOverlay.config(bg=variables.overlayColor)
        self.finalOverlay.delete("all")

        hole_size = 1
        yOffset = 0
        for string in variables.renderText:
            fontSize = 12
            fontType = "normal"
            startedWith = False

            if string.startswith("n:"):
                fontSize = 10
                startedWith = True
            elif string.startswith("m:"):
                fontSize = 16
                startedWith = True
            elif string.startswith("t:"):
                fontSize = 24
                startedWith = True
            elif string.startswith("!"):
                fontSize = 12
                fontType = "bold"
                startedWith = True
            pass

            if startedWith:
                string = string[2:].lstrip("!")
            pass

            self.finalOverlay.create_text(self.middle_coords[0], self.middle_coords[1] + yOffset,
                text=string, fill=variables.fontColor, font=("Arial", fontSize, fontType),
                activefill=variables.fontColor, disabledfill=variables.fontColor)
            yOffset += fontSize + 4
            pass
        pass

        if self.loadedImages and variables.renderMeme:
            try:
                self.finalOverlay.create_image(((self.middle_coords[0] * 2) - (self.currentMeme.width() / 2)) - 20, (self.currentMeme.height() / 2) + 20, image=self.currentMeme)
            except Exception as e:
                print(f"Error rendering image: {e}")
                variables.renderMeme = False
                pass
            pass
        pass

        self.finalOverlay.create_rectangle(
            self.center_coords_0[0] - hole_size, self.center_coords_0[1] - hole_size,
            self.center_coords_0[0] + hole_size, self.center_coords_0[1] + hole_size,
        fill=variables.ignoreColor, outline="")

        self.finalOverlay.create_rectangle(
            self.center_coords_1[0] - hole_size, self.center_coords_1[1] - hole_size,
            self.center_coords_1[0] + hole_size, self.center_coords_1[1] + hole_size,
        fill=variables.ignoreColor, outline="")

        self.finalOverlay.create_rectangle(
            self.center_coords_2[0] - hole_size, self.center_coords_2[1] - hole_size,
            self.center_coords_2[0] + hole_size, self.center_coords_2[1] + hole_size,
        fill=variables.ignoreColor, outline="")

        self.finalOverlay.create_rectangle(
            self.top_left_coords[0] - hole_size, self.top_left_coords[1] - hole_size,
            self.top_left_coords[0] + hole_size, self.top_left_coords[1] + hole_size,
        fill=variables.ignoreColor, outline="")

        self.finalOverlay.create_rectangle(
            self.top_right_coords[0] - hole_size, self.top_right_coords[1] - hole_size,
            self.top_right_coords[0] + hole_size, self.top_right_coords[1] + hole_size,
        fill=variables.ignoreColor, outline="")
        pass
    pass

pass