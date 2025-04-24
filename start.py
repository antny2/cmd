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
import signal  

# Initialize colorama for Windows support
init(autoreset=True)

def loading_bar(total_iterations, current_iteration):
    bar_length = 30
    progress = float(current_iteration) / float(total_iterations)
    completed = int(progress * bar_length)
    remaining = bar_length - completed
    bar = "[" + "=" * completed + " " * remaining + "]"
    percent = "{0:.0f}%".format(progress * 100)
    print(f"Progress: {bar} {percent}", end='\r')

target_input = "y"
target_input1 = "user"
target_input2 = "ajcounts"
target_input3 = "password"
target_input4 = "pass"
target_input5 = "bypass"
admin_privileges = False

def display_instructions():
    print("If you are a non-admin, please enter the username: user and the password: pass")

def login():
    user_input = input("Enter your username: ")
    print("Processing username...")
    for i in range(3):
        time.sleep(0.3)
        loading_bar(3, i + 1)
    print("\n")

    user_input2 = input("Enter your password: ")
    print("Processing password...")
    for i in range(3):
        time.sleep(0.3)
        loading_bar(3, i + 1)
    print("\n")

    admin_privileges = False  # Initialize as False

    if user_input == target_input5:
        print(Fore.GREEN + "Bypass login successful!")
        print(Fore.GREEN + "Welcome", user_input)
        return True, True  # Return True for login and True for admin

    print("Checking credentials...")
    for i in range(5):
        time.sleep(0.5)
        loading_bar(5, i + 1)
    print("\n")

    if (user_input == target_input1 or user_input == target_input2) and (user_input2 == target_input3 or user_input2 == target_input4):
        print(Fore.GREEN + "You have successfully logged in!")
        print(Fore.GREEN + "Welcome", user_input)
        if user_input == target_input2 or user_input == target_input5:
            admin_privileges = True
        return True, admin_privileges
    else:
        print(Fore.RED + "Incorrect username or password or unknown username. Please try again.")
        return False, False # Return False for login and False for admin

# In your main loop where you call login():
while True:
    user_input_login = input("Would you like to login? Y/N ".format(target_input))
    if user_input_login == target_input:
        print(Fore.CYAN + f"You entered '{target_input}'! Proceeding...")
        display_instructions()
        login_successful, is_admin = login()
        if login_successful:
            print(Fore.GREEN + "Login successful!")
            if is_admin:
                print(Fore.YELLOW + "Admin privileges granted.")
                # Now you can use the 'is_admin' variable to control admin-only features
            break  # Exit the loop upon successful login
    else:
        print(Fore.RED + "Exiting")
        sys.exit()

my_list = ["help", "exit", "ping", "file*", "history", "pong", "clear", "color", "colors", "compress", "admin*", "admintest*", "exitadmintest*" ]

my_list2 = ["N/A"]

stored_commands = []  # List to store user commands
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_ip_address():
    while True:
        ip_address = input("Enter the IP address to ping (or \'exit\' to quit): ")
        stored_commands.append(f"ping {ip_address}") # Store the command
        if ip_address.lower() == 'exit':
            return None
        parts = ip_address.split('.')
        if len(parts) == 4:
            valid = True
            for part in parts:
                if not part.isdigit() or not 0 <= int(part) <= 255:
                    valid = False
                    break
            if valid:
                return ip_address
        print(Fore.YELLOW + "Invalid IP address format. Please enter a valid IPv4 address (e.g., 8.8.8.8).")

import ping3
def ping_ip(ip_address):
    try:
        delay = ping3.ping(ip_address)
        if delay is not None:
            print(Fore.GREEN + f"Ping to {ip_address} successful! Round-trip time: {delay * 1000:.2f} ms")
        else:
            print(Fore.RED + f"Failed to ping {ip_address}")
    except Exception as e:
        print(Fore.RED + f"An error occurred while pinging {ip_address}: {e}")

def execute_file(filename):
    stored_commands.append(f"file {filename}") # Store the command
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

def usercommands():
    admintest = False
    while True:
        user_input_command = input(Fore.WHITE + "What would you like to execute? ")
        stored_commands.append(user_input_command) # Store every command entered

        if user_input_command == "exit":
            print(Fore.RED + "Goodbye.")
            break
        elif user_input_command == "help":
            print("commands with * are admin only")
            print_list_in_columns(my_list, 3)
        elif user_input_command == "ping":
            ip_to_ping = get_valid_ip_address()
            if ip_to_ping:
                print(Fore.YELLOW + "Pinging IP address...")
                for i in range(3):
                    time.sleep(0.3)
                    loading_bar(3, i + 1)
                print("\n")
                ping_ip(ip_to_ping)
        elif user_input_command == "file":
            if admin == True:
                file_name = input(Fore.WHITE + "Enter the name of the Python file to execute: ")
                break
            if not file_name.endswith(".py"):
                print(Fore.RED + "Error: only .py files can be executed")
            elif not os.path.exists(file_name):
                print(Fore.RED + f"Error: File not found: {file_name}")
            else:
                print(Fore.YELLOW + f"Preparing to execute {file_name}...")
                for i in range(3):
                    time.sleep(0.3)
                    loading_bar(3, i + 1)
                print("\n")
                execute_file(file_name)
                if admin == False:
                    print(Fore.RED + "You are not an admin")

        elif user_input_command == "history":
            print(Fore.YELLOW + "\n--- Command History ---")
            for i, command in enumerate(stored_commands):
                print(Fore.LIGHTYELLOW_EX + f"{i+1}. {command}")
            print(Fore.YELLOW + "-----------------------\n")
        elif user_input_command == "clear":
            clear_terminal()
        elif user_input_command == "color":
            set_color()
        elif user_input_command == "compress":
            compress_file_command()
        elif user_input_command == "admin" and is_admin:
            admin = True
            print("You can now run commands that are admin only")
        elif user_input_command == "admintest" and is_admin:
            admin = False
            admin_test = True
            print("You are now in admin test mode")
        elif user_input_command == "exit_admintest" and admin_test == True:
            admin_test = False
            admin = True
            print("You are no longer in admin test mode")
        elif user_input_command == "admin" and not is_admin:
            print(Fore.RED + "You do not have admin privileges for this command.")

        else:
            print(Fore.RED + "Unrecognized command.")
    return None

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

