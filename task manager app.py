import tkinter as tk
from tkinter import messagebox
import pickle
import os
from datetime import datetime

class Task:
    def __init__(self, description, deadline):
        self.description = description
        self.deadline = deadline

    def __repr__(self):
        return f"{self.description} - Due by {self.deadline}"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filepath = 'tasks.pkl'

    def add_task(self, description, deadline):
        try:
            deadline_datetime = datetime.strptime(deadline.strip(), '%Y-%m-%d')
            task = Task(description, deadline_datetime.strftime('%Y-%m-%d'))
            self.tasks.append(task)
            return "Task added."
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return "Invalid date format. Use YYYY-MM-DD."

    def remove_task(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                self.tasks.remove(task)
                return "Task removed."
        return "Task not found."

    def get_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open(self.filepath, 'wb') as file:
            pickle.dump(self.tasks, file)
        return "Tasks saved."

    def load_tasks(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'rb') as file:
                loaded_tasks = pickle.load(file)
                self.tasks = []
                for item in loaded_tasks:
                    if isinstance(item, str):  # Check if the loaded task is a string
                        parts = item.split(' - Due by ')
                        if len(parts) == 2:
                            description, deadline = parts
                            self.tasks.append(Task(description, deadline))
                        else:
                            print(f"Error loading task: '{item}' - Invalid format.")
                    elif isinstance(item, Task):
                        self.tasks.append(item)
        return "Tasks loaded."

def add_task():
    description = task_entry.get()
    deadline = deadline_entry.get()
    result = task_manager.add_task(description, deadline)
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    refresh_task_list()
    messagebox.showinfo("Task Addition", result)

def remove_task():
    selected_item = task_listbox.get(tk.ANCHOR)
    if selected_item:  # Check if an item is actually selected
        task_description = selected_item.split(' - Due by ')[0]
        result = task_manager.remove_task(task_description)
        refresh_task_list()
        messagebox.showinfo("Task Removal", result)

def refresh_task_list():
    task_listbox.delete(0, tk.END)
    tasks = task_manager.get_tasks()
    for task in tasks:
        task_listbox.insert(tk.END, repr(task))

def save_tasks():
    result = task_manager.save_tasks()
    messagebox.showinfo("Save Tasks", result)

def load_tasks():
    result = task_manager.load_tasks()
    refresh_task_list()
    messagebox.showinfo("Load Tasks", result)

root = tk.Tk()
root.title("Task Manager")
root.geometry("400x400")

task_manager = TaskManager()

# Labels for entry fields
label_task = tk.Label(root, text="Task Description:")
label_task.pack()
task_entry = tk.Entry(root, width=50)
task_entry.pack()

label_deadline = tk.Label(root, text="Due Date (YYYY-MM-DD):")
label_deadline.pack()
deadline_entry = tk.Entry(root, width=50)
deadline_entry.pack()

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

remove_button = tk.Button(root, text="Remove Selected Task", command=remove_task)
remove_button.pack()

save_button = tk.Button(root, text="Save Tasks", command=save_tasks)
save_button.pack()

load_button = tk.Button(root, text="Load Tasks", command=load_tasks)
load_button.pack()

task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.pack(fill=tk.BOTH, expand=True)

task_manager.load_tasks()  # Load tasks at startup
refresh_task_list()

root.mainloop()
