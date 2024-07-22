
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb

def center_window(win):
    """
    Centers a Tkinter window on the screen.
    """
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    width = 900
    height = 700
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Steganography - Hiding a text in an image")
root.geometry("3600x700")
center_window(root)
root.resizable(True, True)
root.configure(bg="#000000")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


filename = None
secret = None

def selectimage():
    global filename
    filetypes = [("PNG file", "*.png"), ("JPG File", "*.jpg"), ("All Files", "*.*")]
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File', filetypes=filetypes)
    
    if filename:
        try:
            img = Image.open(filename)
            img = img.resize((250, 250), Image.LANCZOS)

            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img, width=250, height=250)
            lbl.image = img
            status_var.set(f"Selected Image: {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open image: {e}")
            filename = None
    else:
        status_var.set("No image selected")


def hide_message():
    global secret
    if not filename:
        messagebox.showerror("Error", "No image selected")
        return

    message = text1.get(1.0, END).strip()
    if not message:
        messagebox.showerror("Error", "No message to hide")
        return
   
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    if not password:
        messagebox.showerror("Error", "Password is required")
        return

    try:
        secret = lsb.hide(filename, password + ":" + message)
        status_var.set("Message hidden successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Error hiding message: {e}")

def show_message():
    if not filename:
        messagebox.showerror("Error", "No image selected")
        return

    try:
        clear_message = lsb.reveal(filename)
        password = simpledialog.askstring("Password", "Enter password:", show='*')
        if not password:
            messagebox.showerror("Error", "Password is required")
            return
        
        stored_password, stored_message = clear_message.split(":", 1)
        
        if password == stored_password:
            text2.delete(1.0, END)
            text2.insert(END, stored_message)
            status_var.set("Message revealed successfully")
        else:
            messagebox.showerror("Error", "Incorrect password")
    except Exception as e:
        messagebox.showerror("Error", f"Error revealing message: {e}")

def save_image():
    if not secret:
        messagebox.showerror("Error", "No hidden message to save")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
    if save_path:
        try:
            secret.save(save_path)
            status_var.set(f"Image saved: {os.path.basename(save_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving image: {e}")
    else:
        status_var.set("Save operation cancelled")

def clear_text():
    text1.delete(1.0, END)
    status_var.set("Text area cleared")

# Application icon
image_icon1 = PhotoImage(file="logo.png")
root.iconphoto(False, image_icon1)

# Logo
logo = PhotoImage(file="logo.png")
Label(root, image=logo, bg="#000000").place(x=350, y=100)

Label(root, text="The Invisible Messenger: Exploring the Power of Steganography", bg="#000000", fg="#e43f5a", font="arial 25 bold").place(x=100, y=20)

# First Frame
f = Frame(root, bd=3, bg="#333333", width=340, height=280, relief=GROOVE)
f.place(x=10, y=120)

lbl = Label(f, bg="#333333")
lbl.place(x=40, y=10)


# Second Frame
frame2 = Frame(root, bd=3, width=340, height=280, bg="#e43f5a", relief=GROOVE)
frame2.place(x=360, y=120)

text1 = Text(frame2, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Third Frame
frame3 = Frame(root, bd=3, bg="#162447", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=430)

Button(frame3, text="Select Image", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=selectimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=save_image).place(x=180, y=30)
Label(frame3, text="Select an image", bg="#162447", fg="#e43f5a").place(x=20, y=5)

# Fourth Frame
frame4 = Frame(root, bd=3, bg="#162447", width=330, height=100, relief=GROOVE)
frame4.place(x=355, y=430)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=hide_message).place(x=20, y=30)
Button(frame4, text="Clear Text", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=clear_text).place(x=180, y=30)

#Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=show_message).place(x=180, y=30)
Label(frame4, text="Hiding the Text", bg="#162447", fg="#e43f5a").place(x=20, y=5)

#Fifth frame
f5 = Frame(root, bd=3, bg="#333333", width=340, height=280, relief=GROOVE)
f5.place(x=800, y=120)

lbl = Label(f5, bg="#333333")
lbl.place(x=800, y=10)


# Sixth Frame
frame6 = Frame(root, bd=3, width=340, height=280, bg="#e43f5a", relief=GROOVE)
frame6.place(x=1150, y=120)

text2 = Text(frame6, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text2.place(x=0, y=0, width=320, height=295)

scrollbar2 = Scrollbar(frame6)
scrollbar2.place(x=320, y=0, height=300)

scrollbar2.configure(command=text2.yview)
text2.configure(yscrollcommand=scrollbar2.set)

# Seventh Frame
frame7 = Frame(root, bd=3, bg="#162447", width=330, height=100, relief=GROOVE)
frame7.place(x=800, y=430)

Button(frame7, text="Select Image", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=selectimage).place(x=100, y=30)
#Button(frame7, text="Save Image", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=save_image).place(x=180, y=30)
Label(frame7, text="Encrypted Image", bg="#162447", fg="#e43f5a").place(x=20, y=5)

# Eighth Frame
frame8 = Frame(root, bd=3, bg="#162447", width=330, height=100, relief=GROOVE)
frame8.place(x=1150, y=430)

#Button(frame8, text="Hide Data", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=hide_message).place(x=20, y=30)
Button(frame8, text="Show Data", width=10, height=2, font="arial 14 bold", bg="#444444", fg="#cccccc", command=show_message).place(x=100, y=30)
Label(frame8, text="Secret Message", bg="#162447", fg="#e43f5a").place(x=20, y=5)

# Status Bar
status_var = StringVar()
status_var.set("Welcome to Steganography")
status_bar = Label(root, textvariable=status_var, relief=SUNKEN, anchor=W, bg="#444444", fg="white")
status_bar.pack(side=BOTTOM, fill=X)

# Clear Text Button

# Run the Tkinter event loop
root.mainloop()
