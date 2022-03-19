# This is used to run commands directly or through a jumpserver. For taking backup.

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import os
import time
from datetime import datetime
from tkinter import messagebox
import subprocess
from netmiko import Netmiko

root = Tk()

about_this_application = '''
Hi,
This application is created for taking backup of cisco devices after logging into a jumpserver.
Source code for this is available in : https://github.com/sibisita/Multi-Search/blob/main/multi_search.py .
Instructions:
Step 1: Enter the cisco device list or IP. Make sure the hostnames entered is correct.
Step 2: Enter the commands that you want to execute on each host.
Step 3: Select the location where you want the results to be saved. Use 'Browse Save Folder' button.
Step 4: Enter the Jumpserver and device credentials.
Step 5: Press Start Execution button.
After the Execution is completed. The results location is automatically opened in windows file explorer.
In the application, you can press reset to search again.
Regards,
Sibi
'''

save_location1 = os.path.expanduser('~')


def netmiko_logic(devices, commands):
    logs_entry(
        f"**** Establishing connection to Jump Server {jumpserver.get()} ****")
    net_connect = Netmiko(device_type="linux_ssh", host=jumpserver.get(),
                          username=jumpuser.get(), password=jumppassword.get())

    logs_entry(net_connect.find_prompt())
    logs_entry("**** Connection to Jump Server Successful ****\n\n")

    logs_entry(output)
    for device in devices:
        logs_entry(
            f"**** Establishing connection to {device} ****")
        net_connect.write_channel(
            f'ssh -o "StrictHostKeyChecking no" {deviceuser.get()}@{device}\n')
        time.sleep(10)
        output = net_connect.read_channel()
        logs_entry(output)
        if "Password" in output:
            logs_entry("Received password prompt")
            net_connect.write_channel(f'{devicepassword.get()}\n')
            logs_entry(
                f"**** Connection to {device} Successful ****")


def main_logic():
    search.configure(state="disabled")

    start_time = datetime.now()  # Start time to calculate time taken

    # Extracting values from screen
    device_list = (text_area.get("1.0", "end")).lower().splitlines()
    device_list_set = list(set(device_list))
    if "" in device_list_set:
        device_list_set.remove("")
    if len(device_list_set) == 0:
        search.configure(state="normal")
        messagebox.showinfo("Device list Empty!!", 'Enter list of Devices!!')
        return
    command_list = (command_list_area.get("1.0", "end")).lower().splitlines()
    command_list_set = list(set(command_list))
    if "" in command_list_set:
        command_list_set.remove("")
    if len(command_list_set) == 0:
        search.configure(state="normal")
        messagebox.showinfo("Command list Empty!!",
                            'Enter commands to execute!!')
        return
    netmiko_logic(device_list_set, command_list_set)
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    subprocess.run([FILEBROWSER_PATH, os.path.normpath(save_location1)])


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
    "Times New Roman", 12))
jumpserver = StringVar()
jumpServerEntry = Entry(root, textvariable=jumpserver)
jumpuserLabel = Label(root, text="Jumpserver Username", font=(
    "Times New Roman", 12))
jumpuser = StringVar()
jumpuserEntry = Entry(root, textvariable=jumpuser)

jumppasswordLabel = Label(root, text="Jumpserver Password", font=(
    "Times New Roman", 12))
jumppassword = StringVar()
jumppasswordEntry = Entry(root,  textvariable=jumppassword,
                          show='*')

deviceuserLabel = Label(root, text="Device Username", font=(
    "Times New Roman", 12)).grid(row=10, column=3)
deviceuser = StringVar()
deviceuserEntry = Entry(root, textvariable=deviceuser).grid(row=10, column=4)

devicepasswordLabel = Label(root, text="Device Password", font=(
    "Times New Roman", 12)).grid(row=11, column=3)
devicepassword = StringVar()
devicepasswordEntry = Entry(root,  textvariable=devicepassword,
                            show='*').grid(row=11, column=4)

enableLabel = Label(root, text="Cisco enable Password", font=(
    "Times New Roman", 12)).grid(row=12, column=3)
enablepassword = StringVar()
enablepasswordEntry = Entry(root,  textvariable=enablepassword,
                            show='*').grid(row=12, column=4)

command_list_area = scrolledtext.ScrolledText(
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
search = Button(root, text="Start Execution", bg="green",
                fg="yellow", font=100, command=main_logic)

# grid position
text_area.grid(column=0, row=2, pady=1, padx=1,
               sticky="w", rowspan=15, columnspan=2)
about.grid(column=4, row=0, padx=5, sticky=N+E)
command_list_area.grid(column=1, row=2, pady=1, padx=1,
                       sticky="w", rowspan=15, columnspan=2)
l2.grid(column=1, row=21, pady=10, padx=5, sticky="w")
save_loc.grid(column=2, row=21, padx=1, sticky="w")
space.grid(column=0, row=20, pady=1, padx=1, sticky="w")
search.grid(column=4, row=15)
file_count.grid(column=0, row=25, pady=10, padx=10)
statusbar.grid(column=0, row=27, pady=5, padx=5, columnspan=10, sticky=W)

jumpServerLabel.grid(row=4, column=3)
jumpServerEntry.grid(row=4, column=4)
jumpuserLabel.grid(row=5, column=3)
jumpuserEntry.grid(row=5, column=4)
jumppasswordLabel.grid(row=6, column=3)
jumppasswordEntry.grid(row=6, column=4)


text_area.focus()
logs_entry("hello")


root.mainloop()
