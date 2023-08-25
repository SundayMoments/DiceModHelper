import subprocess
import os
from lxml import etree
import tkinter as tk
import pyperclip
import uuid
from tkinter import (
    ttk,
    messagebox,
    filedialog,
    )

from LocaConversion import (
    save,
    load,
    LocaFormat
)

VERSION = 'v1.3'

def create_directories(output_directory, folder_name):
    directories = [
        f'{output_directory}/Localization/English',
        f'{output_directory}/Mods/{folder_name}',
        f'{output_directory}/Public/Game/GUI/Assets/DiceSets/{folder_name}',
        f'{output_directory}/Public/{folder_name}/CustomDice',
        f'{output_directory}/Public/{folder_name}/Game/GUI'
    ]
    for directory in directories:
        try:
            os.makedirs(directory)
            write_to_terminal(f"Directory created: {directory}")
        except Exception as e:
            write_to_terminal(f"Error creating directory {directory}: {str(e)}")

def write_file(file_path, content):
    try:
        with open(file_path, 'wb') as file:
            file.write(content)
        write_to_terminal(f"File written: {file_path}")
    except Exception as e:
        write_to_terminal(f"Error writing file {file_path}: {str(e)}")

def write_to_terminal(message):
    output_terminal.insert(tk.END, message + "\n")
    output_terminal.see(tk.END)  # Scroll to the last line

def generate_folder_name_xml_content(HandName, ModNameGame, HandDesc, ModDescGame):
    content_list = etree.Element("contentList", date="28/12/2022 10:15")
    etree.SubElement(content_list, "content", contentuid=HandName, version="1").text = ModNameGame
    etree.SubElement(content_list, "content", contentuid=HandDesc, version="1").text = ModDescGame
    return etree.tostring(content_list, encoding="utf-8", pretty_print=True)

def generate_custom_dice_lsx_content(FolderName, HandName, HandDesc, ModUUID):
    save = etree.Element("save")
    etree.SubElement(save, "version", major="4", minor="0", revision="9", build="307")
    region = etree.SubElement(save, "region", id="CustomDice")
    node_root = etree.SubElement(region, "node", id="root")
    children = etree.SubElement(node_root, "children")
    node_custom_dice = etree.SubElement(children, "node", id="CustomDice")
    attributes = [
        ("Description", "TranslatedString", HandDesc, "handle", "1"),
        ("DisplayName", "TranslatedString", HandName, "handle", "1"),
        ("Flip1", "bool", "false"),
        ("Flip20", "bool", "false"),
        ("Icon1", "bool", "true"),
        ("Icon20", "bool", "true"),
        ("Name", "LSString", FolderName),
        ("UUID", "guid", ModUUID),
    ]
    for attr in attributes:
        if "handle" in attr:
            attribute_name = attr[3]
            version = attr[4] if len(attr) > 4 else None
            etree.SubElement(node_custom_dice, "attribute", id=attr[0], type=attr[1], **{attribute_name: attr[2]}, version=version)
        else:
            etree.SubElement(node_custom_dice, "attribute", id=attr[0], type=attr[1], value=attr[2])

    return etree.tostring(save, encoding="utf-8", pretty_print=True, xml_declaration=True)

