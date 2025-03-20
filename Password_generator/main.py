from tkinter import *
import random
from string import ascii_letters, digits, punctuation

root = Tk()
root.title("Stephnora's Password Generator")
root.geometry("800x600")

# Character sets
LOWERCASE = ascii_letters[:26]
UPPERCASE = ascii_letters[26:]
NUMBERS = digits
SYMBOLS = punctuation


def generate_password():
    # Get password length
    try:
        password_length = int(entry_length.get())
    except ValueError:
        entry_password.delete(0, END)
        entry_password.insert(0, "Invalid length")
        return

    # Prepare character sets based on user selection
    characters = ""
    if var_lowercase.get():
        characters += LOWERCASE
    if var_uppercase.get():
        characters += UPPERCASE
    if var_numbers.get():
        characters += NUMBERS
    if var_symbols.get():
        characters += SYMBOLS

    # Validate if at least one character type is selected
    if not characters:
        entry_password.delete(0, END)
        entry_password.insert(0, "Select character types")
        return

    # Ensure the password meets security rules
    strong_password = []
    if var_lowercase.get():
        strong_password.append(random.choice(LOWERCASE))
    if var_uppercase.get():
        strong_password.append(random.choice(UPPERCASE))
    if var_numbers.get():
        strong_password.append(random.choice(NUMBERS))
    if var_symbols.get():
        strong_password.append(random.choice(SYMBOLS))

    # Fill the rest of the password length
    if password_length > len(strong_password):
        strong_password += random.choices(characters, k=password_length - len(strong_password))

    random.shuffle(strong_password)
    generated_password = "".join(strong_password)
    entry_password.delete(0, END)
    entry_password.insert(0, generated_password)


def copy_clipboard():
    root.clipboard_clear()
    root.clipboard_append(entry_password.get())


# Frame for password length
frame_length = LabelFrame(root, text="Password Length (8-128):")
frame_length.pack(pady=20)

entry_length = Entry(frame_length, font=("Helvetica", 24))
entry_length.pack(pady=20, padx=20)

# Frame for character options
frame_options = LabelFrame(root, text="Character Options:")
frame_options.pack(pady=20)

var_lowercase = BooleanVar(value=True)
var_uppercase = BooleanVar(value=True)
var_numbers = BooleanVar(value=True)
var_symbols = BooleanVar(value=True)

Checkbutton(frame_options, text="Include Lowercase", variable=var_lowercase).pack(side=LEFT, padx=10)
Checkbutton(frame_options, text="Include Uppercase", variable=var_uppercase).pack(side=LEFT, padx=10)
Checkbutton(frame_options, text="Include Numbers", variable=var_numbers).pack(side=LEFT, padx=10)
Checkbutton(frame_options, text="Include Symbols", variable=var_symbols).pack(side=LEFT, padx=10)

# Entry for excluding specific characters
entry_exclude = Entry(root, font=("Helvetica", 16), width=30)
entry_exclude.pack(pady=10)
entry_exclude.insert(0, "Exclude characters (optional)")

# Entry for generated password
entry_password = Entry(root, text="", font=("Helvetica", 24), bd=0, bg="systembuttonface")
entry_password.pack(pady=20, padx=20)

my_frame = Frame(root)
my_frame.pack(pady=20)

# Buttons
btn_generate = Button(my_frame, text="Generate Password", command=generate_password)
btn_generate.grid(row=0, column=0, padx=10)

btn_copy = Button(my_frame, text="Copy to Clipboard", command=copy_clipboard)
btn_copy.grid(row=0, column=1, padx=10)

root.mainloop()
