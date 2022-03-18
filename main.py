# This is used to run commands directly or through a jumpserver. For taking backup.

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import os
import time

root = Tk()

about_this_application = '''
Hi,
This application is created for searching a list of IPs from hundreds of network device backup folder. 
This can be be used for other use cases as well.
Source code for this is available in : https://github.com/sibisita/Multi-Search/blob/main/multi_search.py .
Instructions:
Step 1: Enter the values you want to search in top left box. Each line is taken a seperate entry.
Step 2: Select the location where you have the files to be searched. Use 'Browse Search Folder' button.
Step 3: Select the location where you want the results to be saved. Use 'Browse Save Folder' button.
Step 4: (Optional) You can enter any notes in the box below the search button.
Step 5: Press search button.
After the search is completed. The results location is automatically opened in windows file explorer.
In the application, you can press reset to search again.
Regards,
Sibi
'''

save_location1 = os.path.expanduser('~')


def logs_entry(log, end="\n"):
    statusbar.configure(state='normal')
    statusbar.insert(END, log+end)
    statusbar.configure(state='disabled')
    statusbar.yview(END)
    root.update_idletasks()


def new_window():
    window11 = Toplevel(root)
    window11.geometry("1000x400")

    window11.title("About This Application!")
    a11 = Text(window11, height=400, width=1000)
    a11.insert(INSERT, about_this_application)
    a11.grid(column=0, row=0, pady=1, padx=1, sticky="w")


def save_in_folder():
    temp_var = filedialog.askdirectory()
    if temp_var != "":
        global save_location1
        save_location1 = temp_var
        l2.configure(text=save_location1)


# FrontEnd
root.title("Scripter")
ttk.Label(root, text="Enter the device list in below box. ", font=(
    "Times New Roman", 12)).grid(column=0, row=0, sticky="w", columnspan=2)
ttk.Label(root, text="   Each line is treated as a seperate value.",
          font=("Times New Roman", 10)).grid(column=0, row=1, sticky="w",)
ttk.Label(root, text="Enter the command to be executed in below box. ", font=(
    "Times New Roman", 12)).grid(column=1, row=0, sticky="w", columnspan=2)
ttk.Label(root, text="   Each line is treated as a seperate value.",
          font=("Times New Roman", 10)).grid(column=1, row=1, sticky="w",)
text_area = scrolledtext.ScrolledText(
    root, wrap=WORD, width=30, height=15, font=("Times New Roman", 12))

l2 = ttk.Label(root, text=save_location1)
save_loc = ttk.Button(root, text="Browse Save folder", command=save_in_folder)
jumpServerLabel = Label(root, text="Jumpserver (name or IP)", font=(
    "Times New Roman", 12)).grid(row=4, column=3)
jumpserver = StringVar()
jumpServerEntry = Entry(root, textvariable=jumpserver).grid(row=4, column=4)
jumpuserLabel = Label(root, text="Jumpserver Username", font=(
    "Times New Roman", 12)).grid(row=5, column=3)
jumpuser = StringVar()
jumpuserEntry = Entry(root, textvariable=jumpuser).grid(row=5, column=4)

passwordLabel = Label(root, text="Jumpserver Password", font=(
    "Times New Roman", 12)).grid(row=6, column=3)
jumpServerpassword = StringVar()
passwordEntry = Entry(root,  textvariable=jumpServerpassword,
                      show='*').grid(row=6, column=4)

usernameLabel = Label(root, text="Device Username", font=(
    "Times New Roman", 12)).grid(row=10, column=3)
deviceusername = StringVar()
usernameEntry = Entry(root, textvariable=deviceusername).grid(row=10, column=4)

passwordLabel = Label(root, text="Device Password", font=(
    "Times New Roman", 12)).grid(row=11, column=3)
userpassword = StringVar()
passwordEntry = Entry(root,  textvariable=userpassword,
                      show='*').grid(row=11, column=4)

enableLabel = Label(root, text="Cisco enable Password", font=(
    "Times New Roman", 12)).grid(row=12, column=3)
enablepassword = StringVar()
enablepasswordEntry = Entry(root,  textvariable=enablepassword,
                            show='*').grid(row=12, column=4)

command_list = scrolledtext.ScrolledText(
    root, wrap=WORD, width=30, height=15, font=("Times New Roman", 12))
about = ttk.Button(root, text="About", width=8, command=new_window)

space = ttk.Label(root, text=" ")
file_count = ttk.Label(
    root, text="Backup progress stats will appear here!!!", font=("Times New Roman", 14))
statusbar = scrolledtext.ScrolledText(
    root, wrap=WORD, width=60, height=15, font=("Times New Roman", 12))
statusbar.insert(INSERT, "Here comes the logs\n\n")
statusbar.configure(state='disabled')
output_window = scrolledtext.ScrolledText(
    root, wrap=WORD, width=45, height=30, state='disabled', font=("Times New Roman", 12))
output_lable = ttk.Label(
    root, text="Searched values and their number of occurances: ", font=("Times New Roman", 10))

# grid position
text_area.grid(column=0, row=2, pady=1, padx=1,
               sticky="w", rowspan=15, columnspan=2)
about.grid(column=4, row=0, padx=5, sticky=N+E)
command_list.grid(column=1, row=2, pady=1, padx=1,
                  sticky="w", rowspan=15, columnspan=2)
l2.grid(column=1, row=21, pady=10, padx=5, sticky="w")
save_loc.grid(column=2, row=21, padx=1, sticky="w")
space.grid(column=0, row=20, pady=1, padx=1, sticky="w")

file_count.grid(column=0, row=25, pady=10, padx=10)
statusbar.grid(column=0, row=27, pady=5, padx=5, columnspan=10, sticky=W)

text_area.focus()
logs_entry("hello")
root.mainloop()