def generate_meta_lsx_content(AuthorName, ModName, ModDesc, FolderName, ModUUID):
    save = etree.Element("save")
    etree.SubElement(save, "version", major="4", minor="0", revision="9", build="303")
    region = etree.SubElement(save, "region", id="Config")
    node_root = etree.SubElement(region, "node", id="root")
    children_root = etree.SubElement(node_root, "children")
    etree.SubElement(children_root, "node", id="Dependencies")
    node_module_info = etree.SubElement(children_root, "node", id="ModuleInfo")
    attributes = [
        ("Author", "LSString", AuthorName),
        ("CharacterCreationLevelName", "FixedString", ""),
        ("Description", "LSString", ModDesc),
        ("Folder", "LSString", FolderName),
        ("LobbyLevelName", "FixedString", ""),
        ("MD5", "LSString", ""),
        ("MainMenuBackgroundVideo", "FixedString", ""),
        ("MenuLevelName", "FixedString", ""),
        ("Name", "LSString", ModName),
        ("NumPlayers", "uint8", "4"),
        ("PhotoBooth", "FixedString", ""),
        ("StartupLevelName", "FixedString", ""),
        ("Tags", "LSString", ""),
        ("Type", "FixedString", "Add-on"),
        ("UUID", "FixedString", ModUUID),
        ("Version64", "int64", "36028797018963968"),
    ]
    for attr in attributes:
        etree.SubElement(node_module_info, "attribute", id=attr[0], type=attr[1], value=attr[2])
    children_module_info = etree.SubElement(node_module_info, "children")
    node_publish_version = etree.SubElement(children_module_info, "node", id="PublishVersion")
    etree.SubElement(node_publish_version, "attribute", id="Version64", type="int64", value="144255927713898169")
    etree.SubElement(children_module_info, "node", id="Scripts")
    node_target_modes = etree.SubElement(children_module_info, "node", id="TargetModes")
    children_target_modes = etree.SubElement(node_target_modes, "children")
    node_target = etree.SubElement(children_target_modes, "node", id="Target")
    etree.SubElement(node_target, "attribute", id="Object", type="FixedString", value="Story")
    return etree.tostring(save, encoding="utf-8", pretty_print=True, xml_declaration=True)

def generate_metadata_lsx_content(FolderName):
    save = etree.Element("save")
    etree.SubElement(save, "version", major="4", minor="0", revision="9", build="319")
    region = etree.SubElement(save, "region", id="config")
    node_config = etree.SubElement(region, "node", id="config")
    children_config = etree.SubElement(node_config, "children")
    node_entries = etree.SubElement(children_config, "node", id="entries")
    children_entries = etree.SubElement(node_entries, "children")

    # Define the map keys
    map_keys = [
        "d20", "d20_1", "d20_10", "d20_11", "d20_12", "d20_13",
        "d20_14", "d20_15", "d20_16", "d20_17", "d20_18", "d20_19",
        "d20_2", "d20_20", "d20_3", "d20_4", "d20_5", "d20_6",
        "d20_7", "d20_8", "d20_9", "d20_faceCover",
        "double_roll_1", "double_roll_2", "single_roll"
    ]
    
    # Loop through the map keys to create repetitive nodes
    for key in map_keys:
        node_object = etree.SubElement(children_entries, "node", id="Object")
        etree.SubElement(node_object, "attribute", id="MapKey", type="FixedString", value=f"Assets/DiceSets/{FolderName}/{key}.png")
        children_object = etree.SubElement(node_object, "children")
        node_entries_inner = etree.SubElement(children_object, "node", id="entries")
        attributes = [("h", "int16", "1024"), ("mipcount", "int8", "1"), ("w", "int16", "1280")]
        if key.endswith("faceCover"):
            attributes[0] = ("h", "int16", "256")
            attributes[2] = ("w", "int16", "256")
        elif key.startswith("double_roll") or key == "single_roll":
            attributes[0] = ("h", "int16", "1280")
            attributes[2] = ("w", "int16", "1536")
        for attr in attributes:
            etree.SubElement(node_entries_inner, "attribute", id=attr[0], type=attr[1], value=attr[2])
    return etree.tostring(save, encoding="utf-8", pretty_print=True, xml_declaration=True)

