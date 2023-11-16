import os
import pandas as pd
from tkinter import (
    Tk,
    Label,
    Button,
    filedialog,
    Entry,
    StringVar,
    Listbox,
    Scrollbar,
    MULTIPLE,
    messagebox,
)
from tkinter.ttk import Progressbar
from datetime import datetime


def get_output_file_path(input_file, output_directory, output_prefix, index):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{file_name}_{output_prefix}_{index + 1}.csv"
    output_path = (
        output_directory or f"entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    return os.path.join(output_path, output_file)


def split_csv(
    root,
    input_files,
    chunk_size=100000,
    output_directory=None,
    output_prefix="output_file",
    progress_var=None,
):
    total_files = len(input_files)
    progress_step = 100 / total_files

    for file_idx, input_file in enumerate(input_files, start=1):
        df = pd.read_csv(input_file)
        num_chunks = (len(df) - 1) // chunk_size + 1

        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(df))
            output_file_path = get_output_file_path(
                input_file, output_directory, output_prefix, i
            )
            df.iloc[start_idx:end_idx].to_csv(output_file_path, index=False)

        # Update progress bar
        progress_value = int(file_idx * progress_step)
        progress_var.set(progress_value)
        root.update_idletasks()

    messagebox.showinfo("CSV Splitter", "CSV splitting completed!")


def create_output_directory(input_file, output_directory):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    default_output_path = f"entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_path = os.path.join(os.path.dirname(input_file), default_output_path)

    if output_directory:
        output_path = os.path.join(output_directory, default_output_path)

    os.makedirs(output_path, exist_ok=True)
    return output_path


def select_files(entry_list):
    file_paths = filedialog.askopenfilenames(
        title="Select CSV Files", filetypes=[("CSV files", "*.csv")]
    )
    entry_list.delete(0, "end")

    for file_path in file_paths:
        entry_list.insert("end", file_path)


def select_directory(entry):
    directory = filedialog.askdirectory(title="Select Output Directory")
    entry.delete(0, "end")
    entry.insert(0, directory)


def validate_csv_files(input_files):
    for file_path in input_files:
        if not file_path.lower().endswith(".csv"):
            return False
    return True


def split_csv_gui():
    root = Tk()
    root.title("Entries File Spliter")

    # Set custom icon
    icon_path = "resource/icon.ico"
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    file_label = Label(root, text="SELECT CSV FILES:")
    file_label.pack()

    file_listbox = Listbox(root, selectmode=MULTIPLE, width=50)
    file_listbox.pack()

    file_button = Button(
        root, text="BROWSE FILES", command=lambda: select_files(file_listbox)
    )
    file_button.pack()

    directory_label = Label(root, text="Select Output Directory (Optional):")
    directory_label.pack()

    directory_entry = Entry(root, width=50)
    directory_entry.pack()

    directory_button = Button(
        root, text="Browse", command=lambda: select_directory(directory_entry)
    )
    directory_button.pack()

    chunk_label = Label(root, text="Chunk Size (rows):")
    chunk_label.pack()

    chunk_entry = Entry(root)
    chunk_entry.pack()

    prefix_label = Label(root, text="Output Prefix:")
    prefix_label.pack()

    prefix_entry = Entry(root)
    prefix_entry.pack()

    progress_var = StringVar()
    progress_bar = Progressbar(
        root, orient="horizontal", length=300, mode="determinate", variable=progress_var
    )
    progress_bar.pack()

    def start_processing():
        input_files = file_listbox.get(0, "end")
        output_directory = directory_entry.get()
        chunk_size = int(chunk_entry.get()) if chunk_entry.get() else 100000
        output_prefix = prefix_entry.get() if prefix_entry.get() else "output_file"

        # Validate CSV files
        if not validate_csv_files(input_files):
            messagebox.showerror("Error", "Please select valid CSV files.")
            return

        try:
            # Create the output directory
            output_directory = create_output_directory(input_files[0], output_directory)

            # Perform CSV splitting
            split_csv(
                root,
                input_files,
                chunk_size,
                output_directory,
                output_prefix,
                progress_var,
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        root.destroy()

    process_button = Button(root, text="Start Processing", command=start_processing)
    process_button.pack()

    root.mainloop()


if __name__ == "__main__":
    split_csv_gui()
