import threading
import time
from playsound import playsound
from customtkinter import *
from tkinterdnd2 import TkinterDnD, DND_ALL
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from stegano import lsb

set_appearance_mode("dark")
set_default_color_theme("FlipperZeroTheme.json")

class Tk(CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

def show_error():

    showerror("ERROR", "Expected a PNG image but received another file")

def process_drag_and_drop(event):
    if event.data.endswith(".png") or event.data.endswith(".PNG"):
        playsound('Sound.mp3', False)
        encode_or_decode(event.data)
    else:
        show_error()

FILE = None
progressbar = None
img = None
frame = None
def encode_img(text):
    global progressbar, img
    img = lsb.hide(FILE, text)
    progressbar.stop()

    for x in range(0, 101):
        progressbar.set(x/100)
        root.update()
    playsound('Sound.mp3', False)

    time.sleep(0.5)
    for widget in frame.winfo_children():
        widget.destroy()

    save_btn = CTkButton(frame, text="Click Here to Download the Image", font=("HaxrCorp4089", 70), command=save)
    save_btn.place(anchor="center", relx=0.5, rely=0.5)

    go_back = CTkButton(frame, text="< Go Back", font=("HaxrCorp4089", 70), command=home)
    go_back.place(anchor="nw", x=20, y=20)
    save()

def save():
    file = asksaveasfilename()
    if file != "":
        if file.endswith(".png"):
            img.save(file)
        else:
            img.save(file+".png")

def encode(text):
    global progressbar


    for widget in frame.winfo_children():
        widget.destroy()
    description = CTkLabel(frame, text="Working On It.....", font=("HaxrCorp4089", 50), anchor="w")
    description.pack(fill="x", pady=20, padx=20)
    progressbar = CTkProgressBar(frame, height=50, corner_radius=3)
    progressbar.pack(expand=True, fill="x", padx=20)
    progressbar.start()
    t1 = threading.Thread(target=encode_img, args=(text, ))
    t1.start()







def encode_ui():
    playsound('Sound.mp3', False)

    for widget in frame.winfo_children():
        widget.destroy()

    data = CTkTextbox(frame, height=300, font=("HaxrCorp4089", 50))
    data.pack(expand=True, fill="both", padx=20, pady=20)

    encode_btn = CTkButton(frame, font=("HaxrCorp4089", 70), text=" Encode", anchor="w", command=lambda : encode(data.get(0.0, "end")))
    encode_btn.pack(expand=True, fill="both", padx=20, pady=(0, 20))


def decode_ui():
    playsound('Sound.mp3', False)

    for widget in frame.winfo_children():
        widget.destroy()
    try:
        data = lsb.reveal(FILE)
        go_back = CTkButton(frame, text="< Go Back", font=("HaxrCorp4089", 70), command=home)
        go_back.place(anchor="nw", x=20, y=20)

        text = CTkLabel(frame, text=data, font=("HaxrCorp4089", 70), wraplength=700)
        text.place(anchor="center", relx=0.5, rely=0.5)
    except Exception as e:
        showerror("Error", e)
        go_back = CTkButton(frame, text="< Go Back", font=("HaxrCorp4089", 70), command=home)
        go_back.place(anchor="nw", x=20, y=20)





def encode_or_decode(file):
    global FILE
    playsound('Sound.mp3', False)

    for widget in frame.winfo_children():
        widget.destroy()

    FILE = file

    encodeOption = CTkFrame(frame)
    encodeOption.pack(padx=20, pady=30, expand=True, fill="both", side="left")
    encodeOption.bind("<Enter>", lambda e: encodeOption.configure(fg_color="#814007"))
    encodeOption.bind("<Leave>", lambda e: encodeOption.configure(fg_color="#000000"))
    encodeOption.bind("<Button-1>", lambda e: encode_ui())

    description = CTkLabel(encodeOption, text="Add data to the image   ", font=("HaxrCorp4089", 50), anchor="w")
    description.pack(side="bottom", fill="x", pady=20, padx=20)
    description.bind("<Enter>", lambda e: encodeOption.configure(fg_color="#814007"))
    description.bind("<Leave>", lambda e: encodeOption.configure(fg_color="#000000"))
    description.bind("<Button-1>", lambda e: encode_ui())

    title = CTkLabel(encodeOption, text="Encode", font=("HaxrCorp4089", 70), anchor="w")
    title.pack(side="bottom", fill="x", pady=0, padx=20)
    title.bind("<Enter>", lambda e: encodeOption.configure(fg_color="#814007"))
    title.bind("<Leave>", lambda e: encodeOption.configure(fg_color="#000000"))
    title.bind("<Button-1>", lambda e: encode_ui())



    decodeOption = CTkFrame(frame)
    decodeOption.pack(padx=20, pady=30, expand=True, fill="both", side="left")
    decodeOption.bind("<Enter>", lambda e: decodeOption.configure(fg_color="#814007"))
    decodeOption.bind("<Leave>", lambda e: decodeOption.configure(fg_color="#000000"))
    decodeOption.bind("<Button-1>", lambda e: decode_ui())

    description = CTkLabel(decodeOption, text="Decode data in the image", font=("HaxrCorp4089", 50), anchor="w")
    description.pack(side="bottom", fill="x", pady=20, padx=20)
    description.bind("<Enter>", lambda e: decodeOption.configure(fg_color="#814007"))
    description.bind("<Leave>", lambda e: decodeOption.configure(fg_color="#000000"))
    description.bind("<Button-1>", lambda e: decode_ui())

    title = CTkLabel(decodeOption, text="Decode", font=("HaxrCorp4089", 70), anchor="w")
    title.pack(side="bottom", fill="x", pady=0, padx=20)
    title.bind("<Enter>", lambda e: decodeOption.configure(fg_color="#814007"))
    title.bind("<Leave>", lambda e: decodeOption.configure(fg_color="#000000"))
    title.bind("<Button-1>", lambda e: decode_ui())






def choose_file():
    file = askopenfilename()

    if file != "":
        if file.endswith(".png") or file.endswith(".PNG"):
            playsound('Sound.mp3', False)

            encode_or_decode(file)
        else:
            show_error()

root = Tk()
root.geometry("900x500")
root.title("Hide Data")

def home():
    global frame
    if frame != None:
        frame.destroy()
        playsound('Sound.mp3', False)


    frame = CTkFrame(root)
    frame.pack(padx=20, pady=20, expand=True, fill="both")

    text = CTkLabel(frame, text="Drag and Drop the Image or Choose the File", font=("HaxrCorp4089", 50))
    text.pack(pady=20)

    dnd_frame = CTkFrame(frame)
    dnd_frame.pack(padx=30, pady=(10, 30), expand=True, fill="both")

    dnd_frame.drop_target_register(DND_ALL)
    dnd_frame.dnd_bind("<<Drop>>", process_drag_and_drop)


    lbl = CTkButton(dnd_frame, text="Click to choose the file or Drag and Drop the File", font=("HaxrCorp4089", 30), hover=False, fg_color="transparent", command=choose_file)
    lbl.pack(expand=True, fill="both")

home()

root.mainloop()
