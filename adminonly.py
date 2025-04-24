import subprocess
import sys
import time
import os
import random
import gzip
import zipfile
import tarfile
from colorama import Fore, Back, Style, init
import math
import pdb
import psutil
import netifaces
import warnings

# Initialize colorama for Windows support
init(autoreset=True)

# Global variable to control debug mode
debug_mode = False

my_list = ["help", "exit", "toggle_debug", "memory", "color", "return", "netinterface", "powercfg", "dir", "cd", "edit_file", "read_file", "rm" ] # Define my_list here

def extended_help(command):
    """Provides extended help for a given command."""
    help_messages = {
        "cd": "cd <path>\n\nChanges the current working directory to the specified <path>.\nUse 'cd ..' to go up one directory.\nUse 'cd' or 'cd ~' to return to your home directory.",
        "dir": "dir <path>\n\nLists the contents (files and directories) of the specified <path>.\nIf no <path> is provided, it lists the contents of the current directory.",
        "powercfg": "powercfg /l\n\n(Windows only) Lists the available power schemes on the system.",
        "memory": "memory\n\nDisplays the memory usage (Resident Set Size and Virtual Memory Size) of the current Python process.",
        "toggle_debug": "toggle_debug\n\nToggles the debug mode on or off. When enabled, may provide more detailed output or logging.",
        "return": "return\n\nExecutes the 'start.py' script.",
        "netinterface": "netinterface\n\nDisplays information about the network interfaces on the system, including MAC address, IPv4 and IPv6 addresses.",
        "ef": "ef <filename>\n\nOpens the specified <filename> for rudimentary editing within the shell.\nType new lines or modify existing ones. Use '.done' to save and exit.\nUse '-<line_number>' to delete a specific line.",
        "rf": "rf <filename> or cat <filename>\n\nDisplays the content of the specified <filename> on the console.",
        "rm": "rm [-f] <filename> or delete_file [-f] <filename>\n\nDeletes the specified <filename>.\nUse the '-f' flag to force deletion without confirmation (use with caution!).",
        "help": "help\n\nDisplays a list of available commands.",
        "exit": "exit\n\nCloses the current shell or command interface.",
        "clear": "clear\n\nClears the terminal screen.",
        
    }
    if command in help_messages:
        print(Fore.CYAN + f"\n--- Extended Help for '{command}' ---")
        print(Fore.WHITE + help_messages[command])
        print(Fore.CYAN + "---------------------------------------\n")
    else:
        print(Fore.RED + f"No extended help available for '{command}'.")


def create_directories_recursive(directory_path, exist_ok=True):
    """Creates directories recursively."""
    try:
        os.makedirs(directory_path, exist_ok=exist_ok)
        print(Fore.GREEN + f"Successfully created directory(ies): '{directory_path}'")
    except FileExistsError:
        if not exist_ok:
            print(Fore.YELLOW + f"Warning: Directory '{directory_path}' already exists (exist_ok=False).")
        else:
            print(Fore.CYAN + f"Directory '{directory_path}' already exists.")
    except PermissionError:
        print(Fore.RED + f"Error: Permission denied to create directory(ies) '{directory_path}'.")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")



def change_directory(path):
    """Changes the current working directory."""
    try:
        os.chdir(path)
        print(Fore.GREEN + f"Changed directory to: {os.getcwd()}")
    except FileNotFoundError:
        print(Fore.RED + f"Error: No such file or directory: {path}")
    except NotADirectoryError:
        print(Fore.RED + f"Error: Not a directory: {path}")
    except PermissionError:
        print(Fore.RED + f"Error: Permission denied: {path}")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

def list_directory_admin():
    """Lists the contents of a specified directory."""
    path = input(Fore.WHITE + "Enter the directory path to list: ")
    try:
        items = os.listdir(path)
        print(Fore.YELLOW + f"\n--- Contents of '{path}' ---")
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                print(Fore.WHITE + f"  File: {item}")
            elif os.path.isdir(full_path):
                print(Fore.CYAN + f"  Directory: {item}/")
            else:
                print(Fore.LIGHTBLACK_EX + f"  Other: {item}")
        print(Fore.YELLOW + "-----------------------------\n")
    except FileNotFoundError:
        print(Fore.RED + f"Error: Directory not found: {path}")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

