import tkinter as tk


def getTextEntry(master,text,**kwargs):
    t_var = tk.StringVar()
    t_var.set(text)
    entry = tk.Entry(master,textvariable=t_var,state="readonly",readonlybackground="white",**kwargs)
    return entry