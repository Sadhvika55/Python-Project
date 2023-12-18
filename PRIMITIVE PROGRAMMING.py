import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import Label
from tkinter import messagebox
import pygame

def space(expression):
    try:
        if ' ' in expression:
            raise ValueError("The expression should not contain any spaces.")
        else:
            return True
    except ValueError as err:
        print("Error:", err)
        return False

def unaryminus(expression):
    try:
        if '=-' in expression:
            raise ValueError("The expression should not contain a unary minus.")
        else:
            return True
    except ValueError as err:
        print("Error:", err)
        return False
def is_variable(expression):
    valid_variables = ['A', 'B', 'C', 'D', 'E']
    if expression in valid_variables:
        return True
    else:
        raise ValueError(f"Invalid variable name: {expression}")

def operator(op):
    if op == '+' or op == '-' or op == '*':
        return True
    else:
        return False

def valid_expression(expression):
    operator_count = len([char for char in expression if operator(char)])
    try:
        if operator_count > 1:
            raise ValueError("Invalid Expression")
        else:
            return True
    except ValueError as error:
        print("Error occurred:", error)
        return False

def interpreter(statements):
    memory = {}
    for statement in statements:
        if unaryminus(statement) and space(statement):
            var, expression = statement.split('=')
            if is_variable(var):
                if valid_expression(expression):
                    if expression.isdigit() and int(expression) < 100:
                        memory[var] = int(expression)                      #Ex:A=5
                    elif '+' in expression or '-' in expression or '*' in expression:       #Ex:B=A+C
                        operator = None
                        for op in ['+', '-', '*']:
                            if op in expression:
                                operator = op
                                break
                        if operator is None:                                    
                            print("Invalid expression:", expression)
                            return

                        operand1, operand2 = expression.split(operator)
                        try:
                            if operand1.isdigit() and int(operand1) < 100:
                                operand1 = int(operand1)
                            elif operand1 in memory:                            
                                operand1 = memory[operand1]
                            else:
                                raise ValueError("Invalid constituent")         #Ex: A=A*A
                        except ValueError as error:
                            print("Error occurred:", error)
                            return

                        try:
                            if operand2.isdigit() and int(operand2) < 100:
                                operand2 = int(operand2)
                            elif operand2 in memory:
                                operand2 = memory[operand2]
                            else:
                                raise ValueError("Invalid constituent")
                        except ValueError as error:
                            print("Error occurred:", error)
                            return

                        if operator == '+':                                     
                            result = operand1 + operand2
                        elif operator == '-':
                            result = operand1 - operand2
                        elif operator == '*':
                            result = operand1 * operand2
                        memory[var] = result
                    else:
                        print("Invalid expression:", expression)                      #If expression is neither digit nor it contains any operator . Ex: A=-K
                        return
                else:
                    print("Invalid expression:", expression)                           #Ex: A=B+C*D
                    return
            else:
                print("Invalid variable name. Variables can be A, B, C, D, or E:", var)     #Ex:K=A+B
                return
    new_dict = {key: value for key, value in (memory.items())}                          #memory.items will make key value pairs
    output_text = "\n".join([f"{key} = {value}" for key, value in new_dict.items()])
    return output_text

def start_button_clicked():
    notebook.select(1)  

def on_button_click(value):
    text_field.insert(tk.END, value) 
    play_sound(button_click_sound)

def on_run_click():
    statements = text_field.get("1.0", tk.END).splitlines()
    output_text = interpreter(statements)
    output_label.config(text=output_text)
    notebook.select(2) 
    play_sound(run_button_sound)

def on_stop_click():
    for button in alphabet_buttons_frame.winfo_children():
        button.configure(state=tk.DISABLED)
    for button in number_buttons_frame.winfo_children():
        button.configure(state=tk.DISABLED)
    for button in operator_buttons_frame.winfo_children():
        button.configure(state=tk.DISABLED)
    play_sound(stop_button_sound)

def on_enter_click():
    text_field.insert(tk.END, "\n") 
    play_sound(enter_button_sound)

# Initialize pygame for sound
pygame.mixer.init()

def play_button_click_sound():
    pygame.mixer.Sound("sound.wav").play()

background_music = pygame.mixer.Sound("tab1music.wav")

background_music.play(-1)

def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

def play_exit_button_sound():
    pygame.mixer.Sound("sound.wav").play()

def exit_button_clicked():
    play_exit_button_sound()
    result = messagebox.askquestion("Exit", "Are you sure you want to exit?")
    if result == 'yes':
        root.destroy()

# File paths
run_button_sound = "runbutton.mp3"
stop_button_sound = "stopbutton.wav"
enter_button_sound = "sound.wav"
button_click_sound = "sound.wav"

# Main Window
root = tk.Tk()
root.title("MINI INTERPRETER")
window_width = 800
window_height = 600

#Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# First tab
main_tab = ttk.Frame(notebook)
notebook.add(main_tab, text='FRONT PAGE')

