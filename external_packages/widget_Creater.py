import tkinter
class widget_creater:
    def create_labels(self,master,background,n,font = [],foreground = [],text = [],image = []):
        label_lst = []
        while(n>0):
            if(len(text)):
                label = tkinter.Label(master = master,text = text[0],font = font[0],bg = background[0],fg = foreground[0])
                del text[0]
                del font[0]
                del foreground[0] 
            elif(len(image)):
                photo = tkinter.PhotoImage(file = image[0])
                label = tkinter.Label(master = master,image = photo,bg = background[0])
                label.image = photo
                del image[0]
            del background[0]
            label_lst.append(label)
            n-=1
        return label_lst
    
    def create_buttons(self,master,width,height,background,activebackground,n,foreground = [],font = [],text = [],image = [],compound = []):
        button_lst = []
        while(n>0):
            if(len(text) and len(compound) and len(image)):
                photo = tkinter.PhotoImage(file = image[0])
                button = tkinter.Button(
                    master = master,width = width[0],height = height[0],bg = background[0],bd = 0,image = photo,compound = compound[0],
                    fg = foreground[0],font = font[0],activebackground = activebackground[0],text = text[0]
                    )
                button.image = photo
                del compound[0]
                del image[0]
                del foreground[0]
                del font[0]
                del text[0]
            elif(len(text) and len(compound)):
                button = tkinter.Button(
                    master = master,width = width[0],height = height[0],bg = background[0],bd = 0,font = font[0],
                    fg = foreground[0],activebackground = activebackground[0]
                )
                del text[0]
                del font[0]
                del foreground[0]
            elif(len(image)):
                photo = tkinter.PhotoImage(file = image[0])
                button = tkinter.Button(
                    master = master,width = width[0],height = height[0],bg = background[0],bd = 0,
                    image = photo,activebackground = activebackground[0]
                )
                button.image = photo
                del image[0]
            del width[0]
            del height[0]
            del background[0]
            del activebackground[0]
            button_lst.append(button)
            n-=1
        return button_lst
    
    def create_entry_box(self,master,width,background,insertbackground,font,n):
        entry_lst = []
        while(n>0):
            entry = tkinter.Entry(
                master = master,width = width,bg = background,insertbackground = insertbackground,font = font,bd = 0,
                exportselection = 0
            )
            entry_lst.append(entry)
            n-=1
        return entry_lst

    def create_text_box(self,master,width,height,background,insertbackground,font,n):
        text_lst = []
        while(n>0):
            text = tkinter.Text(
                master = master,width = width,height = height,bg = background,insertbackground = insertbackground,font = font,bd = 0,
                exportselection = 0
                )
            text_lst.append(text)
            n-=1
        return text_lst