def list_power_schemes_admin():
    """Lists the available power schemes."""
    try:
        result = subprocess.run(['powercfg', '/l'], capture_output=True, text=True, check=True)
        print(Fore.YELLOW + "\n--- Available Power Schemes ---")
        print(Fore.WHITE + result.stdout)
        print(Fore.YELLOW + "-------------------------------\n")
    except FileNotFoundError:
        print(Fore.RED + "Error: 'powercfg' command not found. This is a Windows-specific command.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error executing 'powercfg /l': {e}")
        print(Fore.WHITE + e.stderr)

def show_memory_usage_command():
    """Displays the memory usage of the current process."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(Fore.YELLOW + "Memory Usage:")
    print(Fore.YELLOW + f"  Resident Set Size (RSS): {memory_info.rss / (1024 * 1024):.2f} MB (physical memory used)")
    print(Fore.YELLOW + f"  Virtual Memory Size (VMS): {memory_info.vms / (1024 * 1024):.2f} MB (address space reserved)")

def toggle_debug_mode():
    """Toggles the debug mode."""
    global debug_mode
    debug_mode = not debug_mode
    status = "enabled" if debug_mode else "disabled"
    print(Fore.YELLOW + f"Debug mode is now {status}.")

def execute_file(filename):
    try:
        result = subprocess.run(["python", filename], capture_output=True, text=True, check=True)
        print(Fore.GREEN + f"Successfully executed {filename}.")
        print("Output:")
        print(result.stdout)
    except FileNotFoundError:
        print(Fore.RED + f"Error: File not found: {filename}")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error executing {filename}: {e}")
        print("Error Output:")
        print(e.stderr)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

def print_list_in_columns(data, cols):
    if not data:
        return

    rows = math.ceil(len(data) / cols)
    col_data = [data[i::rows] for i in range(rows)]
    col_widths = [max(len(item) for item in col) + 2 for col in col_data] # Add some extra spacing

    for row_index in range(rows):
        for col_index in range(cols):
            if row_index < len(col_data[col_index]):
                item = col_data[col_index][row_index]
                print(f"{Fore.YELLOW}{item:<{col_widths[col_index]}}", end="")
        print()
import os
from colorama import Fore

def read_file_command(filename):
    """Reads and displays the content of a file."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
            print(Fore.YELLOW + f"\n--- Content of '{filename}' ---")
            print(Fore.WHITE + content)
            print(Fore.YELLOW + "-----------------------------\n")
    except FileNotFoundError:
        print(Fore.RED + f"Error: File not found: {filename}")
    except PermissionError:
        print(Fore.RED + f"Error: Permission denied to read: {filename}")
    except Exception as e:
        print(Fore.RED + f"An error occurred while reading '{filename}': {e}")

def edit_file_command(filename):
    """Rudimentarily edits a file within the shell."""
    try:
        with open(filename, 'r+') as f:
            content = f.readlines()
            print(Fore.YELLOW + f"\n--- Editing '{filename}' ---")
            print(Fore.WHITE + "Current content:")
            for i, line in enumerate(content):
                print(f"{i+1}: {line.strip()}")
            print(Fore.CYAN + "\nEnter new lines or modify existing ones. Type '.done' when finished.")
            print(Fore.CYAN + "To delete a line, enter its number prefixed with '-'.")

            new_content = []
            while True:
                user_input = input(Fore.WHITE + ">> ")
                if user_input.lower() == '.done':
                    break
                elif user_input.startswith('-') and user_input[1:].isdigit():
                    try:
                        line_number_to_delete = int(user_input[1:]) - 1
                        if 0 <= line_number_to_delete < len(new_content) + len(content):
                            if line_number_to_delete < len(content):
                                print(Fore.YELLOW + f"Deleted line: {content[line_number_to_delete].strip()}")
                                content[line_number_to_delete] = None # Mark for deletion
                            else:
                                del new_content[line_number_to_delete - len(content)]
                                print(Fore.YELLOW + f"Deleted new line: {new_content[line_number_to_delete - len(content)].strip()}")
                        else:
                            print(Fore.RED + "Invalid line number.")
                    except ValueError:
                        print(Fore.RED + "Invalid input for deletion.")
                else:
                    new_content.append(user_input + '\n')

            f.seek(0)
            f.truncate()
            for line in content:
                if line is not None:
                    f.write(line)
            for line in new_content:
                f.write(line)
            print(Fore.GREEN + f"Successfully saved changes to '{filename}'.")

    except FileNotFoundError:
        print(Fore.RED + f"Error: File not found: {filename}")
    except PermissionError:
        print(Fore.RED + f"Error: Permission denied to read/write: {filename}")
    except Exception as e:
        print(Fore.RED + f"An error occurred while editing '{filename}': {e}")

