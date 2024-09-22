import requests
import json
from dotenv import load_dotenv, set_key
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Label
from PIL import Image, ImageTk  # Import from Pillow for handling images
from get_token import get_token
from elevate_token import elevate_token
from create_form import create_form
import sys


def on_get_token_button_click(status_label_get):
    # Function now takes the status_label as an argument
    try:
        get_token()
        status_label_get.config(text="Token obtained successfully!", bootstyle="success")
        messagebox.showinfo("Success", "Token obtained successfully!")  # Show pop-up message - optional
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label_get.config(text="Error occurred", bootstyle="danger")

def on_elevate_token_button_click(status_label_elevate):
    try:
        elevate_token()  # Call the elevate_token function
        status_label_elevate.config(text="Token elevated successfully!", bootstyle="success")
        messagebox.showinfo("Success", "Token elevated successfully!")  # Show pop-up message - optional
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label_elevate.config(text="Error occurred", bootstyle="danger")

def on_create_form_button_click(spinbox_value, extension_combobox, status_label_create_form, issue_definition_entry, project_id_entry):
    try:
        num_forms = int(spinbox_value.get())  # Get the number from the spinbox
        selected_option = extension_combobox.get()  # Get the selected option from the dropdown
        project_id = project_id_entry.get()
        issue_definition_id = issue_definition_entry.get()
        
        if not selected_option:
            raise ValueError("No extension data option selected.")
        
        if not issue_definition_id:
            raise ValueError("Issue Definition ID cannot be empty. Obtain from Fulcrum via inspecting network.")
        
        if not project_id:
            raise ValueError("Project ID cannot be empty. Obtain from Fulcrum via inspecting network.")
        
        # Retrieve the extension data for the selected option
        extension_data_options = load_extension_data_options()
        extension_data = extension_data_options.get(selected_option)
        
        if not extension_data:
            raise ValueError("Invalid extension data option selected.")
        
        # Parse the JSON string into a dictionary
        extension_data = json.loads(extension_data)
        
        # Call the create_form function as many times as needed
        for _ in range(num_forms):
            create_form(extension_data, issue_definition_id, project_id)  # Pass the extension data to create_form
        
        status_label_create_form.config(text=f"{num_forms} forms created successfully!", bootstyle="success")
        messagebox.showinfo("Success", f"{num_forms} forms created successfully!")  # Show success pop-up
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label_create_form.config(text="Error occurred while creating forms", bootstyle="danger")

def load_extension_data_options():
    load_dotenv()  # Load the .env file
    options = {
        "Contract Cashflow": os.getenv("EXTENSION_DATA_CONTRACT_CASHFLOW"), #completed
        "Project Progress": os.getenv("EXTENSION_DATA_PROJECT_PROGRESS"), #completed
        "HOTO": os.getenv("EXTENSION_DATA_HOTO"), #completed
        "RSS Inspection": os.getenv("EXTENSION_DATA_RSS_INSPECTION"), #completed
    }
    return options

