import tkinter as tk



def ConvertWithDefault(func, default):
    def inner(n):
        try:
            return func(n)
        except:
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
    check_button = tk.Entry(master,
                            textvariable=variable,
                            **kwargs)
    variable.set(func_v(config[key]))
    return check_button


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
