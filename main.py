import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import random
import string


class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")

        self.data = []  # Array to store data as objects
        self.qr_image = None  # Store the QR Code image
        self.page_1()

    def page_1(self):
        self.clear_window()

        # Header Labels
        # header_frame = tk.Frame(self.root)
        # header_frame.pack(pady=5, fill="x")

        # tk.Label(header_frame, text="Name", width=20, anchor="w",
        #          font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        # tk.Label(header_frame, text="Value", width=30, anchor="w",
        #          font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)

        self.rows_frame = tk.Frame(self.root)
        self.rows_frame.pack(pady=10)

        # Initialize with one row
        self.add_row()

        # Add Generate button
        generate_btn = tk.Button(
            self.root, text="Generate", command=self.page_2, bg="#4285F4", fg="white", padx=20)
        generate_btn.pack(pady=10)

    def page_2(self):
        self.clear_window()
        self.root.geometry("800x1000")
        # Gather inputs
        input_data = self.data
        if not input_data:
            return

        # Generate QR Code
        qr_data = "\n".join(
            f"{item['name']}: {item['value']}" for item in input_data)
        qr_code = qrcode.make(qr_data)

        # Store the image to prevent garbage collection
        self.qr_image = ImageTk.PhotoImage(qr_code)

        # Display QR Code
        qr_label = tk.Label(self.root, image=self.qr_image)
        qr_label.pack(pady=10)

        # Display table of inputs
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10)

        for i, item in enumerate(input_data):
            ttk.Label(table_frame, text=item["name"], anchor="w", width=20).grid(
                row=i, column=0, padx=5, pady=5)
            ttk.Label(table_frame, text=item["value"], anchor="w", width=30).grid(
                row=i, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        download_btn = tk.Button(button_frame, text="Download", command=lambda: self.download_qr(
            qr_code), bg="#4285F4", fg="white")
        download_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(button_frame, text="Back", command=self.page_1)
        back_btn.grid(row=0, column=1, padx=10)

    def add_row(self, name_placeholder="Name", value_placeholder="Value"):
        row_index = len(self.data)

        row_frame = tk.Frame(self.rows_frame)
        row_frame.pack(pady=5, fill="x")

        # Name Entry with placeholder
        name_entry = tk.Entry(row_frame, width=20, fg="grey")
        name_entry.grid(row=0, column=0, padx=5)
        name_entry.insert(0, name_placeholder)
        name_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(
            name_entry, name_placeholder))
        name_entry.bind("<FocusOut>", lambda e: self.add_placeholder(
            name_entry, name_placeholder))
        name_entry.bind("<KeyRelease>", lambda e: self.update_data(
            row_index, name_entry, "name"))

        # Value Entry with placeholder
        value_entry = tk.Entry(row_frame, width=30, fg="grey")
        value_entry.grid(row=0, column=1, padx=5)
        value_entry.insert(0, value_placeholder)
        value_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(
            value_entry, value_placeholder))
        value_entry.bind("<FocusOut>", lambda e: self.add_placeholder(
            value_entry, value_placeholder))
        value_entry.bind("<KeyRelease>", lambda e: self.update_data(
            row_index, value_entry, "value"))

        # Add and Remove buttons
        add_btn = tk.Button(row_frame, text="+", command=self.add_row, width=2)
        add_btn.grid(row=0, column=2, padx=5)

        remove_btn = tk.Button(
            row_frame, text="x", command=lambda: self.remove_row(row_frame, row_index), width=2)
        remove_btn.grid(row=0, column=3, padx=5)

        # Add to data array
        self.data.append({"name": "", "value": ""})

        if len(self.data) == 1:
            remove_btn.grid_remove()  # Hide remove button for the first row

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder and entry.cget("fg") == "grey":
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def remove_row(self, row_frame, row_index):
        row_frame.destroy()
        self.data.pop(row_index)

    def update_data(self, row_index, entry, field):
        value = entry.get().strip()
        if row_index < len(self.data):
            self.data[row_index][field] = value

    def download_qr(self, qr_code):
        file_name = ''.join(random.choices(
            string.ascii_letters + string.digits, k=10)) + ".png"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=file_name,
            filetypes=[("PNG Files", "*.png")]
        )
        if save_path:
            qr_code.save(save_path)
            messagebox.showinfo("Success", f"QR Code saved as {save_path}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = QRCodeApp(root)
    root.mainloop()