def generate_files():
    # Retrieve the values from the form
    folder_name = folder_name_var.get()
    hand_name = hand_name_var.get()
    hand_desc = hand_desc_var.get()
    mod_name_game = mod_name_game_var.get()
    mod_desc_game = mod_desc_game_var.get()
    mod_uuid = mod_uuid_var.get()
    author_name = author_name_var.get()
    mod_name = mod_name_var.get()
    mod_desc = mod_desc_var.get()
    output_directory = output_dir_var.get()

    # Create the folder structure
    create_directories(output_directory, folder_name)

    # Generate the content for each file
    folder_name_xml_content = generate_folder_name_xml_content(hand_name, mod_name_game, hand_desc, mod_desc_game)
    custom_dice_lsx_content = generate_custom_dice_lsx_content(folder_name, hand_name, hand_desc, mod_uuid)
    meta_lsx_content = generate_meta_lsx_content(author_name, mod_name, mod_desc, folder_name, mod_uuid)
    metadata_lsx_content = generate_metadata_lsx_content(folder_name)

    # Create and write the content for each file
    write_file(f'{output_directory}/Localization/English/{folder_name}.xml', folder_name_xml_content)
    write_file(f'{output_directory}/Public/{folder_name}/CustomDice/CustomDice.lsx', custom_dice_lsx_content)
    write_file(f'{output_directory}/Mods/{folder_name}/meta.lsx', meta_lsx_content)
    write_file(f'{output_directory}/Public/{folder_name}/Game/GUI/metadata.lsx', metadata_lsx_content)

    # Convert the newly created XML file to .loca format
    convert_xml_to_loca()

    # Assuming that messagebox is part of a GUI library like tkinter
    messagebox.showinfo("Success", "Files generated successfully!")

def select_output_dir():
    folder_selected = filedialog.askdirectory()
    output_dir_var.set(folder_selected)

def open_dice_sets_folder():
    folder_path = output_dir_var.get()
    subprocess.Popen(f'explorer {os.path.realpath(folder_path)}')

def open_localization_folder():
    folder_path = os.path.join(output_dir_var.get(), 'Localization', 'English')
    subprocess.Popen(f'explorer {os.path.realpath(folder_path)}')

def open_dds_folder():
    folder_path = os.path.join(output_dir_var.get(), 'Public', 'Game', 'GUI', 'Assets', 'DiceSets', folder_name_var.get())
    subprocess.Popen(f'explorer {os.path.realpath(folder_path)}')

def copy_localization_path():
    file_path = os.path.join(output_dir_var.get(), 'Localization', 'English', f'{folder_name_var.get()}.xml')
    pyperclip.copy(file_path)  # Copy to clipboard
    messagebox.showinfo("Success", "Path copied to clipboard!")

def generate_guid():
    return str(uuid.uuid4())

def generate_handle():
    guid = uuid.uuid4()
    return f"h{guid}".replace('-', 'g')

def update_handle1():
    hand_name_var.set(generate_handle())

def update_handle2():
    hand_desc_var.set(generate_handle())

def update_mod_uuid():
    mod_uuid_var.set(generate_guid())

