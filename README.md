The provided tool is a file integrity checker with a graphical user interface (GUI) that allows users to monitor a specified directory for changes in file integrity. Here's an overview of how the tool works:

1. **User Interface (GUI):**
   - The script uses Tkinter to create a GUI application.
   - Users can browse and select a directory, initiate an integrity check, clear the output, and exit the application.

2. **Baseline Creation:**
   - The `BaselineManager` class handles the creation and management of a baseline for the selected directory.
   - When the user runs the tool for the first time or after baseline verification, a baseline file (`baseline.json`) is created. This file contains the hashes of all files in the specified directory.

3. **File Monitoring:**
   - The `FileChangeMonitor` class monitors the selected directory for changes by comparing the current state with the baseline.
   - It identifies three types of changes: added files, modified files, and deleted files.
   - For added files, it calculates and displays the size of the file.
   - For modified files, it calculates and displays that the file has been modified.
   - For deleted files, it indicates that the file has been deleted.

4. **Integrity Verification:**
   - The `BaselineManager.verify_baseline_integrity` method checks if the baseline file (`baseline.json`) has been tampered with.
   - It does this by recalculating the hash of the baseline and comparing it with the stored hash in the baseline file.

5. **Alerts and Reports:**
   - The `FileChangeMonitor` class sends desktop notifications using `plyer.notification` for detected file changes.
   - It generates a compliance report (`report.txt`) summarizing the changes, including modified, added, and deleted files.

6. **Output Display:**
   - The output of the integrity checks, analysis, and alerts are displayed in the GUI's scrolled text widget.

7. **Usage:**
   - Users run the tool by selecting a directory, initiating the integrity check, and reviewing the results in the GUI.
   - The tool informs users about any changes in file integrity and provides details about added, modified, and deleted files.

8. **Bubble Sort for Report Generation:**
   - The `bubble_sort` function is used for sorting file paths in the compliance report.

9. **Notification for Baseline Tampering:**
   - If the baseline file integrity is compromised, a desktop notification is triggered to alert the user.

10. **Exception Handling:**
    - The tool includes basic exception handling, such as checking if the baseline file exists before attempting to load it.

In summary, the tool helps users monitor and maintain the integrity of files in a specified directory by creating baselines, comparing them to the current state, and notifying users of any detected changes. The GUI provides a user-friendly interface for interacting with the tool and viewing the results.
