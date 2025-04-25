<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
=======
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
matplotlib.use('TkAgg')  # Force backend
>>>>>>> e740f02 ( Fixed visualization unpack bug + enhanced GUI log + memory manager improvements)

class MemoryVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Visualizer")
        self.root.geometry("600x500")

<<<<<<< HEAD
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
=======
    def visualize(self, heap, fragmentation=None, memory_leaks=None):
        fig, ax = plt.subplots(figsize=(12, 2))
        ax.set_xlim(0, self.heap_size)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_title("Heap Memory Visualization", fontsize=14)

        i = 0
        while i < len(heap):
            start = i
            if heap[i] is not None:
                while i < len(heap) and heap[i] is not None:
                    i += 1
                color = "green"
            else:
                while i < len(heap) and heap[i] is None:
                    i += 1
                color = "lightgray"
            ax.add_patch(mpatches.Rectangle((start, 0), i - start, 1, color=color))

        # Draw memory leak labels
        if memory_leaks:
            for addr, (size, name) in memory_leaks.items():
                label = f"{name} ({addr})" if name else str(addr)
                ax.text(addr + size / 2, 0.5, label, ha='center', va='center', fontsize=8, color='black')

        # Draw free blocks (Fragmentation)
        if fragmentation:
            for start, size in fragmentation:
                ax.add_patch(mpatches.Rectangle((start, 0.5), size, 0.5, color='lightblue', alpha=0.6))
                ax.text(start + size / 2, 1.1, f"Free {size}", ha='center', va='center', fontsize=8, color='black')

        ax.legend(handles=[
            mpatches.Patch(color='green', label='Allocated'),
            mpatches.Patch(color='lightgray', label='Free'),
            mpatches.Patch(color='lightblue', label='Free Block (Fragmented)'),
        ])

        plt.tight_layout()
        fig.canvas.manager.window.attributes('-topmost', 1)
        plt.show()
>>>>>>> e740f02 ( Fixed visualization unpack bug + enhanced GUI log + memory manager improvements)
