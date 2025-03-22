import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MemoryVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Visualizer")
        self.root.geometry("600x500")

        # Input Fields
        self.memory_size_label = tk.Label(root, text="Total Memory Size (MB):")
        self.memory_size_label.pack()
        self.memory_size_entry = tk.Entry(root)
        self.memory_size_entry.pack()

        self.process_size_label = tk.Label(root, text="Process Size (MB):")
        self.process_size_label.pack()
        self.process_size_entry = tk.Entry(root)
        self.process_size_entry.pack()

        # Buttons for allocation and deallocation
        self.allocate_button = tk.Button(root, text="Allocate Memory", command=self.allocate_memory)
        self.allocate_button.pack(pady=5)

        self.deallocate_button = tk.Button(root, text="Deallocate Memory", command=self.deallocate_memory)
        self.deallocate_button.pack(pady=5)

        # Figure for visualization
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

        # Memory Storage
        self.memory_blocks = []
        self.total_memory = 0

    def allocate_memory(self):
        try:
            if self.total_memory == 0:
                self.total_memory = int(self.memory_size_entry.get())  # Set total memory from input

            process_size = int(self.process_size_entry.get())

            used_memory = sum(self.memory_blocks)
            free_memory = self.total_memory - used_memory

            if process_size > free_memory:
                messagebox.showerror("Error", "Not enough memory available!")
                return

            self.memory_blocks.append(process_size)
            self.update_chart()

            messagebox.showinfo("Success", f"Process of size {process_size} MB allocated!")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")

    def deallocate_memory(self):
        if not self.memory_blocks:
            messagebox.showerror("Error", "No processes to deallocate!")
            return

        removed_process = self.memory_blocks.pop(0)  # Remove the first allocated process
        self.update_chart()
        messagebox.showinfo("Success", f"Process of size {removed_process} MB deallocated!")

    def update_chart(self):
        self.ax.clear()
        used_memory = sum(self.memory_blocks)
        free_memory = self.total_memory - used_memory

        labels = ['Used Memory', 'Free Memory']
        sizes = [used_memory, free_memory]

        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['red', 'green'])
        self.ax.set_title("Memory Allocation Status")

        self.canvas.draw()

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryVisualizer(root)
    root.mainloop()