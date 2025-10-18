from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from pygame import mixer
import threading

mixer.init()

def play_gif():
    def run():
        root = Tk()
        root.geometry("1000x500")
        root.title("EVA Assistant")
        root.lift()
        root.attributes("-topmost", True)
        root.resizable(False, False)

        # Load GIF and audio
        gif = Image.open("gif.gif")
        lbl = Label(root)
        lbl.place(x=0, y=0)

        frames = [ImageTk.PhotoImage(frame.copy().resize((1000, 500))) for frame in ImageSequence.Iterator(gif)]

        mixer.music.load("notification.mp3.wav")
        mixer.music.play()

        def update(index=0):
            if not hasattr(root, "closing"):
                frame = frames[index]
                lbl.configure(image=frame)
                next_index = (index + 1) % len(frames)
                root.after(60, update, next_index)

        update()
        root.after(2000, lambda: setattr(root, "closing", True) or root.destroy())  # Auto-close after 2 seconds
        root.mainloop()

    threading.Thread(target=run).start()