def create_ui():
    # Create the ttkbootstrap window
    root = ttk.Window(themename="darkly")
    root.title("DBE O2 Assistant Bot")

    # Define the ASCII header
    ascii_header = """                                                                                                          

 ██████╗ ██████╗     ██████╗  ██████╗ ████████╗
██╔═══██╗╚════██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
██║   ██║ █████╔╝    ██████╔╝██║   ██║   ██║   
██║   ██║██╔═══╝     ██╔══██╗██║   ██║   ██║   
╚██████╔╝███████╗    ██████╔╝╚██████╔╝   ██║   
 ╚═════╝ ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
                                                                                                                                                                                                                                                                                                    
"""

    ascii_actions = """

 █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
███████║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
                                                       
"""

    # Create and place the ASCII header label
    header_label = ttk.Label(root, text=ascii_header, font=("Courier", 8), bootstyle="info", anchor="w", justify="left")
    header_label.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Create and place "Get Token" button
    get_token_button = ttk.Button(root, text="Get Token", bootstyle=SUCCESS, command=lambda: on_get_token_button_click(status_label_get), width=20)
    get_token_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Create and place "Elevate Token" button
    elevate_token_button = ttk.Button(root, text="Elevate Token", bootstyle=SUCCESS, command=lambda: on_elevate_token_button_click(status_label_elevate), width=20)
    elevate_token_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Add title for actions. Create and place the ASCII header label, ANSI Shadow
    header_label = ttk.Label(root, text=ascii_actions, font=("Courier", 4), bootstyle="info", anchor="w", justify="left")
    header_label.grid(row=3, column=0, columnspan=4, pady=10, sticky="ew")
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Add a Combobox for extension data selection
    extension_label = ttk.Label(root, text="Select Form Type:", bootstyle="info")
    extension_label.grid(row=4, column=0, padx=10, pady=4, sticky="ew")
    extension_combobox = ttk.Combobox(root, values=list(load_extension_data_options().keys()), width=20)
    extension_combobox.grid(row=5, column=0, padx=10, pady=4, sticky="ew")

    # Add Spinbox to select the number of forms
    spinbox_label = ttk.Label(root, text="No. of forms to create:", bootstyle="info")
    spinbox_label.grid(row=4, column=1, padx=10, pady=4, sticky="ew")
    spinbox_value = ttk.Spinbox(root, from_=1, to=100, width=10)  # You can set the range for the number of forms
    spinbox_value.grid(row=5, column=1, padx=10, pady=4, sticky="ew")

    # Add a new label and entry box for Issue Definition ID
    issue_definition_label = ttk.Label(root, text="Issue Definition ID", bootstyle="info")
    issue_definition_label.grid(row=6, column=0, padx=10, pady=4, sticky="ew")
    issue_definition_entry = ttk.Entry()
    issue_definition_entry.grid(row=7, column=0, padx=10, pady=4, sticky="ew")

    # Add Entry to select Project ID
    project_id_label = ttk.Label(root, text="Project ID", bootstyle="info")
    project_id_label.grid(row=6, column=1, padx=10, pady=4, sticky="ew")
    project_id_entry = ttk.Entry()
    project_id_entry.grid(row=7, column=1, padx=10, pady=4, sticky="ew")
    
    # Add "Create Form" button
    create_form_button = ttk.Button(root, text="Create Form", bootstyle=SUCCESS, command=lambda: on_create_form_button_click(spinbox_value, extension_combobox, status_label_create_form, issue_definition_entry, project_id_entry), width=20)
    #create_form_button = ttk.Button(root, text="Create Form", bootstyle=SUCCESS, command=lambda: on_create_form_button_click(spinbox_value, extension_combobox, issue_definition_entry, project_id_entry, status_label_create_form), width=20)
    create_form_button.grid(row=5, column=2, columnspan=3, padx=10, pady=10, sticky="ew")

    # Create status labels
    status_label_get = ttk.Label(root, text="Status: Getting Token...", bootstyle="info")
    status_label_get.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    status_label_elevate = ttk.Label(root, text="Status: Elevating Token...", bootstyle="info")
    status_label_elevate.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    status_label_create_form = ttk.Label(root, text="Status: Creating Form...", bootstyle="info")
    status_label_create_form.grid(row=6, column=2, padx=10, pady=5, sticky="ew")

    # pyinstaller expects to find your assets in a temp folder called sys._MEIPASS/2
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Load and display the cat image
    image_path = resource_path("photos\\cat.jpg")  # Path to your cat image
    image = Image.open(image_path)
    image = image.resize((300, 300), Image.LANCZOS)  # Use Image.LANCZOS for high-quality resizing

    # Convert the image to a format compatible with Tkinter
    tk_image = ImageTk.PhotoImage(image)

    # Store a reference to the image to prevent garbage collection
    root.tk_image = tk_image

    # Create and place the image label
    image_label = Label(root, image=tk_image)
    image_label.grid(row=8, column=2, columnspan=2, pady=10)

    # Set window size
    root.geometry("800x800")

    return root


