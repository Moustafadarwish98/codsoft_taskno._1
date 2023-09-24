from tkinter import *
from tkinter import messagebox
from turtle import TurtleScreen

BG_COLOUR = "#1ABC9C"
DONE = "#28B463"
BUTTON_COLOR = "#76D7C4"


def check_saved():
    """Checking if there is a previously saved list with the name entered and asking the user
    if they want to open it or create a new list."""
    try:
        with open(file=f"./{title_of_list}", mode="r", encoding="utf-8") as file:
            open_existing = messagebox.askyesno(title="List exists", message="There is an existing list with"
                                                                             " the same name do you want to open"
                                                                             " it? or create new list?")
            if open_existing:
                saved_list = file.readlines()
                for element in saved_list:
                    list_items.insert(END, element)
                for index, listbox_entry in enumerate(list_items.get(0, END)):
                    if "✔️" in str(listbox_entry):
                        list_items.itemconfig(index, fg=DONE)

    except FileNotFoundError:
        pass


def save_list_items():
    save = messagebox.askyesno(title="save", message="Do you want to save list?")
    if save:
        messagebox.showinfo(message=f"List will be saved with this name:\n"
                                    f"{title_of_list}")
        elements = list(list_items.get(0, END))
        for i in range(0, len(elements)):
            if "\n" not in elements[i]:
                elements[i] = elements[i] + "\n"
        with open(file=f"./{title_of_list}", mode="w", encoding="utf-8") as file_to_save:
            for item in elements:
                file_to_save.writelines(item)


def add_item():
    """To add items to the list"""
    item = entry.get()
    if item == "":
        messagebox.showinfo(title="Nothing to add", message="Please type item you want to add.")
    else:
        list_items.insert(END, f"{list_items.index(END) + 1}.{item}")
        entry.delete(0, END)
        entry.focus()


def delete_item():
    """Delete items from the list and update items order in list."""
    temp = list_items.index(ANCHOR)
    text = list_items.get(temp)
    item = list_items.get(ANCHOR)
    if temp == 0 and text == "":
        messagebox.showerror(title="Error", message="List is empty.\nPlease insert items in"
                                                    " list.")
    elif text == "":
        messagebox.showinfo(title="Nothing to delete", message="Please choose item"
                                                               " you want to delete.")
    else:
        sure = messagebox.askyesno(title="Check", message=f"You sure you want to delete {item}.")
        if sure:
            list_items.delete(ANCHOR)
            for list_indices, list_entry in enumerate(list_items.get(0, END)):
                order = str(list_entry).split(".")
                if int(order[0]) > temp:
                    list_items.delete(list_indices)
                    list_items.insert(list_indices, str(int(order[0]) - 1) + "." + order[1])
                if "✔️" in str(list_entry):
                    list_items.itemconfig(list_indices, fg=DONE)


def check_item():
    """To mark item as done in list"""
    checked_index = list_items.index(ANCHOR)
    checked = list_items.get(checked_index)
    if checked != "":
        list_items.delete(ANCHOR)
        if "\n" in checked:
            checked = checked.replace("\n", " ✔️ \n")
        else:
            checked = checked + " ✔️"
        list_items.insert(checked_index, f"{checked}")
        list_items.itemconfig(checked_index, fg=DONE)

    else:
        messagebox.showinfo(title="Nothing selected", message="Please select"
                                                              " item to mark it.")


def update_items():
    """To update items in list"""
    item_index = list_items.index(ANCHOR)
    old_item = list_items.get(item_index)
    if old_item == "" and item_index == 0:
        messagebox.showerror(title="Error", message="List is empty.\nPlease insert items in"
                                                    " list.")
    elif old_item == "":
        messagebox.showinfo(title="Nothing selected.", message="Please choose item"
                                                               " you want to update.")
    else:
        new_item = screen.textinput(title="Update item", prompt="Enter new item to"
                                                                " replace current item.")
        list_items.delete(item_index)
        list_items.insert(item_index, f"{item_index + 1}" + "." + new_item)


def clear_list_items():
    """To delete all items in list"""
    answer = messagebox.askyesno(title="Check", message="Are you sure you want "
                                                        "to delete all items.")
    if answer:
        list_items.delete(0, END)


"""Window setup"""
window = Tk()
window.title("To-Do list")
window.minsize(width=800, height=750)
window.config(padx=50, pady=20, bg=BG_COLOUR)

"""Frame and Canvas creation, Canvas needed to embed turtle graphics library with Tkinter"""
frame = Frame(window)
canvas = Canvas(frame)

"""Creation on screen object, prompting user to enter title of To-do-list."""
screen = TurtleScreen(canvas)
title_of_list = screen.textinput(title="To-Do-List title.", prompt="Enter title for your list"
                                                                   " (enter title only): \n"
                                                                   "Example: 2023 To-Do list,"
                                                                   " today To-Do list, "
                                                                   "August To-Do list..etc").title()
frame.grid(row=1, column=0, rowspan=2, columnspan=2)

"""Labels setup"""
title_label = Label(text=f"{title_of_list} To-Do-List", bg=BG_COLOUR, highlightthickness=0)
title_label.config(padx=70, pady=10, font=("Times New Roman", 60, "italic"), anchor="center")
title_label.grid(row=0, column=0, sticky="N")

"""List box"""
list_items = Listbox(frame, bd=10, fg="black", font=("boulder", 12), cursor="target",
                     highlightthickness=0, width=80, height=22, selectbackground=BG_COLOUR,
                     activestyle=NONE
                     )
list_items.grid(row=1, column=0, columnspan=2)

"""Buttons"""
add = Button(text="Add item", font=("Boulder", 14), bg=BUTTON_COLOR, highlightthickness=0,
             width=8, command=add_item)
delete = Button(text="Delete item", font=("Boulder", 14), bg=BUTTON_COLOR, highlightthickness=0,
                width=10, command=delete_item)
mark_as_done = Button(text="Mark as done", font=("Boulder", 14), bg=BUTTON_COLOR,
                      highlightthickness=0, width=10, command=check_item)
update_item = Button(text="Update item", font=("Boulder", 14), bg=BUTTON_COLOR,
                     highlightthickness=0, width=10, command=update_items)
clear_list = Button(text="Clear list", font=("Boulder", 14), bg=BUTTON_COLOR,
                    highlightthickness=0, width=10, command=clear_list_items)
save_list = Button(text="Save list", font=("Boulder", 14), bg=BUTTON_COLOR,
                   highlightthickness=0, width=10, command=save_list_items)
save_list.place(x=630, y=615)
clear_list.place(x=20, y=615)
mark_as_done.place(x=480, y=615)
delete.place(x=170, y=615)
add.place(x=10, y=560)
update_item.place(x=330, y=615)

"""Scroll bar"""
scrollbar = Scrollbar(frame, orient=VERTICAL)
list_items.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=list_items.yview)
scrollbar.grid(row=1, column=2, sticky=N + S)

"""Entry box"""
entry = Entry(width=40, font=("boulder", 21))
entry.insert(END, string="Type here")
entry.place(x=115, y=560)

check_saved()

window.mainloop()
