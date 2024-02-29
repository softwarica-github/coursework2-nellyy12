import os
import json
import tkinter as tk
from tkinter import filedialog, scrolledtext
from enum import Enum
from plyer import notification
from hashlib import sha3_256

class ChangeType(Enum):
    MODIFIED = "Modified"
    ADDED = "Added"
    DELETED = "Deleted"

class FileAnalyzer:
    def __init__(self, file_path, output_text):
        self.file_path = file_path
        self.output_text = output_text

    def analyze_added_file(self):
        self.output_text.insert(tk.END, f"Analyzing additions for file: {self.file_path}\n")
        self.output_text.insert(tk.END, f"- Added {self.get_file_size()} bytes.\n")
        self.output_text.insert(tk.END, "Addition analysis completed.\n\n")
        root.update()

    def analyze_deleted_file(self):
        self.output_text.insert(tk.END, f"Analyzing deletions for file: {self.file_path}\n")
        self.output_text.insert(tk.END, "- Deleted.\n")
        self.output_text.insert(tk.END, "Deletion analysis completed.\n\n")
        root.update()

    def analyze_modified_file(self):  # Added method
        self.output_text.insert(tk.END, f"Analyzing modifications for file: {self.file_path}\n")
        self.output_text.insert(tk.END, "- Modified.\n")
        self.output_text.insert(tk.END, "Modification analysis completed.\n\n")
        root.update()

    def get_file_size(self):
        return os.path.getsize(self.file_path)

class BaselineManager:
    @staticmethod
    def create_baseline(directory, baseline_file):
        baseline = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = BaselineManager.calculate_hash(file_path)
                baseline[file_path] = file_hash

        with open(baseline_file, 'w') as f:
            json.dump(baseline, f, indent=4)

    @staticmethod
    def calculate_hash(file_path):
        with open(file_path, 'rb') as f:
            sha3_hash = sha3_256()
            for data in iter(lambda: f.read(8192), b''):
                sha3_hash.update(data)
            return sha3_hash.hexdigest()

    @staticmethod
    def load_baseline(baseline_file):
        if os.path.getsize(baseline_file) > 0:
            with open(baseline_file) as f:
                baseline = json.load(f)
            return baseline
        else:
            return {}

    @staticmethod
    def verify_baseline_integrity(baseline_file):
        with open(baseline_file, 'r') as f:
            stored_hash = f.readline().strip()

        with open(baseline_file, 'rb') as f:
            sha3_hash = sha3_256()
            f.readline()
            for data in iter(lambda: f.read(8192), b''):
                sha3_hash.update(data)
            calculated_hash = sha3_hash.hexdigest()

        if calculated_hash != stored_hash:
            print("Baseline file has been tampered with.")
            notification.notify(
                title='Baseline Tampering Alert',
                message='The baseline file has been tampered with.',
                timeout=10
            )
        else:
            print("Baseline file integrity verified.")

