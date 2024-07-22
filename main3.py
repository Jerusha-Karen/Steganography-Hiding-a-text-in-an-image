def hide_message():
    global secret
    if not filename:
        messagebox.showerror("Error", "No image selected")
        return

    message = text1.get(1.0, END).strip()
    if not message:
        messagebox.showerror("Error", "No message to hide")
        return

    try:
        def on_password_submit():
            password = password_entry.get()
            if password:
                secret = lsb.hide(filename, message)
                secret.save("hidden.png")
                popup.destroy()
                status_var.set("Message hidden successfully")
            else:
                messagebox.showerror("Error", "Password cannot be empty")

        # Create the password popup
        popup = Toplevel(root)
        popup.title("Enter Password")
        popup.geometry("300x150")
        popup.configure(bg="#333333")

        Label(popup, text="Enter Password", bg="#333333", fg="#ffffff", font=("Arial", 12)).pack(pady=10)
        password_entry = Entry(popup, show='*', bg="#555555", fg="#ffffff", font=("Arial", 12))
        password_entry.pack(pady=10)

        Button(popup, text="Submit", command=on_password_submit, bg="#444444", fg="#ffffff", font=("Arial", 12)).pack(pady=10)

        popup.transient(root)
        popup.grab_set()
        root.wait_window(popup)
    except Exception as e:
        messagebox.showerror("Error", f"Error hiding message: {e}")

def show_message():
    if not filename:
        messagebox.showerror("Error", "No image selected")
        return

    try:
        def on_password_submit():
            password = password_entry.get()
            if password:
                clear_message = lsb.reveal(filename)
                text1.delete(1.0, END)
                text1.insert(END, clear_message)
                popup.destroy()
                status_var.set("Message revealed successfully")
            else:
                messagebox.showerror("Error", "Password cannot be empty")

        # Create the password popup
        popup = Toplevel(root)
        popup.title("Enter Password")
        popup.geometry("300x150")
        popup.configure(bg="#333333")

        Label(popup, text="Enter Password", bg="#333333", fg="#ffffff", font=("Arial", 12)).pack(pady=10)
        password_entry = Entry(popup, show='*', bg="#555555", fg="#ffffff", font=("Arial", 12))
        password_entry.pack(pady=10)

        Button(popup, text="Submit", command=on_password_submit, bg="#444444", fg="#ffffff", font=("Arial", 12)).pack(pady=10)

        popup.transient(root)
        popup.grab_set()
        root.wait_window(popup)
    except Exception as e:
        messagebox.showerror("Error", f"Error revealing message: {e}")














password = simpledialog.askstring("Password", "Enter password:", show='*')
    if not password:
        messagebox.showerror("Error", "Password is required")
        return
