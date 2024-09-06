from tkinter import filedialog,messagebox
import tkinter as tk
from PIL import Image,ImageTk
import ttkbootstrap as ttk
import requests
from ttkbootstrap.constants import *

label_image=None
have_image=None
def request_image():
    global label_image,have_image
    if not entry.get():
        messagebox.showerror(message="Place The TextBox SomeThing")
        return
    if have_image:
        messagebox.showinfo(message="There is Image in the Box")
    image_name=entry.get()

    request_action=requests.get(f"http://127.0.0.1:8080/getimage?imagename={image_name}")
    if request_action.status_code==200:
       try:
           with open("example.jpg", "wb") as file:
               file.write(request_action.content)

           img = Image.open("example.jpg")
           img=img.resize((300,300))
           img = ImageTk.PhotoImage(img)

           # the resize method retruns new object and does not modify original image if you use it like this img.resize

           label.config(image=img)
           label_image=img
           have_image=True
       except Exception as E:
           print(E)

    else:
        messagebox.showerror(title="Error We Have Nothing",message=request_action.json())
def upload_image():
    file=filedialog.askopenfilename(filetypes=[("Image Files","*")])

    with open(file ,'rb') as buffer:


        path=requests.post(f"http://127.0.0.1:8080/upload-image",files=({"file":buffer}))

        GetAllImages()

    print(path.status_code)


def GetAllImages():
    images_request=requests.get("http://127.0.0.1:8080/allimages")
    Images=images_request.json()
    print(Images)
    if "images" in Images:
        print(Images)
        Images = list(Images["images"])

        entry["values"]=Images
        entry.current(0)

    else:
        entry["values"]=[]

def delimage():
    global label_image
    name_of_image=entry.get()
    if name_of_image:
        try:
            DeleteOrNO=messagebox.askyesno(message=f"Are You Sure To Delete  {name_of_image}  Image")
            if DeleteOrNO:
                r = requests.delete(f"http://127.0.0.1:8080/delete?name={name_of_image}")
                GetAllImages()

            return
        except Exception as E:
            print(E)

        if r.status_code == 200:
            messagebox.showinfo(message=r.json())
            GetAllImages()
        else:
            messagebox.showerror(message=r.json())
    else:
        messagebox.showerror(message="Enter some thing")


chat = tk.Tk()
chat.geometry("500x400")

entry = ttk.Combobox(chat)


# Create buttons with the correct style
button = ttk.Button(chat, text="Request Image", command=request_image, cursor="hand2", bootstyle=(INFO, OUTLINE))
button3 = ttk.Button(chat, text="Delete Image", command=delimage, cursor="hand2", bootstyle=(DANGER, OUTLINE))
button2 = ttk.Button(chat, text="Upload Image", command=upload_image, cursor="hand2", bootstyle=(SUCCESS, OUTLINE))


# Create a label for the image placeholder
label = ttk.Label(chat, text="image will be placed here", anchor="center")

# Place the entry widget
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Place the buttons on the same line
button.grid(row=1, column=1, padx=5, pady=10)
button2.grid(row=1, column=2, padx=5, pady=10)
button3.grid(row=1, column=3, padx=5, pady=10)

# Place the label below the buttons
label.grid(row=2, column=0, columnspan=4, padx=5, pady=10, sticky="we")

# Configure the columns to expand with the window
for col in range(4):
    chat.columnconfigure(col, weight=10)
    #Yes, exactly. Setting weight=1 for each column ensures that the
    # available space is evenly distributed among all the columns.

GetAllImages()

#Setting the weight of columns ensures that each column gets a proportional amount of space.
# By configuring each column with the same weight, you are explicitly telling Tkinter to distribute
# space evenly across these columns.
# This not only affects resizing but also ensures that the initial layout is as intended.
# Run the main event loop
chat.mainloop()