from tkinter import *
import tkinter as tk
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk

root = Tk()
root.title("Steph's BMI Calculator")
root.geometry("650x700+300+200")
root.resizable(False, False)
root.configure(bg="#f0f1f5")


def BMI():
    h = float(Height.get())
    w = float(Weight.get())

    m = h / 100  # Convert height to meters
    bmi = round(float(w / m**2), 1)
    label_1.config(text=bmi)

    if bmi <= 18.5:
        label_2.config(text="Underweight!")
        label_3.config(text="You have lower weight than normal body!")

    elif 18.5 < bmi <= 25:
        label_2.config(text="Normal!")
        label_3.config(text="You are healthy and have a normal body!")

    elif 25 < bmi <= 30:
        label_2.config(text="Overweight!")
        label_3.config(text="You have a higher weight than normal body! \nThis means you're slightly overweight")

    else:
        label_2.config(text="Obese!")
        label_3.config(text="You have a higher weight than normal body! \nIf you do not lose weight, you may be at risk")


image_icon = PhotoImage(file="images/banner.png")
root.iconphoto(False, image_icon)

top = PhotoImage(file="images/BMI.png")
top_image = Label(root, image=top, background="#f0f1f5")
top_image.place(x=-1, y=-1)

Label(root, width=90, height=18, bg="lightblue").pack(side=BOTTOM)

# Create boxes for height and weight
box = PhotoImage(file="images/box.png")
Label(root, image=box).place(x=40, y=100)  # Height Box
Label(root, image=box).place(x=360, y=100)  # Weight Box

# Labels for Height and Weight
Label(root, text="Height (cm)", bg="#1f6e68", fg="white", font="Arial 15").place(x=80, y=130)
Label(root, text="Weight (kg)", bg="#1f6e68", fg="white", font="Arial 15").place(x=400, y=130)

scale = PhotoImage(file="images/scalee.PNG")
Label(root, image=scale, bg="lightblue").place(x=10, y=400)

# Slider for Height
current_value = tk.DoubleVar()


def get_current_value():
    return "{:.2f}".format(current_value.get())


def slider_change(event):
    Height.set(get_current_value())

    size = int(float(get_current_value()))
    img = Image.open("images/woman.png")
    resized_image = img.resize((90, 10 + size))
    photo_2 = ImageTk.PhotoImage(resized_image)
    person_image.config(image=photo_2)
    person_image.place(x=120, y=670 - size)
    person_image.image = photo_2

style_color = ttk.Style()
style_color.configure("TScale", background="white")

slider = ttk.Scale(root, from_=100, to=230, orient="horizontal", style="TScale",
                    command=slider_change, variable=current_value)
slider.place(x=80, y=250)  # Adjusted starting point for height slider

# Slider for Weight
current_value_2 = tk.DoubleVar()


def get_current_value_2():
    return "{:.2f}".format(current_value_2.get())


def slider_change_2(event):
    Weight.set(get_current_value_2())


style_color_2 = ttk.Style()
style_color_2.configure("TScale", background="white")

slider_2 = ttk.Scale(root, from_=30, to=200, orient="horizontal", style="TScale",
                      command=slider_change_2, variable=current_value_2)
slider_2.place(x=390, y=250)  # Adjusted starting point for weight slider

Height = StringVar()
Weight = StringVar()

# Entry fields for Height and Weight
height = Entry(root, textvariable=Height, width=6, font="arial 38", bg="#fff", fg="#000", bd=0)
height.place(x=60, y=175)
Height.set(get_current_value())

weight = Entry(root, textvariable=Weight, width=6, font="arial 38", bg="#fff", fg="#000", bd=0)
weight.place(x=380, y=175)
Weight.set(get_current_value_2())

person_image = Label(root, bg="lightblue")
person_image.place(x=70, y=550)

Button(root, text="View Report", width=18, height=3, font="arial 10 bold", bg="#1f6e68", fg="white", command=BMI).place(x=380, y=340)

# Label for BMI result
label_1 = Label(root, font="arial 35 bold", bg="#1f6e68", fg="white")
label_1.place(x=220, y=340)

# Labels for BMI category and message
label_2 = Label(root, font="arial 20 bold", bg="lightblue", fg="#3b3a3a")
label_2.place(x=300, y=430)

label_3 = Label(root, font="arial 10 bold", bg="lightblue")
label_3.place(x=250, y=500)

root.mainloop()