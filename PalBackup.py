import os
import shutil
import tkinter as tk
from tkinter import Button, filedialog, messagebox, Canvas

serverDirpath = 'C:\\Program Files(x86)\\Steam\\steamapps\\common\\PalServer\\Pal\\Saved\\SaveGames\\0'
backup_periodic_active = False
backup_periodic_id = None
status = "red"

#Server Path Insertion
def InsertServerPath():
    serverPath = filedialog.askdirectory()
    serverPath = os.path.join(serverDirpath, serverPath)

    with open(os.getcwd() + '\PalBackup.txt', 'w') as f:
        f.write(serverPath)

#List Files to compare with the original folder to make sure 
#there is nothing missing and only the files in it get backed up
def listdir(path):
    try:
        return os.listdir(path)
    except PermissionError:
        messagebox.showerror("Erro de Permissão", "Sem permissão para aceder a este diretório.")
        return []

#Backup Server
def BackupServer():
    with open(os.getcwd() + '\PalBackup.txt', 'r') as f:
        serverFilepath = f.readline()

    if(os.path.exists(os.getcwd() + '\\Backup') == False):
        shutil.copytree(serverFilepath, os.getcwd() + '\\Backup')
    else:
        if(listdir(serverFilepath) == listdir(os.getcwd() + '\\Backup')):
            shutil.rmtree(os.getcwd() + '\\Backup', ignore_errors=True)
            shutil.copytree(serverFilepath, os.getcwd() + '\\Backup')
            print("Backup Successful!")
        else:
            messagebox.showerror("Backup Error", "The server folder is missing files")

#Backup toggle
def backup_periodically_toggle():
    global backup_periodic_active
    if backup_periodic_active:
        stop_periodic_backup()
        status = "red"
    else:
        start_periodic_backup()
        status = "green"
    canvas.itemconfig(circle, fill = status)

#Start Periodic Backup
def start_periodic_backup():
    global backup_periodic_active
    global backup_periodic_id

    backup_periodic_active = True
    backup_periodic_id = root.after(30000, backup_periodically)

    messagebox.showinfo("Backup Periodic", "Backup Periodic Started!")
    

#Stop Periodic Backup
def stop_periodic_backup():
    global backup_periodic_active
    global backup_periodic_id

    backup_periodic_active = False

    root.after_cancel(backup_periodic_id)
    messagebox.showinfo("Backup Periodic", "Backup Periodic Stopped!")

#Periodic Backup (every 30 seconds)
def backup_periodically():
    BackupServer()
    global backup_periodic_active
    if backup_periodic_active:
        root.after(30000, backup_periodically)
        print("Backup Successful!")

#Tkinter main interface creation
root = tk.Tk()
root.title("PalBackup")
root.geometry("180x150")
canvas = Canvas()

#if the txt file in the current directory exists, show the button
if(os.path.exists(os.getcwd() + '\PalBackup.txt')):
    #Server Path Insertion Button
    insertServerPath = Button(root, text="Insert Server Path", command=InsertServerPath)
    insertServerPath.pack(side=tk.TOP, anchor=tk.W)

    #Backup Server Button
    backupServer = Button(root, text="Backup Server", command=BackupServer)
    backupServer.pack(side=tk.TOP, anchor=tk.W)

    #Backup Server Periodically Button
    button_backup_periodically = Button(root, text="Backup Server Periodically", command=backup_periodically_toggle)
    button_backup_periodically.pack(side=tk.TOP, anchor=tk.W)

    #Exit Button
    exitButton = Button(root, text="Exit", command=root.destroy)
    exitButton.pack(side=tk.TOP, anchor=tk.W)

    #Periodic backup status light
    circle = canvas.create_oval(10,10,17,17,outline ="black",fill =status ,width = 2)
    canvas.pack()
else:
    InsertServerPath()
    insertServerPath = Button(root, text="Insert Server Path", command=InsertServerPath)
    insertServerPath.pack(side=tk.TOP, anchor=tk.W)

    backupServer = Button(root, text="Backup Server", command=BackupServer)
    backupServer.pack(side=tk.TOP, anchor=tk.W)

    button_backup_periodically = Button(root, text="Backup Server Periodically", command=backup_periodically_toggle)
    button_backup_periodically.pack(side=tk.TOP, anchor=tk.W)

    exitButton = Button(root, text="Exit", command=root.destroy)
    exitButton.pack(side=tk.TOP, anchor=tk.W)

    circle = canvas.create_oval(10,10,17,17,outline ="black",fill =status ,width = 2)
    canvas.pack()

    

root.mainloop()

#Made By JohnnyPeni