def show_interfaces_admin():
    interfaces = netifaces.interfaces()
    print(Fore.YELLOW + "\n--- Network Interfaces ---")
    for iface in interfaces:
        addresses = netifaces.ifaddresses(iface)
        ipv4 = addresses.get(netifaces.AF_INET)
        ipv6 = addresses.get(netifaces.AF_INET6)
        mac = addresses.get(netifaces.AF_LINK)

        print(Fore.CYAN + f"Interface: {iface}")
        if mac:
            print(Fore.WHITE + f"  MAC Address: {mac[0]['addr']}")
        if ipv4:
            for addr_info in ipv4:
                print(Fore.GREEN + f"  IPv4 Address: {addr_info['addr']}")
                print(Fore.GREEN + f"  Netmask: {addr_info.get('netmask', 'N/A')}")
                print(Fore.GREEN + f"  Broadcast: {addr_info.get('broadcast', 'N/A')}")
        if ipv6:
            for addr_info in ipv6:
                print(Fore.BLUE + f"  IPv6 Address: {addr_info['addr']}")
                print(Fore.BLUE + f"  Netmask: {addr_info.get('netmask', 'N/A')}")
                print(Fore.BLUE + f"  Scope: {addr_info.get('scope', 'N/A')}")
        print(Fore.YELLOW + "---------------------------\n")