if __name__ == "__main__":
    usercommands()

def compress_file_command():
    """Handles the 'compress' command."""
    print(Fore.WHITE + "Available compression formats: gzip (.gz), zip (.zip), tar (.tar), tar.gz (.tar.gz), tar.bz2 (.tar.bz2)")
    input_path = input(Fore.WHITE + "Enter the path to the file or directory to compress: ")
    output_path = input(Fore.WHITE + "Enter the desired output path (including extension): ")

    if not os.path.exists(input_path):
        print(Fore.RED + f"Error: Input path '{input_path}' not found.")
        return

    if output_path.lower().endswith(".gz"):
        compress_single_gzip(input_path, output_path)
    elif output_path.lower().endswith(".zip"):
        if os.path.isfile(input_path):
            create_zip_archive(output_path, [input_path])
        elif os.path.isdir(input_path):
            create_zip_archive(output_path, [], [input_path])
        else:
            print(Fore.RED + "Error: Cannot zip the specified input.")
    elif output_path.lower().endswith(".tar.gz"):
        create_tar_archive(output_path, [input_path] if os.path.isfile(input_path) else [], [input_path] if os.path.isdir(input_path) else [], compression='gz')
    elif output_path.lower().endswith(".tar.bz2"):
        create_tar_archive(output_path, [input_path] if os.path.isfile(input_path) else [], [input_path] if os.path.isdir(input_path) else [], compression='bz2')
    elif output_path.lower().endswith(".tar"):
        create_tar_archive(output_path, [input_path] if os.path.isfile(input_path) else [], [input_path] if os.path.isdir(input_path) else [], compression='')
    else:
        print(Fore.RED + "Error: Unsupported compression format in output path.")

def compress_single_gzip(input_path, output_path):
    """Compresses a single file using gzip."""
    try:
        with open(input_path, 'rb') as f_in, gzip.open(output_path, 'wb') as f_out:
            f_out.writelines(f_in)
        print(Fore.GREEN + f"Successfully compressed '{input_path}' to '{output_path}'")
    except FileNotFoundError:
        print(Fore.RED + f"Error: Input file '{input_path}' not found.")
    except Exception as e:
        print(Fore.RED + f"An error occurred during gzip compression: {e}")

def create_zip_archive(output_path, file_list, dir_list=None):
    """Creates a ZIP archive containing the specified files and directories."""
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_list:
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
                else:
                    print(Fore.YELLOW + f"Warning: File not found: '{file_path}'")
            if dir_list:
                for dir_path in dir_list:
                    if os.path.isdir(dir_path):
                        for root, _, files in os.walk(dir_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                relative_path = os.path.relpath(file_path, os.path.dirname(dir_path))
                                zipf.write(file_path, os.path.join(os.path.basename(dir_path), relative_path))
                    else:
                        print(Fore.YELLOW + f"Warning: Directory not found: '{dir_path}'")
        print(Fore.GREEN + f"Successfully created ZIP archive: '{output_path}'")
    except Exception as e:
        print(Fore.RED + f"An error occurred during ZIP creation: {e}")

def create_tar_archive(output_path, file_list, dir_list=None, compression=''):
    """Creates a TAR archive with optional compression (gz or bz2)."""
    try:
        with tarfile.open(output_path, 'w:' + compression) as tar:
            for file_path in file_list:
                if os.path.exists(file_path):
                    tar.add(file_path, arcname=os.path.basename(file_path))
                else:
                    print(Fore.YELLOW + f"Warning: File not found: '{file_path}'")
            if dir_list:
                for dir_path in dir_list:
                    if os.path.isdir(dir_path):
                        tar.add(dir_path, arcname=os.path.basename(dir_path))
                    else:
                        print(Fore.YELLOW + f"Warning: Directory not found: '{dir_path}'")
        print(Fore.GREEN + f"Successfully created TAR archive: '{output_path}' with compression '{compression}'")
    except Exception as e:
        print(Fore.RED + f"An error occurred during TAR creation: {e}")