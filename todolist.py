import tkinter as tk
from tkinter import messagebox, ttk


tasks = []
filter_status = "All"
displayed_task_indexes = []

def add_task():
    task_info = AddTaskDialog(root)
    root.wait_window(task_info.top)
    if task_info.task_description is not None and task_info.task_priority is not None:
        task = {
            'description': task_info.task_description,
            'status': 'pending',
            'priority': task_info.task_priority,
            'starred': False
        }
        tasks.append(task)
        update_task_text()

def delete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        actual_index = displayed_task_indexes[selected_task_index[0]]
        tasks.pop(actual_index)
        update_task_text()
    else:
        messagebox.showwarning("Warning", "You must select a task.")

def complete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        actual_index = displayed_task_indexes[selected_task_index[0]]
        tasks[actual_index]['status'] = 'completed'
        update_task_text()
    else:
        messagebox.showwarning("Warning", "You must select a task.")

def update_task_text():
    global displayed_task_indexes
    task_listbox.delete(0, tk.END)
    sorted_tasks = sorted(enumerate(tasks), key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x[1]['priority']])
    displayed_task_indexes = []
    for index, task in sorted_tasks:
        if filter_status == "All" or (filter_status == "Starred" and task.get('starred', False)) or (filter_status == task['status']):
            display_text = f"{task['description']} [{task['priority']}]"
            if task['status'] == 'completed':
                display_text += " ✔️"
            if task.get('starred', False):
                display_text += " ★"
            task_listbox.insert(tk.END, display_text)
            displayed_task_indexes.append(index)

def save_tasks():
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(f"{task['description']}|{task['status']}|{task['priority']}|{task.get('starred', False)}\n")

def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    description, status, priority, starred = parts
                else:
                    continue  
                task = {
                    'description': description,
                    'status': status,
                    'priority': priority,
                    'starred': starred == 'True'
                }
                tasks.append(task)
        update_task_text()
    except FileNotFoundError:
        pass

def filter_tasks(filter_type):
    global filter_status
    filter_status = filter_type
    update_task_text()

def star_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        actual_index = displayed_task_indexes[selected_task_index[0]]
        tasks[actual_index]['starred'] = not tasks[actual_index].get('starred', False)
        update_task_text()
    else:
        messagebox.showwarning("Warning", "You must select a task.")


class AddTaskDialog:
    def __init__(self, parent):
        
        top = self.top = tk.Toplevel(parent)
        top.title("Add Task")
        top.geometry("300x200")
        top.configure(bg="#E6F7FF")  

        self.task_description = None
        self.task_priority = None

        
        tk.Label(top, text="Task Description:", bg="#E6F7FF", fg="#333333", font=("Helvetica", 12)).pack(pady=5)
        self.task_description_entry = tk.Entry(top, width=30, font=("Helvetica", 12))
        self.task_description_entry.pack(pady=5)

       
        tk.Label(top, text="Priority:", bg="#E6F7FF", fg="#333333", font=("Helvetica", 12)).pack(pady=5)
        self.priority_combobox = ttk.Combobox(top, values=["low", "medium", "high"], state="readonly", font=("Helvetica", 12))
        self.priority_combobox.set("medium")
        self.priority_combobox.pack(pady=5)

      
        tk.Button(top, text="Add Task", command=self.ok, bg="#009688", fg="white", font=("Helvetica", 12)).pack(pady=10)

       
        tk.Button(top, text="Cancel", command=self.cancel, bg="#009688", fg="white", font=("Helvetica", 12)).pack(pady=5)

    def ok(self):
        self.task_description = self.task_description_entry.get()
        self.task_priority = self.priority_combobox.get()
        self.top.destroy()

    def cancel(self):
        self.top.destroy()


root = tk.Tk()
root.title("To-Do List")
root.geometry("600x400")
root.configure(bg="#FAFAFA")  


sidebar_frame = tk.Frame(root, width=200, bg="#FFFFFF")  
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)


sidebar_title = tk.Label(sidebar_frame, text="Filters", bg="#FFFFFF", fg="#333333", font=("Helvetica", 16))
sidebar_title.pack(pady=10)


filters = ["All", "Starred"]
for filter in filters:
    filter_button = tk.Button(sidebar_frame, text=filter, bg="#EEEEEE", fg="#333333", relief=tk.FLAT, font=("Helvetica", 12), command=lambda f=filter: filter_tasks(f))
    filter_button.pack(fill=tk.X, padx=20, pady=5)



main_frame = tk.Frame(root, bg="#FAFAFA")  
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


tasks_label = tk.Label(main_frame, text="Tasks", bg="#FAFAFA", fg="#333333", font=("Helvetica", 16))
tasks_label.pack(pady=10)


task_listbox = tk.Listbox(main_frame, bg="#FFFFFF", fg="#333333", font=("Helvetica", 12), selectbackground="#B2DFDB")
task_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)


button_frame = tk.Frame(main_frame, bg="#FAFAFA")
button_frame.pack(fill=tk.X, padx=20, pady=10)


add_button = tk.Button(button_frame, text="Add Task", command=add_task, bg="#009688", fg="white", relief=tk.FLAT, font=("Helvetica", 12))
add_button.pack(side=tk.LEFT, padx=5)


delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task, bg="#009688", fg="white", relief=tk.FLAT, font=("Helvetica", 12))
delete_button.pack(side=tk.LEFT, padx=5)


complete_button = tk.Button(button_frame, text="Complete Task", command=complete_task, bg="#009688", fg="white", relief=tk.FLAT, font=("Helvetica", 12))
complete_button.pack(side=tk.LEFT, padx=5)

star_button = tk.Button(button_frame, text="Star Task", command=star_task, bg="#009688", fg="white", relief=tk.FLAT, font=("Helvetica", 12))
star_button.pack(side=tk.LEFT, padx=5)


root.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), root.destroy()])

load_tasks()


root.mainloop()
