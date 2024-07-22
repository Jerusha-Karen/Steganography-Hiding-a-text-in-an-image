from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("800x600+150+80")
root.resizable(False, False)
root.configure(bg="#1e3d59")

filename = None
secret = None

def reload_icon():
    # Reload the application icon to reflect any changes
    try:
        image_icon = PhotoImage(file="logo.png")
        root.iconphoto(False, image_icon)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot load icon: {e}")

def showimage():
    global filename
    filetypes = [("PNG file", "*.png"), ("JPG File", "*.jpg"), ("All Files", "*.*")]
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File', filetypes=filetypes)
    
    if filename:
        try:
            img = Image.open(filename)
            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img, width=250, height=250)
            lbl.image = img
            status_var.set(f"Selected Image: {os.path.basename(filename)}")
            reload_icon()  # Reload the icon when an image is selected
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
            text1.delete(1.0, END)
            text1.insert(END, stored_message)
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
            reload_icon()  # Reload the icon when an image is saved
        except Exception as e:
            messagebox.showerror("Error", f"Error saving image: {e}")
    else:
        status_var.set("Save operation cancelled")

def clear_text():
    text1.delete(1.0, END)
    status_var.set("Text area cleared")

# Application icon
reload_icon()

# Logo
logo = PhotoImage(file="logo.png")
Label(root, image=logo, bg="#1e3d59").place(x=10, y=0)

Label(root, text="CYBER SCIENCE", bg="#1e3d59", fg="#f0a500", font="arial 25 bold").place(x=100, y=20)

# First Frame
f = Frame(root, bd=3, bg="#162447", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="#162447")
lbl.place(x=40, y=10)

# Second Frame
frame2 = Frame(root, bd=3, width=340, height=280, bg="#e43f5a", relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Third Frame
frame3 = Frame(root, bd=3, bg="#1e3d59", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", bg="#162447", fg="white", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", bg="#162447", fg="white", command=save_image).place(x=180, y=30)
Label(frame3, text="Picture, Image, Photo File", bg="#1e3d59", fg="yellow").place(x=20, y=5)

# Fourth Frame
frame4 = Frame(root, bd=3, bg="#1e3d59", width=330, height=100, relief=GROOVE)
frame4.place(x=350, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", bg="#162447", fg="white", command=hide_message).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", bg="#162447", fg="white", command=show_message).place(x=180, y=30)
Label(frame4, text="Picture, Image, Photo File", bg="#1e3d59", fg="yellow").place(x=20, y=5)

# Status Bar
status_var = StringVar()
status_var.set("Welcome to Steganography")
status_bar = Label(root, textvariable=status_var, relief=SUNKEN, anchor=W, bg="#162447", fg="white")
status_bar.pack(side=BOTTOM, fill=X)

# Clear Text Button
Button(root, text="Clear Text", width=10, height=2, font="arial 14 bold", bg="#e43f5a", fg="white", command=clear_text).place(x=600, y=500)

# Run the Tkinter event loop
root.mainloop()
