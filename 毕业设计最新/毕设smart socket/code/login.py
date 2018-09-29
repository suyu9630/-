from tkinter import *  
from tkinter.messagebox import *  
import os
class LoginPage(Frame):  
    def __init__(self):  
        super().__init__()  
        self.username = StringVar()  
        self.password = StringVar()  
        self.pack()  
        self.createForm()   
    def createForm(self):  
        Label(self).grid(row=0, stick=W, pady=10)  
        Label(self, text = '账户: ').grid(row=1, stick=W, pady=10)  
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)  
        Label(self, text = '密码: ').grid(row=2, stick=W, pady=10)  
        Entry(self, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)  
        Button(self, text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10)  
        Button(self, text='退出', command=self.quit).grid(row=3, column=1, stick=E)  
    def loginCheck(self):  
        name = self.username.get()  
        secret = self.password.get()  
        if name=='root' and secret=='123456':  
            os.system('python qt.py')
            self.destroy()           
        else:  
            showinfo(title='错误', message='账号或密码错误！')  
            # print('账号或密码错误！')  
          
root = Tk()  
root.title('蓝牙控制登录')  
width = 280  
height = 200  
screenwidth = root.winfo_screenwidth()    
screenheight = root.winfo_screenheight()   
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)  
root.geometry(alignstr)    # 居中对齐  
  
page1 = LoginPage()  
root.mainloop()  
