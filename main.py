# -*- coding: utf-8 -*-
from os import walk
from pprint import pprint

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

from DataObject import JsonArray

# Main logic and layout
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.active_sel = {
            'count': '',
            'index': 0,
            'full_name': '',
            'name': '',
            'number': '',
            'stats': '',
            'various': ''
        }
        self.list = {}
        self.await_load = False
        self.btn = {}
        self.curr_loc = ''
        self.form = {}
        self.mode = tk.IntVar(value=0)  # errorlog value active
        self.mode_opts = {}
        self.content = {}
        
        # ===================== (Main Menu + controls)
        self.active_sel['location'] = tk.Label(self.master, text='Location : {0}'.format(self.curr_loc))
        self.mode_opts['mode1'] = tk.Radiobutton(self.master, text='Data Viewer', value=0, variable=self.mode, command=self.sm)
        self.mode_opts['mode2'] = tk.Radiobutton(self.master, text='Data editor', value=1, variable=self.mode, command=self.sm)
        
        self.active_sel['location'].grid(row=0, column=0, columnspan=2, sticky='w')
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
        self.active_sel['stats'] = tk.Label(self.master, text='Total : {0} records'.format(self.active_sel['count']))
        self.active_sel['stats'].grid(row=9, column=0, columnspan=7, sticky='w')
        self.refresh()
        
    def sm(self):
        backup = self.curr_loc
        self.curr_loc = dialog.askdirectory()
        if self.curr_loc:
            _, _, filenames = next(walk(self.curr_loc))
            for file in filenames:
                if 'json' in file:
                    print(self.curr_loc + '/' + file)
                    self.list['values'][file] = self.curr_loc + '/' + file
                    self.list['box'].insert('end', file)
            self.active_sel['index'] = ''
            self.active_sel['name'] = ''
            self.active_sel['full_name'] = ''
            self.await_load = True
        else:
            if backup:
                self.curr_loc = backup  # reverting to previous value
        self.refresh()            

    def refresh(self):
        if self.await_load:
            self.form['content'].delete(*self.form['content'].get_children())
            if self.mode.get() == 0:
                if self.active_sel['index']:
                    self.content = JsonArray(self.curr_loc+'/'+self.active_sel['value'])
                    self.form['content']['columns'] = self.content.field
                    for column in self.content.field:
                        self.form['content'].heading(column, text=column, anchor='center')
                        self.form['content'].column(column, stretch="no")
                    for row in self.content.content:
                        temp = []
                        for column, value in row.items():
                            temp.append(value)
                        self.form['content'].insert("", "end", values=temp)
            elif self.mode.get() == 1:
                print('editor mode not yet implemented')

    def on_select(self, evt):
        w = evt.widget
        if w.curselection():
            if w == self.list['box']:  # click in file list
                self.active_sel['index'] = int(w.curselection()[0])
                self.active_sel['value'] = w.get(self.active_sel['index'])
                # TODO: need to change a lot more
        self.refresh()

    def prev(self):
        if self.content.content:
            if self.active_sel['index'] > 1:
                self.active_sel['index'] -= 1

    def next(self):
        if self.content.content:
            if self.active_sel['index'] < len(self.content.content):
                self.active_sel['index'] += 1

    def control(self):
        print('onthing really here yet')

    def export(self):
        if self.content.content:
            if self.mode.get():  # file mode, export to directory
                final_loc = dialog.askdirectory()
            else:
                final_loc = dialog.asksaveasfile(mode='w', defaultextension=".txt")
            if self.curr_loc != final_loc and final_loc:
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