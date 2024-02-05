# Autor kodu tworzącego ciemny motyw okna w tkinterze - Terranova Tech
# https://github.com/Terranova-Python/Tkinter-Menu-Bar/blob/main/main.py

from tkinter import *
from ctypes import windll

tk_title = "Projekt" # Put here your window title

root=Tk() # root (your app doesn't go in root, it goes in window)
root.title(tk_title) 
root.overrideredirect(True) # turns off title bar, geometry

screen_width = root.winfo_screenwidth(); screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (850 / 2)
y = (screen_height / 2) - (400 / 2)

root.geometry(f"{850}x{400}+{int(x)}+{int(y) - 100}") # set new geometry the + 75 + 75 is where it starts on the screen
#root.iconbitmap("your_icon.ico") # to show your own icon 
root.minimized = False # only to know if root is minimized
root.maximized = False # only to know if root is maximized

LGRAY = '#3e4042' # button color effects in the title bar (Hex color)
DGRAY = '#25292e' # window background color               (Hex color)
RGRAY = '#10121f' # title bar color                       (Hex color)

root.config(bg="#25292e")
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)

def set_appwindow(mainWindow): # to display the window icon on the taskbar, 
                               # even when using root.overrideredirect(True
    # Some WindowsOS styles, required for task bar integration
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())
    

def minimize_me():
    root.attributes("-alpha",0) # so you can't see the window when is minimized
    root.minimized = True


def deminimize(event):

    # root.focus() 
    root.attributes("-alpha",1) # so you can see the window when is not minimized
    if root.minimized == True:
        root.minimized = False                              
        

def maximize_me():

    if root.maximized == False: # if the window was not maximized
        root.normal_size = root.geometry()
        expand_button.config(text=" 🗗 ")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.maximized = not root.maximized 
        # now it's maximized
        
    else: # if the window was maximized
        expand_button.config(text=" 🗖 ")
        root.geometry(root.normal_size)
        root.maximized = not root.maximized
        # now it is not maximized

# put a close button on the title bar
close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)

# a frame for the main area of the window, this is where the actual app will go
window = Frame(root, bg=DGRAY,highlightthickness=0)

# pack the widgets
title_bar.pack(fill=X)
close_button.pack(side=RIGHT,ipadx=7,ipady=1)
expand_button.pack(side=RIGHT,ipadx=7,ipady=1)
minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
title_bar_title.pack(side=LEFT, padx=10)
window.pack(expand=1, fill=BOTH) # replace this with your main Canvas/Frame/etc.
#xwin=None
#ywin=None
# bind title bar motion to the move window function

def changex_on_hovering(event):
    global close_button
    close_button['bg']='red'
    
    
def returnx_to_normalstate(event):
    global close_button
    close_button['bg']=RGRAY
    

def change_size_on_hovering(event):
    global expand_button
    expand_button['bg']=LGRAY
    
    
def return_size_on_hovering(event):
    global expand_button
    expand_button['bg']=RGRAY
    

def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=LGRAY
    
    
def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=RGRAY
    

def get_pos(event): # this is executed when the title bar is clicked to move the window
    if root.maximized == False:
 
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        
        def move_window(event): # runs when window is dragged
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


        def release_window(event): # runs when window is released
            root.config(cursor="arrow")
            
            
        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)
    else:
        expand_button.config(text=" 🗖 ")
        root.maximized = not root.maximized

title_bar.bind('<Button-1>', get_pos) # so you can drag the window from the title bar
title_bar_title.bind('<Button-1>', get_pos) # so you can drag the window from the title 

# button effects in the title bar when hovering over buttons
close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
expand_button.bind('<Enter>', change_size_on_hovering)
expand_button.bind('<Leave>', return_size_on_hovering)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)


# some settings
root.bind("<FocusIn>",deminimize) # to view the window by clicking on the window icon on the taskbar
root.after(10, lambda: set_appwindow(root)) # to see the icon on the task bar
root.after(1, lambda: root.focus_force())