import tkinter as tk

from tkinter import ttk, PhotoImage

from PIL import Image,ImageTk

from utils import vfile


class PlayerProgressBar(ttk.Scale):
    style = None
    def __init__(self, master=None, **kw):
        self.slider_img = ImageTk.PhotoImage(Image.open(vfile.getResourcePath('resource/favicon.png')).resize((16, 16), Image.ANTIALIAS))
        self.style or self.__createStyle(master)
        self.variable = kw.pop('variable', tk.DoubleVar(master))
        ttk.Scale.__init__(self, master, variable=self.variable, **kw)
        self._style_name = '{}.custom.Horizontal.TScale'.format(self)
        self['style'] = self._style_name

    def __createStyle(self, master):
        style = ttk.Style(master)
        style.element_create('custom.Horizontal.Scale.slider', 'image', self.slider_img)
        style.layout('custom.Horizontal.TScale',
                     [('Scale.focus',
                       {'expand': '1',
                        'sticky': 'nswe',
                        'children': [('Horizontal.Scale.trough',
                                      {'expand': '1', 'sticky': 'nswe',
                                       'children': [(
                                           'Horizontal.Scale.track',
                                           {'sticky': 'we'}), (
                                           'custom.Horizontal.Scale.slider',
                                           {'side': 'left',
                                            'sticky': ''})]})]})])
        PlayerProgressBar.style = style