class FileChangeMonitor:
    @staticmethod
    def monitor_directory(directory, baseline, baseline_file, output_text):
        modified_files = []
        new_files = []
        deleted_files = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    if file_path in baseline:
                        stored_hash = baseline[file_path]
                        current_hash = BaselineManager.calculate_hash(file_path)
                        if current_hash != stored_hash:
                            modified_files.append(file_path)
                            FileAnalyzer(file_path, output_text).analyze_modified_file()  # Corrected line
                    else:
                        new_files.append(file_path)
                        FileAnalyzer(file_path, output_text).analyze_added_file()  # Added line

        for file_path in baseline.keys():
            if not os.path.exists(file_path):
                deleted_files.append(file_path)
                FileAnalyzer(file_path, output_text).analyze_deleted_file()

        BaselineManager.create_baseline(directory, baseline_file)

        if not any((modified_files, new_files, deleted_files)):
            print("Integrity maintained. No changes detected.")
        else:
            print("Integrity violated. Changes detected:")
            if modified_files:
                print("Modified files:")
                for file_path in modified_files:
                    print(file_path)
                    FileAnalyzer(file_path, output_text).analyze_modified_file()
            if new_files:
                print("New files created:")
                for file_path in new_files:
                    print(file_path)
                    FileAnalyzer(file_path, output_text).analyze_added_file()
            if deleted_files:
                print("Deleted files:")
                for file_path in deleted_files:
                    print(file_path)
                    FileAnalyzer(file_path, output_text).analyze_deleted_file()

                FileChangeMonitor.send_alert(modified_files, new_files, deleted_files)
                FileChangeMonitor.generate_compliance_report(modified_files, new_files, deleted_files)

    @staticmethod
    def send_alert(modified_files, new_files, deleted_files):
        title = 'File Change Alert'
        message = ''

        if modified_files:
            message += 'Modified files:\n'
            for file_path in modified_files:
                message += file_path + '\n'

        if new_files:
            message += 'New files created:\n'
            for file_path in new_files:
                message += file_path + '\n'

        if deleted_files:
            message += 'Deleted files:\n'
            for file_path in deleted_files:
                message += file_path + '\n'

        notification.notify(
            title=title,
            message=message,
            timeout=10
        )

    @staticmethod
    def generate_compliance_report(modified_files, new_files, deleted_files):
        report = "Conformity Report:\n\n"

        if modified_files:
            bubble_sort(modified_files)
            report += "Modified files:\n"
            for file_path in modified_files:
                report += f"- {file_path}\n"
            report += "\n"

        if new_files:
            bubble_sort(new_files)
            report += "New files created:\n"
            for file_path in new_files:
                report += f"- {file_path}\n"
            report += "\n"

        if deleted_files:
            bubble_sort(deleted_files)
            report += "Deleted files:\n"
            for file_path in deleted_files:
                report += f"- {file_path}\n"
            report += "\n"

        with open('report.txt', 'w') as f:
            f.write(report)

        print("Compliance report generated.")

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

class GUIApplication:
    def __init__(self, master):
        self.master = master
        master.title("File Integrity Checker")
        master.geometry("700x600")
        master.resizable(False, False)
        self.selected_directory = None  # Store selected directory
        self.create_widgets()

    def create_widgets(self):
        # Heading
        heading_label = tk.Label(self.master, text="File Integrity Checker", font=("Helvetica", 16, "bold"))
        heading_label.pack(pady=10)

        # File Browser
        browse_button = tk.Button(self.master, text="Browse Directory", command=self.browse_directory)
        browse_button.pack(pady=10)

        # Output Display
        self.output_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=75, height=22)
        self.output_text.pack(pady=10)

        # Run Button
        run_button = tk.Button(self.master, text="Run Integrity Check", command=self.run_integrity_check_btn)
        run_button.pack(pady=10)

        # Clear Button
        clear_button = tk.Button(self.master, text="Clear Output", command=self.clear_output)
        clear_button.pack(pady=10)

        # Exit Button
        exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy)
        exit_button.pack(pady=10)

    def browse_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.selected_directory = directory_path  # Update selected directory
            self.output_text.insert(tk.END, f"Selected Directory: {directory_path}\n\n")

    def run_integrity_check_btn(self):
        if self.selected_directory:
            self.output_text.insert(tk.END, "Running Integrity Check...\n")

            baseline_file = 'baseline.json'
            baseline = {}

            if os.path.exists(baseline_file):
                BaselineManager.verify_baseline_integrity(baseline_file)
                baseline = BaselineManager.load_baseline(baseline_file)
            else:
                BaselineManager.create_baseline(self.selected_directory, baseline_file)
                baseline = BaselineManager.load_baseline(baseline_file)

            FileChangeMonitor.monitor_directory(self.selected_directory, baseline, baseline_file, self.output_text)

            self.output_text.insert(tk.END, "\nIntegrity Check Completed.\n")
        else:
            self.output_text.insert(tk.END, "Please select a directory using the 'Browse Directory' button.\n")

    def clear_output(self):
        self.output_text.delete('1.0', tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApplication(root)
    root.mainloop()