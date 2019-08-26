from tkinter import *
import tkinter.messagebox as dialogs
from tkinter import ttk
from cryptography.fernet import InvalidToken

from utils import files as util, crypto


class InputFrame(Frame):
    def get_values(self):
        values = {"password": self.entry_password.get()}
        if values["password"] == self.entry_repassword.get():
            values["username"] = self.entry_username.get()
            values["website"] = self.entry_website.get()
            for key in values.keys():
                if len(values[key]) is 0:
                    dialogs.showerror(title="Blank Values", message="Please enter valid values!!")
                    return None
        else:
            dialogs.showerror(title="Password", message="Passwords don't match!!")
            return None
        return values

    def __init__(self, window, **kw):
        super().__init__(window)

        self.label_username = Label(self, text="Username/Email : ")
        self.entry_username = Entry(self)

        self.label_website = Label(self, text="Website : ")
        self.entry_website = Entry(self)

        self.label_password = Label(self, text="Password : ")
        self.entry_password = Entry(self, show="*")

        self.label_repassword = Label(self, text="Re-Enter Password : ")
        self.entry_repassword = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.entry_username.grid(row=0, column=1)

        self.label_website.grid(row=1, sticky=E)
        self.entry_website.grid(row=1, column=1)

        self.label_password.grid(row=2, sticky=E)
        self.entry_password.grid(row=2, column=1)

        self.label_repassword.grid(row=3, sticky=E)
        self.entry_repassword.grid(row=3, column=1)


class ButtonFrame(Frame):
    def __init__(self, master, input_frame):
        super().__init__(master)
        self.input_frame = input_frame

        self.button_save = Button(self, text="Save", command=self.save_button)
        self.button_show_all = Button(self, text="Show All", command=self.show_all)

        self.button_save.grid(row=0, column=0)
        self.button_show_all.grid(row=0, column=1)

    def save_button(self):
        values = self.input_frame.get_values()
        if values is not None:
            password_dialog = PasswordDialog(self.master, "Save", values=values)
            password_dialog.top.grab_set()

    def show_all(self):
        password_dialog = PasswordDialog(self.master, "Show All")
        password_dialog.top.grab_set()


class PasswordDialog:
    def __init__(self, parent, action, **values):
        top = self.top = Toplevel(parent)
        self.action = action
        if action is "Save":
            self.values = values['values']

        self.password_label = Label(top, text="Master password : ")
        self.password_entry = Entry(top, show="*")

        self.done_button = Button(top, text="Done", command=self.submit_password)

        self.password_label.grid(row=0, sticky=E)
        self.password_entry.grid(row=0, column=1)
        self.done_button.grid(row=0, column=2)

        self.top.resizable(False, False)
        window_xpos = str((top.winfo_screenwidth() // 2 - top.winfo_reqwidth() // 2))
        window_ypos = str((top.winfo_screenheight() // 2 - top.winfo_reqheight() // 2))
        top.geometry("+" + window_xpos + "+" + window_ypos)

    def submit_password(self):
        password = self.password_entry.get()
        try:
            if self.action is "Save":
                if not util.store_values(password, self.values) == 1:
                    dialogs.showerror("Duplicate", "Values already exists!!")
            else:
                values = util.get_values(crypto.create_key(password))
                print(values)
                ShowAllDialog(values)
        except InvalidToken:
            dialogs.showerror("Error", "Password Incorrect")
        self.top.destroy()


class NewPasswordWindow:
    def __init__(self):
        root = self.root = Tk()
        root.title('New Password')
        self.password_label = Label(root, text='Password : ')
        self.password_entry = Entry(root, show='*')

        self.repassword_label = Label(root, text='Re-Enter Password : ')
        self.repassword_entry = Entry(root, show="*")

        self.password_label.grid(row=0, sticky=E)
        self.password_entry.grid(row=0, column=1)

        self.repassword_label.grid(row=1, sticky=E)
        self.repassword_entry.grid(row=1, column=1)

        self.submit_button = Button(root, text='Submit', command=self.save_password)
        self.submit_button.grid(row=2, column=1)

        self.root.resizable(False, False)
        window_xpos = str((root.winfo_screenwidth() // 2 - root.winfo_reqwidth() // 2))
        window_ypos = str((root.winfo_screenheight() // 2 - root.winfo_reqheight() // 2))
        root.geometry("+" + window_xpos + "+" + window_ypos)

        root.mainloop()

    def save_password(self):

        password = self.password_entry.get()
        repassword = self.repassword_entry.get()

        if password == repassword and password is not '':
            util.create_password_file(password)
            self.root.destroy()
            main()
        else:
            dialogs.showerror("Password", "Passwords not valid!!!")


class MainWindow:
    def __init__(self):
        root = self.root = Tk()

        self.input_frame = InputFrame(root)
        self.button_frame = ButtonFrame(root, self.input_frame)
        self.input_frame.grid()
        self.button_frame.grid(row=1)

        self.root.resizable(False, False)
        window_xpos = str((root.winfo_screenwidth() // 2 - root.winfo_reqwidth() // 2))
        window_ypos = str((root.winfo_screenheight() // 2 - root.winfo_reqheight() // 2))
        root.geometry("+" + window_xpos + "+" + window_ypos)

        root.mainloop()


class ShowAllDialog:
    def __init__(self, values):
        self.values = values
        top = self.top = Toplevel()
        top.title("All passwords !!")
        index = 0
        password_view = self.password_view = ttk.Treeview(top, columns=('#1', '#2', '#3'), show=['headings'])
        self.password_view.heading('#1', text='Username/E-mail')
        self.password_view.heading('#2', text='Password')
        self.password_view.heading('#3', text='Website')

        passwords = values['passwords']

        for password in passwords:
            password_view.insert('', 'end', text=password['username'],
                                 values=(password['username'], password['password'], password['website']))
        password_view.pack()
        self.top.resizable(False, False)
        window_xpos = str((top.winfo_screenwidth() // 2 - top.winfo_reqwidth() // 2))
        window_ypos = str((top.winfo_screenheight() // 2 - top.winfo_reqheight() // 2))
        top.geometry("+" + window_xpos + "+" + window_ypos)
        top.grab_release()


def main():
    if util.key_exists():
        MainWindow()
    else:
        NewPasswordWindow()


if __name__ == '__main__':
    main()
