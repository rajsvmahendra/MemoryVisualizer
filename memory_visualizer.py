import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MemoryVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Visualizer")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")

        # Main frame
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(pady=10)

        # Input Frame
        input_frame = tk.LabelFrame(main_frame, text="Memory Settings", padx=10, pady=10, bg="white", font=("Arial", 12, "bold"))
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Total Memory Size (MB):", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.memory_size_entry = tk.Entry(input_frame)
        self.memory_size_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Process Size (MB):", bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.process_size_entry = tk.Entry(input_frame)
        self.process_size_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=5)

        self.allocate_button = tk.Button(button_frame, text="Allocate Memory", command=self.allocate_memory, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15)
        self.allocate_button.grid(row=0, column=0, padx=10, pady=5)

        self.deallocate_button = tk.Button(button_frame, text="Deallocate Memory", command=self.deallocate_memory, bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=15)
        self.deallocate_button.grid(row=0, column=1, padx=10, pady=5)

        # Status Bar
        self.status_label = tk.Label(root, text="Memory Usage: 0 MB Used", bg="#222", fg="white", font=("Arial", 10, "bold"), relief="sunken", anchor="w")
        self.status_label.pack(fill="x", pady=5)

        # Figure for visualization
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

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
            self.update_status()

            messagebox.showinfo("Success", f"Process of size {process_size} MB allocated!")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")

    def deallocate_memory(self):
        if not self.memory_blocks:
            messagebox.showerror("Error", "No processes to deallocate!")
            return

        removed_process = self.memory_blocks.pop(0)  # Remove the first allocated process
        self.update_chart()
        self.update_status()
        messagebox.showinfo("Success", f"Process of size {removed_process} MB deallocated!")

    def update_chart(self):
        self.ax.clear()
        used_memory = sum(self.memory_blocks)
        free_memory = self.total_memory - used_memory

        labels = ['Used Memory', 'Free Memory']
        sizes = [used_memory, free_memory]
        colors = ['#ff9999', '#99ff99']

        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, wedgeprops={'edgecolor': 'black'})
        self.ax.set_title("Memory Allocation Status")

        self.canvas.draw()

    def update_status(self):
        used_memory = sum(self.memory_blocks)
        self.status_label.config(text=f"Memory Usage: {used_memory} MB Used")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryVisualizer(root)
    root.mainloop()