def delete_file_command(command_parts):
    """Deletes the specified file with an optional force flag."""
    if len(command_parts) < 2:
        print(Fore.YELLOW + "Usage: delete_file [-f] <filename> or rm [-f] <filename>")
        return

    force = False
    filename = None

    for part in command_parts[1:]:
        if part == '-f':
            force = True
        elif filename is None:
            filename = part
        else:
            print(Fore.RED + f"Error: Too many arguments: {part}")
            return

    if not filename:
        print(Fore.YELLOW + "Usage: delete_file [-f] <filename> or rm [-f] <filename>")
        return

    if not force:
        confirm = input(Fore.YELLOW + f"Are you sure you want to delete '{filename}'? (y/N): " + Fore.WHITE).lower()
        if confirm != 'y':
            print(Fore.CYAN + f"Deletion of '{filename}' cancelled.")
            return

    try:
        os.remove(filename)
        print(Fore.GREEN + f"Successfully deleted '{filename}'.")
    except FileNotFoundError:
        print(Fore.RED + f"Error: File not found: {filename}")
    except PermissionError:
        print(Fore.RED + f"Error: Permission denied to delete: {filename}")
    except Exception as e:
        print(Fore.RED + f"An error occurred while deleting '{filename}': {e}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def delete_directory_recursive(directory_path, force=False):
    """Deletes a directory."""
    if not force:
        confirm = input(Fore.YELLOW + f"Are you sure you want to delete '{directory_path}' and all its contents? (y/N): " + Fore.WHITE).lower()
        if confirm != 'y':
            print(Fore.CYAN + f"Deletion of '{directory_path}' cancelled.")
            return

    try:
        shutil.rmtree(directory_path)
        print(Fore.GREEN + f"Successfully deleted directory and its contents: '{directory_path}'")
    except FileNotFoundError:
        print(Fore.RED + f"Error: Directory not found: '{directory_path}'")
    except PermissionError:
        print(Fore.RED + f"Error: Permission denied to delete directory '{directory_path}' or its contents.")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

def create_file_command(filename):
    """Creates an empty file with the specified filename."""
    try:
        with open(filename, 'w'):
            pass  # Just open in write mode and close to create an empty file
        print(Fore.GREEN + f"Successfully created file: '{filename}'")
    except PermissionError:
        print(Fore.RED + f"Error: Permission denied to create file: '{filename}'")
    except Exception as e:
        print(Fore.RED + f"An error occurred while creating file '{filename}': {e}")

def admincommands():
    print(Fore.CYAN + "Welcome to Admin Commands")
    while True:
        user_input_command = input(Fore.WHITE + "What would you like to execute? ")
        if user_input_command == "help":
            print("\n--- Available Commands ---")
            print_list_in_columns(my_list, 3)
            print(Fore.YELLOW + "\nType 'help <command>' for more information on a specific command.")
        elif user_input_command.startswith("help "):
            command = user_input_command.split()[1]
            extended_help(command)
        elif user_input_command == "toggle_debug":
            toggle_debug_mode()
        elif user_input_command == "memory":
            show_memory_usage_command()
        elif user_input_command == "color":
            set_color()
        elif user_input_command == "return":
                execute_file("start.py")
                print("Please wait")
        elif user_input_command == "exit":
            print(Fore.RED + "Exiting Admin Commands.")
            sys.exit()
        elif user_input_command == "netinterface":
            show_interfaces_admin()
        elif user_input_command == "powercfg":
            list_power_schemes_admin()
        elif user_input_command == "clear":
            clear_screen()
        elif user_input_command == "dir":
            list_directory_admin()
        elif user_input_command.startswith("cd"): # Check if the command starts with "cd"
            parts = user_input_command.split()
            if len(parts) > 1:
                path = parts[1]
                change_directory(path)
            else:
                print(Fore.YELLOW + f"Current directory: {os.getcwd()}")
        elif user_input_command.startswith("rf") or user_input_command.startswith("cat"):
            parts = user_input_command.split()
            if len(parts) > 1:
                filename = parts[1]
                read_file_command(filename)
            else:
                print(Fore.YELLOW + "Usage: read_file <filename> or cat <filename>")
        elif user_input_command.startswith("ef"):
            parts = user_input_command.split()
            if len(parts) > 1:
                filename = parts[1]
                edit_file_command(filename)
            else:
                print(Fore.YELLOW + "Usage: edit_file <filename>")
        elif user_input_command.startswith("delete_file") or user_input_command.startswith("rm"):
            parts = user_input_command.split()
            delete_file_command(parts)
        elif user_input_command.startswith("cf"):
            warnings.warn("This command is not available", UserWarning)
        elif user_input_command.startswith("mkdir"):
            parts = user_input_command.split()
            if len(parts) > 1:
                directory_to_create = parts[1]
                create_directories_recursive(directory_to_create) # Using makedirs for convenience
            else:
                print(Fore.YELLOW + "Usage: mkdir <directory_name>")
        elif user_input_command.startswith("rmdir"):
            parts = user_input_command.split()
            if len(parts) > 1:
                directory_to_delete = parts[1]
                delete_empty_directory(directory_to_delete)
            else:
                print(Fore.YELLOW + "Usage: rmdir <directory_name>") # Using rmtree for convenience
        else:
            print(Fore.RED + "Invalid command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    admincommands()
def set_color():
    print(Fore.WHITE + "Available colors: black, red, green, yellow, blue, magenta, cyan, white")
    text_color_input = input(Fore.WHITE + "Enter text color: ").lower()
    bg_color_input = input(Fore.WHITE + "Enter background color (optional, press Enter for default): ").lower()

    text_color_code = ""
    bg_color_code = ""

    color_map = {
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }

    bg_color_map = {
        "black": Back.BLACK,
        "red": Back.RED,
        "green": Back.GREEN,
        "yellow": Back.YELLOW,
        "blue": Back.BLUE,
        "magenta": Back.MAGENTA,
        "cyan": Back.CYAN,
        "white": Back.WHITE
    }

    if text_color_input in color_map:
        text_color_code = color_map[text_color_input]
    else:
        print(Fore.RED + "Invalid text color.")
        return

    if bg_color_input in bg_color_map:
        bg_color_code = bg_color_map[bg_color_input]
    elif bg_color_input != "":
        print(Fore.RED + "Invalid background color.")
        return

    example_text = "This is an example with your chosen colors."
    print(f"{text_color_code}{bg_color_code}{example_text}{Style.RESET_ALL}")
