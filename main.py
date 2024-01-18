import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox

def get_installed_drivers():
    try:
        powershell_cmd = '''
        Get-WmiObject Win32_PnPSignedDriver | Select-Object DeviceName, DriverVersion | Format-Table -AutoSize | Out-String
        '''
        installed_drivers = subprocess.check_output(['powershell', '-Command', powershell_cmd], text=True)
        return installed_drivers
    except subprocess.CalledProcessError as e:
        return f"Error while getting installed drivers: {e}"

def get_available_updates():
    try:
        powershell_cmd = '''
        Get-HotFix | Where-Object { $_.Description -like '*driver*' } | Sort-Object -Property InstalledOn -Descending | Select-Object -First 1 | Format-Table -AutoSize | Out-String
        '''
        available_update = subprocess.check_output(['powershell', '-Command', powershell_cmd], text=True)
        return available_update
    except subprocess.CalledProcessError as e:
        return f"Error while getting available updates: {e}"

def check_for_updates(result_text):
    result_text.delete(1.0, tk.END)
    
    installed_drivers = get_installed_drivers()
    available_update = get_available_updates()

    result_text.insert(tk.END, "Installed Drivers:\n")
    result_text.insert(tk.END, f"{installed_drivers}\n")

    result_text.insert(tk.END, "Available Update:\n")
    result_text.insert(tk.END, f"{available_update}\n")

    if "No updates are installed" in available_update:
        result_text.insert(tk.END, "Your drivers are up to date.\n")
    else:
        result_text.insert(tk.END, "Update available. Do you want to update your drivers?\n")
        update_button.config(state=tk.NORMAL)

def update_drivers(result_text):
    result_text.delete(1.0, tk.END)
    
    try:
        powershell_cmd = '''
        Write-Host "Simulating driver update..."
        '''
        update_result = subprocess.check_output(['powershell', '-Command', powershell_cmd], text=True)
        result_text.insert(tk.END, f"{update_result}\n")
        result_text.insert(tk.END, "Drivers updated successfully.\n")
        update_button.config(state=tk.DISABLED)
    except subprocess.CalledProcessError as e:
        result_text.insert(tk.END, f"Error while updating drivers: {e}\n")

def main():
    global update_button

    window = tk.Tk()
    window.title("Driver Update Tool")

    # Pole tekstowe dla informacji
    result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
    result_text.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

    # Przycisk do sprawdzania sterowników i aktualizacji
    check_button = tk.Button(window, text="Check for Updates", command=lambda: check_for_updates(result_text))
    check_button.grid(column=0, row=1, padx=10, pady=10, sticky="W")

    # Przycisk do aktualizacji sterowników
    update_button = tk.Button(window, text="Update Drivers", command=lambda: update_drivers(result_text), state=tk.DISABLED)
    update_button.grid(column=1, row=1, padx=10, pady=10, sticky="E")

    window.mainloop()

if __name__ == "__main__":
    main()
