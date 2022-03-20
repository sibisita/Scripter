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
from netmiko import Netmiko, redispatch, ssh_exception

root = Tk()

about_this_application = '''
Hi,
This application is created for taking backup of cisco devices after logging into a jumpserver.
Source code for this is available in : https://github.com/sibisita/Scripter.git .
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
    for device in devices:
        try:
            if(device != "\n" and device[0] != " "):
                logs_entry(
                    f"**** Establishing connection to {device} ****")
                net_connect.write_channel(
                    f'ssh -o "StrictHostKeyChecking no" {deviceuser.get()}@{device.lower()}\n')
                delay_with_refresh(10)  # Wait for 10 secs to connect
                output = net_connect.read_channel()
                logs_entry(output)
                if "Password" not in output:
                    # Wait for another 10 secs to connect if no response
                    logs_entry(output)
                    delay_with_refresh(10)
                    output = net_connect.read_channel()
                if "Password" not in output:  # Wait for another 10 secs to connect if no response
                    logs_entry(output)
                    delay_with_refresh(10)
                    output = net_connect.read_channel()
                if "Password" not in output:
                    # Wait for another 10 secs to connect if no response, If no response for 40 secs this device will throw error.
                    logs_entry(output)
                    delay_with_refresh(10)
                    output = net_connect.read_channel()
                if "Password" in output:
                    logs_entry(output)
                    logs_entry("Received password prompt")
                    net_connect.write_channel(f'{devicepassword.get()}\n')
                    delay_with_refresh(10)
                    logs_entry(net_connect.find_prompt())
                    if (net_connect.find_prompt()[-1] not in [">", "#"]):
                        logs_entry(
                            f"**** Connection to {device} not Successful ****")
                        continue  # can be due to any error
                    else:
                        logs_entry(
                            f"**** Connection to {device} Successful ****")
                redispatch(net_connect, device_type="cisco_ios")
                if (net_connect.find_prompt()[-1] != "#"):
                    logs_entry(net_connect.find_prompt())
                    net_connect.write_channel("enable\n")
                    delay_with_refresh(3)
                    net_connect.write_channel(f"{enablepassword.get()}\n")
                    delay_with_refresh(10)
                    logs_entry(net_connect.find_prompt())
                with open(save_location1+f"/{device}_{datetime.now().strftime('%Y%m-%d%H-%M%S')}.log", "w+") as f1:
                    for cmd in commands:
                        f1.write(f"******** Output : {cmd} ********\n\n")
                        logs_entry(
                            f"In {device}, Executing {cmd}")
                        command_output = net_connect.send_command(cmd)
                        f1.write(command_output+"\n\n****************\n\n")
                logs_entry(net_connect.find_prompt())
                net_connect.write_channel("exit\n\n")
                delay_with_refresh(2)
                logs_entry(net_connect.find_prompt())
        except Exception as e:
            logs_entry(f"\n\nError in {device} \n {e}\n\n\n")


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

    try:
        netmiko_logic(device_list, command_list)
    except ssh_exception.NetmikoTimeoutException:
        search.configure(state="normal")
        messagebox.showerror("Jump Server not found", "Check IP or Hostname")
    except ssh_exception.NetmikoAuthenticationException:
        search.configure(state="normal")
        messagebox.showerror("Check Password", "Jump Server password error")
    end_time = datetime.now()  # Start time to calculate time taken
    completed_in = (end_time-start_time).total_seconds()
    logs_entry(f"#### Total time taken is {completed_in} secs ####")
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    subprocess.run([FILEBROWSER_PATH, os.path.normpath(save_location1)])


def delay_with_refresh(n):
    i = 0
    while(i < n):
        i += 1
        time.sleep(1)
        logs_entry("# ", end="")
    logs_entry("#")


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
    try:
        photo = PhotoImage(file=resource_path("icon.png"))
        window11.iconphoto(False, photo)
    except:
        pass
    a11 = Text(window11, height=400, width=1000)
    a11.insert(INSERT, about_this_application)
    a11.grid(column=0, row=0, pady=1, padx=1, sticky="w")


def save_in_folder():
    temp_var = filedialog.askdirectory()
    if temp_var != "":
        global save_location1
        save_location1 = temp_var
        l2.configure(text=save_location1)


def resource_path(relative_path):
    try:
        base_path = os.sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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

try:
    photo = PhotoImage(file=resource_path("icon.png"))
    root.iconphoto(False, photo)
except:
    pass

text_area.focus()


root.mainloop()
