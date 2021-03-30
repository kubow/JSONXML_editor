# -*- coding: utf-8 -*-
from os import walk

# Compatibility win <> lnx
try:
    import Tkinter as tk
    import Tkinter.filedialog as dialog
    import Tkinter.ttk as ttk
    print('using big tkinter (linux way)')
except ImportError:
    import tkinter as tk
    import tkinter.filedialog as dialog
    import tkinter.ttk as ttk
    print('using small tkinter (windows way)')

from DataObject import JsonObject

# Main logic and layout
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.active = {
            'count': '',  # number of files count
            'index': 0,  # currentindex of selection
            'location': '',
            'mode': tk.IntVar(value=0),  # errorlog value active
            'stats': '',  # information panel
            'value': '',  # 
        }
        self.await_load = False
        self.btn = {}
        self.data = {}  # holds currently loaded object
        self.form = {}  # holds all GUI components (except radiobuttons and buttons)
        self.list = {}
        self.mode_opts = {}
        
        # ===================== (Main Menu + controls)
        self.form['location'] = tk.Label(self.master, text='Location : {0}'.format(self.active['location']))
        self.mode_opts['mode1'] = tk.Radiobutton(self.master, text='Data Viewer', value=0, variable=self.active['mode'], command=self.sm)
        self.mode_opts['mode2'] = tk.Radiobutton(self.master, text='Data editor', value=1, variable=self.active['mode'], command=self.sm)
        
        self.form['location'].grid(row=0, column=0, columnspan=2, sticky='w')
        self.mode_opts['mode1'].grid(row=0, column=4)
        self.mode_opts['mode2'].grid(row=0, column=5)
        
        # ===================== (Button Menu)
        self.btn['open'] = tk.Button(self.master, text='open', command=self.sm)
        self.btn['expt'] = tk.Button(self.master, text='export', command=self.export)
        self.btn['prev'] = tk.Button(self.master, text='<', command=self.prev)
        self.btn['save'] = tk.Button(self.master, text='save')  # editing not yet implemented
        self.btn['next'] = tk.Button(self.master, text='>', command=self.next)
        self.btn['exit'] = tk.Button(self.master, text='quit', command=self.quit)
        self.btn['open'].grid(row=1, column=0, pady=5, sticky='nsew')
        self.btn['expt'].grid(row=1, column=1, pady=5, sticky='nsew')
        self.btn['prev'].grid(row=1, column=2, pady=5, sticky='nsew')
        self.btn['save'].grid(row=1, column=3, pady=5, sticky='nsew')
        self.btn['next'].grid(row=1, column=4, pady=5, sticky='nsew')
        self.btn['exit'].grid(row=1, column=5, pady=5, sticky='nsew')
        
        # ===================== (Tables list)
        self.list['box'] = tk.Listbox(self.master, height=3)
        self.list['box'].bind('<<ListboxSelect>>', self.on_select)
        self.list['scroll'] = tk.Scrollbar(self.master, orient='vertical')
        self.list['box']['yscrollcommand'] = self.list['scroll'].set
        self.list['scroll']['command'] = self.list['box'].yview
        self.list['box'].grid(row=2, column=0, rowspan=7, columnspan=1, sticky='nse', pady=(5, 5), padx=(5, 5))
        self.list['scroll'].grid(row=2, column=0, rowspan=7, columnspan=1, sticky='nse', pady=(5, 5), padx=(5, 5))
        self.list['values'] = {}
        
        # ===================== (Fields list)
        self.form['content'] = ttk.Treeview(master, show='headings', selectmode='browse', height=4)
        self.form['content'].grid(row=2, column=1, columnspan=7, rowspan=7)
        self.form['content'].bind("<Return>", lambda e: self.on_select())

        # ===================== (Comment line)
        self.form['stats'] = tk.Label(self.master, text='Total : {0} records'.format(self.active['count']))
        self.form['stats'].grid(row=9, column=0, columnspan=7, sticky='w')
        self.refresh()
        
    def sm(self):
        backup = self.active['location']
        self.active['location'] = dialog.askdirectory()
        if self.active['location']:
            _, _, filenames = next(walk(self.active['location']))
            for file in filenames:
                if 'json' in file:
                    # print(self.active['location'] + '/' + file)
                    self.list['values'][file] = self.active['location'] + '/' + file
                    self.list['box'].insert('end', file)
            self.active['index'] = ''
            self.await_load = True
        else:
            if backup:
                self.active['location'] = backup  # reverting to previous value
        self.refresh()            

    def refresh(self):
        if self.await_load:
            self.form['content'].delete(*self.form['content'].get_children())
            if self.active['mode'].get() == 0:
                if self.active['index'] or self.active['index'] == 0:  # must be item selected
                    self.data = JsonObject(self.active['location']+'/'+self.active['value'])
                    # self.data = JsonObject()  # TODO: need to change a lot more
                    self.form['content']['columns'] = self.data.field_list
                    for column in self.data.field_list:
                        self.form['content'].heading(column, text=column, anchor='center')
                        self.form['content'].column(column, stretch="no")
                    temp = []
                    if self.data.type == 'arr':
                        for row in self.data.content:
                            for column, value in row.items():
                                temp.append(value)
                    elif self.data.type == 'dic':
                        for column, value in self.data.content.items():
                            temp.append(value)
                    self.form['content'].insert("", "end", values=temp)
            elif self.active['mode'].get() == 1:
                print('editor mode not yet implemented')

    def on_select(self, evt):
        w = evt.widget
        if w.curselection():
            if w == self.list['box']:  # click in file list
                self.active['index'] = int(w.curselection()[0])
                self.active['value'] = w.get(self.active['index'])
                self.await_load = True
        self.refresh()

    def prev(self):
        if self.data.content:
            if self.active['index'] > 1:
                self.active['index'] -= 1

    def next(self):
        if self.data.content:
            if self.active['index'] < len(self.data.content):
                self.active['index'] += 1

    def control(self):
        print('onthing really here yet')

    def export(self):
        if self.data.content:
            if self.mode.get():  # file mode, export to directory
                final_loc = dialog.askdirectory()
            else:
                final_loc = dialog.asksaveasfile(mode='w', defaultextension=".txt")
            if self.active['location'] != final_loc and final_loc:
                if self.mode.get():
                    self.contacts_lib.dic.export(final_loc)
                else:
                    self.contacts_lib.dic.merge(final_loc)

    def quit(self):
        self.master.destroy()

    
def editor():
    root = tk.Tk()
    root.title('JSON database folder administrator')
    root.resizable(10, 10)
    # root.geometry('1200x900')
    #root.columnconfigure(0, weight=2)
    #root.columnconfigure(1, weight=1)
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    editor()