def convert_xml_to_loca(show_message=False):
    try:
        file_path = os.path.join(output_dir_var.get(), 'Localization', 'English', f'{folder_name_var.get()}.xml')
        xml_path = file_path
        loca_path = file_path.replace('.xml', '.loca')

        # Read the XML file
        resource = load(xml_path, LocaFormat.XML)

        # Write the .loca file
        save(resource, loca_path, LocaFormat.LOCA)

        # Log the success message in the output terminal
        write_to_terminal(f"File converted: {xml_path} to {loca_path}")

        if show_message:
            messagebox.showinfo("Success", "Converted XML to .loca successfully!")
    except Exception as e:
        # Display the error message in the output terminal
        write_to_terminal(f"An error occurred: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title(f"Dice Mod Helper - Made by SeanConnerX0 - {VERSION}")

# Retrieve the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the window width and height as a percentage of the screen size
window_width = int(screen_width * 0.5)  # Increased width for better view
window_height = int(window_width * 9 / 16)  # 16:9 aspect ratio

# Set the window size
root.geometry(f"{window_width}x{window_height}")

# Variables for the form
folder_name_var = tk.StringVar()
hand_name_var = tk.StringVar()
hand_desc_var = tk.StringVar()
mod_name_game_var = tk.StringVar()
mod_desc_game_var = tk.StringVar()
mod_uuid_var = tk.StringVar()
author_name_var = tk.StringVar()
mod_name_var = tk.StringVar()
mod_desc_var = tk.StringVar()
output_dir_var = tk.StringVar()

# Add some padding to the root window
root.configure(padx=10, pady=10)

def create_section(title, row):
    ttk.Label(root, text=title, font=("Helvetica", 10)).grid(row=row, column=0, columnspan=3, pady=5)
    return row + 1

# Variables for the form
vars = [folder_name_var, hand_name_var, hand_desc_var, mod_name_game_var, mod_desc_game_var, mod_uuid_var, author_name_var, mod_name_var, mod_desc_var]

# Define the form labels and entry fields
row = create_section("Handles and Folder Name(s)", 0)
labels = ["Folder Name:", "Handle - [1]:", "Handle - [2]:"]
for idx, label in enumerate(labels):
    ttk.Label(root, text=label).grid(row=row, column=0, sticky='w', padx=5)
    ttk.Entry(root, textvariable=vars[idx]).grid(row=row, column=1, sticky='ew', padx=5)
    if "Handle - [1]:" in label:
        ttk.Button(root, text="Generate", command=update_handle1).grid(row=row, column=2, padx=5)
    elif "Handle - [2]:" in label:
        ttk.Button(root, text="Generate", command=update_handle2).grid(row=row, column=2, padx=5)
    row += 1

# Add button to generate mod UUID
row = create_section("In-Game Information", row)
labels = ["Name:", "Description:", "Mod UUID:"]
for idx, label in enumerate(labels):
    ttk.Label(root, text=label).grid(row=row, column=0, sticky='w', padx=5)
    ttk.Entry(root, textvariable=vars[idx + 3]).grid(row=row, column=1, sticky='ew', padx=5)
    if "Mod UUID" in label:
        ttk.Button(root, text="Generate", command=update_mod_uuid).grid(row=row, column=2, padx=5)
    row += 1

row = create_section("Meta Information", row)
labels = ["Author:", "Mod Name:", "Mod Description:"]
for idx, label in enumerate(labels):
    ttk.Label(root, text=label).grid(row=row, column=0, sticky='w', padx=5)
    ttk.Entry(root, textvariable=vars[idx + 6]).grid(row=row, column=1, sticky='ew', padx=5)
    row += 1

row = create_section("Output", row)
ttk.Label(root, text="Output Directory:").grid(row=row, column=0, sticky='w', padx=5)
ttk.Entry(root, textvariable=output_dir_var).grid(row=row, column=1, sticky='ew', padx=5)
ttk.Button(root, text="Browse", command=select_output_dir).grid(row=row, column=2, padx=5)
row += 1

# Generate button
generate_button = ttk.Button(root, text="Build", command=generate_files)
generate_button.grid(row=row, column=1, pady=10)  # Centered the Generate button

# Button row under "Generate" button
row += 1
ttk.Button(root, text="Open Output Directory", command=open_dice_sets_folder).grid(row=row, column=0, padx=5)
ttk.Button(root, text="Open Localization Directory", command=open_localization_folder).grid(row=row, column=1, padx=5)
# Modify the command to pass True for the show_message parameter
ttk.Button(root, text="Convert XML to .loca", command=lambda: convert_xml_to_loca(True)).grid(row=row, column=2, padx=5)

row += 1
ttk.Button(root, text="Open .DDS Directory", command=open_dds_folder).grid(row=row, column=1, padx=5)

# Make the second column stretchable
root.grid_columnconfigure(1, weight=1)

# Create a frame to hold the Text widget
output_frame = ttk.Frame(root)
output_frame.grid(row=row+1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

# Configure the row for the output_frame to expand
root.grid_rowconfigure(row+1, weight=1)

# Create a Text widget to serve as the output terminal inside the frame
output_terminal = tk.Text(output_frame, wrap='word', height=9, bg="black", fg="lime")  # Terminal-like appearance
output_terminal.pack(expand=True, fill='both')

# Run the main loop
root.mainloop()