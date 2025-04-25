import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from memory_manager import MemoryManager
from memory_visualizer import MemoryVisualizer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MemoryVisualizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dynamic Memory Visualizer")
        self.geometry("800x550")

        self.heap_size = 1024
        self.memory_manager = MemoryManager(self.heap_size)
        self.visualizer = MemoryVisualizer(self.heap_size)
        self.command_history = []

        self.create_widgets()

    def create_widgets(self):
        self.input_label = ctk.CTkLabel(self, text="💻 Command (malloc 100 as name / free name or address):", font=("JetBrains Mono", 14))
        self.input_label.pack(pady=(20, 5))

        self.command_entry = ctk.CTkEntry(self, width=400, font=("Consolas", 12))
        self.command_entry.pack(pady=(0, 10))

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.run_button = ctk.CTkButton(self.button_frame, text="▶ Run", command=self.run_command, width=100)
        self.run_button.pack(side="left", padx=10)

        self.visualize_button = ctk.CTkButton(self.button_frame, text="📊 Visualize", command=self.visualize_heap, width=100)
        self.visualize_button.pack(side="left", padx=10)

        self.reset_button = ctk.CTkButton(self.button_frame, text="🔄 Reset", command=self.reset_heap, width=100)
        self.reset_button.pack(side="left", padx=10)

        self.history_button = ctk.CTkButton(self.button_frame, text="📜 History", command=self.show_history, width=100)
        self.history_button.pack(side="left", padx=10)

        self.log_label = ctk.CTkLabel(self, text="📄 Log Output", font=("JetBrains Mono", 13, "bold"))
        self.log_label.pack(pady=(20, 5))

        self.log_output = ctk.CTkTextbox(self, height=200, font=("Consolas", 11))
        self.log_output.pack(padx=20, fill="both", expand=True)
        self.log_output.insert("end", "🚀 Memory Visualizer Initialized!\n")

    def run_command(self):
        raw = self.command_entry.get().strip()
        self.command_history.append((datetime.now().strftime("%H:%M:%S"), raw))

        parts = raw.split()
        if not parts:
            return

        try:
            if parts[0] == "malloc":
                size = int(parts[1])
                name = None
                if len(parts) == 4 and parts[2] == "as":
                    name = parts[3]
                address = self.memory_manager.malloc(size, name)
                if address is not None:
                    self.log(f"[+]: Allocated {size} bytes at address {address} {'as ' + name if name else ''}")
                    self.show_custom_alert("Success", f"Allocated {size} bytes at address {address}", "info")
            elif parts[0] == "free":
                key = parts[1]
                address = int(key) if key.isdigit() else self.memory_manager.get_address_by_name(key)
                if address is None:
                    raise ValueError("Invalid address or name")
                self.memory_manager.free(address)
                self.log(f"[+]: Freed memory at address {address}")
                self.show_custom_alert("Freed", f"Memory at {key} is freed", "info")
            else:
                self.log("[-]: Invalid command")
                self.show_custom_alert("Error", "Invalid command", "error")
        except Exception as e:
            self.log(f"[!] Error: {str(e)}")
            self.show_custom_alert("Error", str(e), "error")

    def visualize_heap(self):
        heap = self.memory_manager.get_heap_status()
        fragmentation = self.memory_manager.detect_fragmentation()
        leaks = self.memory_manager.detect_memory_leaks()
        if leaks:
            self.log("[!]: Memory leaks detected")
        else:
            self.log("[=]: No memory leaks detected")
        self.visualizer.visualize(heap, fragmentation, leaks)
        self.log("[=]: Heap Visualization Updated")

    def reset_heap(self):
        self.memory_manager = MemoryManager(self.heap_size)
        self.log("[~]: Heap Reset Complete")
        self.show_custom_alert("Reset", "Heap memory has been reset.", "warn")

    def show_history(self):
        history_window = ctk.CTkToplevel(self)
        history_window.title("📜 Command History")
        history_window.geometry("400x300")
        history_output = ctk.CTkTextbox(history_window, font=("Consolas", 11))
        history_output.pack(expand=True, fill="both", padx=10, pady=10)
        for timestamp, command in self.command_history:
            history_output.insert("end", f"[{timestamp}] {command}\n")

    def show_custom_alert(self, title, message, alert_type="info"):
        alert = ctk.CTkToplevel(self)
        alert.geometry("300x150")
        alert.title(title)
        alert.grab_set()

        icon = {"info": "ℹ️", "warn": "⚠️", "error": "🔥"}.get(alert_type, "🔔")
        ctk.CTkLabel(alert, text=f"{icon} {title}", font=("JetBrains Mono", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(alert, text=message, wraplength=250, font=("Consolas", 12)).pack(pady=(0, 20))
        ctk.CTkButton(alert, text="OK", command=alert.destroy).pack()

    def log(self, message):
        self.log_output.insert("end", message + "\n")
        self.log_output.see("end")

if __name__ == "__main__":
    app = MemoryVisualizerApp()
    app.mainloop()
