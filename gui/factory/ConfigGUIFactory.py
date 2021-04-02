import tkinter as tk
import traceback
from tkinter import ttk


def ConvertWithDefault(func, default):
    def inner(n):
        try:
            return func(n)
        except:
            traceback.print_exc()
            return default
    return inner


def getConfigWriter(config, key, vari, func, funv):
    def inner(*args):
        config[key] = func(vari.get())
        vari.set(funv(config[key]))
    return inner


def getInput(master, config, key, func_c, func_v,
             **kwargs):
    variable = tk.StringVar()
    variable.trace_variable("w", getConfigWriter(config,
                                                 key,
                                                 variable,
                                                 func_c,
                                                 func_v))
    input_entry = tk.Entry(master,
                           textvariable=variable,
                           **kwargs)
    variable.set(func_v(config[key]))
    return input_entry


def getInputWithButton(master, config, key, func_c, func_v,
                       input_kwargs=None, button_kwargs=None):
    input_kwargs = input_kwargs or {}
    button_kwargs = button_kwargs or {}
    variable = tk.StringVar()
    input_entry = tk.Entry(master,
                           textvariable=variable,
                           **input_kwargs)
    update_button = ttk.Button(master,
                               command=getConfigWriter(config,
                                                       key,
                                                       variable,
                                                       func_c,
                                                       func_v),
                               **button_kwargs)
    variable.set(func_v(config[key]))
    return input_entry, update_button


def getCheckButton(master, text, config, key, func_c, func_v,
                   **kwargs):
    variable = tk.IntVar()
    check_button = tk.Checkbutton(master,
                                  text=text,
                                  variable=variable,
                                  command=getConfigWriter(config,
                                                          key,
                                                          variable,
                                                          func_c,
                                                          func_v),
                                  **kwargs)
    variable.set(func_v(config[key]))
    return check_button


def getBoxSelector(master, config, key, values, func_c, func_v,
                   **kwargs):
    variable = tk.StringVar()
    variable.trace_variable("w", getConfigWriter(config,
                                                 key,
                                                 variable,
                                                 func_c,
                                                 func_v))
    box_selector = ttk.Combobox(master,
                                textvariable=variable,
                                **kwargs)
    box_selector['values'] = tuple(values)
    variable.set(func_v(config[key]))
    return box_selector