background_image = PhotoImage(file="fbg.png")
background_label = tk.Label(main_tab, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

button_bg_color = "lightpink"

# Let's Start 
start_button = tk.Button(main_tab, text="Let's Start", command=start_button_clicked, bg=button_bg_color)
start_button.place(x=690, y=340, width=150, height=100)

#Alphabet, Number, and Operator Buttons
second_tab = ttk.Frame(notebook)
notebook.add(second_tab, text='INPUT PAGE')

background_image_second = tk.PhotoImage(file="secbg (2).png")
background_label_second = tk.Label(second_tab, image=background_image_second)
background_label_second.place(x=0, y=0, relwidth=1, relheight=1)
background_label_second.place(x=0,y=0,width=10, height=10)

alphabet_images = {}
image_paths = [ "A.png", "B.png", "C.png", "D.png", "E.png"]
number_paths = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png"]
operator_paths = ["plus.png", "minus.png", "multiply.png", "equal to.png"]
# Operator Dictionary 
operator_images_mapping = {
    "plus.png": "+",
    "minus.png": "-",
    "multiply.png": "*",
    "equal to.png": "="}
for idx, image_path in enumerate(image_paths):
    image = tk.PhotoImage(file=image_path)
    alphabet_images[chr(ord('A') + idx)] = image.subsample(image.width() // 50, image.height() // 50)

alphabet_buttons_frame = tk.Frame(second_tab)
alphabet_buttons_frame.place(x=600, y=400)

for idx, (alphabet, image) in enumerate(alphabet_images.items()):
    button = tk.Button(alphabet_buttons_frame, image=image, command=lambda a=alphabet: on_button_click(a))
    button.grid(row=0, column=idx, padx=10, pady=10)

# Image dictionary
number_images = {}
for idx, number_path in enumerate(number_paths):
    number_image = tk.PhotoImage(file=number_path)
    number_images[str(idx)] = number_image.subsample(number_image.width() // 50, number_image.height() // 50)

number_buttons_frame = tk.Frame(second_tab)
number_buttons_frame.place(x=400, y=500)

for idx, (number, image) in enumerate(number_images.items()):
    button = tk.Button(number_buttons_frame, image=image, command=lambda n=number: on_button_click(n))
    button.grid(row=0, column=idx, padx=10, pady=10)

operator_buttons_frame = tk.Frame(second_tab)
operator_buttons_frame.place(x=600, y=600)


operator_images = {}
for idx, operator_path in enumerate(operator_paths):
    operator_image = tk.PhotoImage(file=operator_path)
    operator_images[operator_images_mapping[operator_path]] = operator_image.subsample(operator_image.width() // 70,operator_image.height() // 70)
    button = tk.Button(operator_buttons_frame, image=operator_images[operator_images_mapping[operator_path]],
                       command=lambda op=operator_images_mapping[operator_path]: on_button_click(op))
    button.grid(row=0, column=idx, padx=10, pady=10)

#Enter Button
enter_button = tk.Button(operator_buttons_frame, text="ENTER", command=on_enter_click, font=("Arial", 12))
enter_button.grid(row=0, column=len(operator_images), padx=10, pady=10)

# Create a label and text field for text entry
label_text = "Enter your text:"
label = tk.Label(second_tab, text=label_text, font=("Palatino", 15))
label.place(x=250, y=250)

text_field = tk.Text(second_tab, font=("Tahoma", 20))
text_field.place(x=400, y=50, width=700, height=300)

# Create the "RUN" button
run_button = tk.Button(second_tab, text="RUN", command=on_run_click, font=("Arial", 12))
run_button.place(x=400, y=600)

# Create the "STOP" button
stop_button = tk.Button(second_tab, text="STOP", command=on_stop_click, font=("Arial", 12))
stop_button.place(x=500, y=600)

# Third tab - Output Page
output_tab = ttk.Frame(notebook)
notebook.add(output_tab, text='OUTPUT PAGE')


style = ttk.Style()
style.configure("OutputFrame.TFrame", background="black")

output_frame = ttk.Frame(output_tab, padding=20, borderwidth=2, relief='groove', style="OutputFrame.TFrame")
output_frame.pack(fill='both', expand=True)


background_image_output = tk.PhotoImage(file="bg2.png")

#Output label
output_label = Label(output_frame, image=background_image_output, compound="center", font=("Arial", 16, "bold"))
output_label.place(x=750, y=350, anchor="center")

# Function to update the output label
def update_output_label(output_text):
    output_label.config(text=output_text)

# Add the exit button
exit_button_x = 1300
exit_button_y = 700
exit_button_width = 100
exit_button_height = 40

exit_button = tk.Button(output_frame, text="Exit", command=exit_button_clicked, bg="green", font=("Arial", 12))
exit_button.place(x=exit_button_x, y=exit_button_y, width=exit_button_width, height=exit_button_height)

# Run the GUI loop
root.mainloop()