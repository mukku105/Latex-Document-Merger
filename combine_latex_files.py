'''
    Author : Muksam Limboo
    Description : A Python based GUI application that combines multiple .tex files into a single .tex file.
    Date : August 23, 2022 23:50
'''

import os
from tkinter import ANCHOR, RIGHT, Y, Scrollbar, Tk, filedialog, Label, Button, Listbox, SINGLE, END, BOTH, font, messagebox

root = Tk()
root.title("Latex Document Merger")

root.geometry("600x360")

class DragDropListbox(Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, **kw):
        kw['selectmode'] = SINGLE
        Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i


def select_folder():
    folder_selected = filedialog.askdirectory()

    if folder_selected:
        dir_select_btn.config(text="Folder Selected > " + folder_selected)
    else :
        dir_select_btn.config(text="Click to Select a Folder")

    list_of_latex_files = []
    for file in os.listdir(folder_selected):
        if file.endswith(".tex"):
            list_of_latex_files.append(file)

    tex_file_listbox.delete(0, END)
    for i, name in enumerate(list_of_latex_files):
        tex_file_listbox.insert(END, folder_selected+"/"+name)
    tex_file_listbox.pack(fill=BOTH, expand=True)


def extract_usepackage(item):
    list_packages = set()
    tex_file = open(item)

    for line in tex_file:
        if "\\usepackage" in line:
            list_packages.add(line.strip().replace(" ", ""))

    tex_file.close()

    return list_packages

def extract_author(item):
    author_details = ""
    tex_file = open(item)

    for line in tex_file:
        if "\\author" in line:
            author_details = line[line.rindex("{")+1:line.rindex("}")]
            break
    return author_details

def extract_macros(item):
    list_macros = []
    tex_file = open(item)

    for line in tex_file:
        if "\\begin{document}" in line:
            break
        elif "\\newcommand" in line or "\\renewcommand" in line:
            list_macros.append(line.strip() + "\t%" + item[item.rindex("/") + 1 : ] + "\n")

    return list_macros

def merge_files():
    list_packages = set()
    author_details = []
    document_title = ""
    list_macros = []

    print("File merge sequence: ")

    if not os.path.exists("output_tex"):
        os.makedirs("output_tex")

    combined_tex = open("output_tex/combined.tex", "w")
    i = 1
    for items in tex_file_listbox.get(0, END) :
        print(str(i) + ". " + items)
        i += 1

        for package in extract_usepackage(items):
            list_packages.add(package)
        author_details.append(extract_author(items))

        for macros in extract_macros(items):
            list_macros.append(macros)

    selected_file = tex_file_listbox.get(ANCHOR)

    if not selected_file:
        messagebox.showinfo("Error", "Please select a file inorder to use its Title in the combined .tex file")
    
    tex_file = open(selected_file)
    for line in tex_file:
        if "\\title" in line:
            document_title = line
            break
    tex_file.close()

    combined_tex.write("\\documentclass{article}\n\n")

    combined_tex.write("\n".join(list_packages))
    combined_tex.write("\n\n")

    combined_tex.write("\n".join(list_macros))
    combined_tex.write("\n\n")

    combined_tex.write(document_title)
    combined_tex.write("\\author{" + ", ".join(author_details) + "}\n\n")
    combined_tex.write("\\begin{document}\n")
    combined_tex.write("\\maketitle\n")

    for item in tex_file_listbox.get(0, END):
        flg = False
        tex_body_file = open(item)
        combined_tex.write("\n\n%=============================================================")
        combined_tex.write("\n%" + item[item.rindex("/") + 1 : ] + "\n")
        for line in tex_body_file:
            if "\\begin{document}" in line:
                flg = True
                continue
            elif "\\end{document}" in line:
                break

            if flg:
                if "\\maketitle" in line:
                    continue
                combined_tex.write(line)

    combined_tex.write("\n")
    combined_tex.write("\\end{document}")
    combined_tex.close()

    print("Packages Used: " + str(list_packages))
    print("Author Names: " + str(author_details))

    messagebox.showinfo("Success", ".tex Files Merged Successfully ! \n'combined.tex'")


dir_select_btn = Button(root, text="Click to Select a Folder", bg="blue", fg="white", font=font.Font(weight='bold'), padx=10, pady=10, command=select_folder)

label_arrange_text = Label(root, text="Arrange Files below to merge them in sequence. And Select the file whose Title is to be used.", padx=10, pady=10)
tex_file_listbox = DragDropListbox(root)
merge_btn = Button(root, text="Merge", command=merge_files, bg="green", fg="white", font=font.Font(weight='bold'), padx=10, pady=10)
Scrollbar = Scrollbar(root)

label_code_author = Label(root, text="Latex Document Merger, Author: Muksam Limboo, August 23 - 2022 \nA Python based GUI application that combines multiple .tex files into a single .tex file.", font=font.Font(size="8"), pady="10")

tex_file_listbox.config(yscrollcommand=Scrollbar.set)
Scrollbar.config(command=tex_file_listbox.yview)
Scrollbar.pack(side=RIGHT, fill=Y)

label_code_author.pack()

dir_select_btn.pack()
label_arrange_text.pack()
tex_file_listbox.pack(fill=BOTH, expand=True)
merge_btn.pack()

root.mainloop()