# coding=utf-8
#我把这个画布大小规定为500*500，单位移动距离为100像素点
import turtle
import time
turtle.screensize(500,500,'green')
turtle.pensize(15)#画笔大小
turtle.pencolor("yellow")#画笔颜色为黄色
#turtle.forward(100)
turtle.speed(1)
#设置单位移动距离
a=70
#起始位置是画布中心
#turtle.goto(40,60)#设置起始位置
#演示用数组，到时候要让硬件上传相关数组到程序执行绘图功能
#在数组里面有1.2.3.4.5，一共5个数字，1.2.3.4分别代表着小车当前方向的前后左右，并向此方向移动一个基本单位的距离，5则是回转180度，不执行移动动作
#move数组模拟移动
move=['1','1','1','4','1','1','3','1','1','5','1','1','1','1','1','1','1','1','3','1','4','1','1','5','1','1','1','1','1','1','5','3','1','3','1','5','1','1','1','1','5','1','1','1','3','1','3','1','1','1','1','4','1','4','1','1','1','1','1','1','3','1','1','3','1','1','3','1','3','1','5','1','4','1','3','1','1','3','1','4','1','1','1','3','1','5','1','4','1','1','3','1','5','1','3','1','3','1','4','1','3','1','3','1','1','4','1','1','3','1','1','3','1','4','1','5','1','1','5','1','3','1','1','3','1','3','1','5','1','4','1','4','1','3','1','3','1','1','1','5','1','1','1','4','3','4','1','3','1','1','4','1','1','1','1','1','4','1','4','1','5','1','4','1','3','1','1','1','3','1','3','1','4','1','1','4','1']
#turtle.fillcolor("red")
 
#turtle.begin_fill()
#for _ in range(5):
#  turtle.forward(200)
#  turtle.right(144)
#turtle.end_fill()
#time.sleep(2)
 
#turtle.penup()
#turtle.goto(-150,-120)
#turtle.color("violet")
#turtle.write("Done", font=('Arial', 40, 'normal'))
 


def forward():#绘制当前画笔方向前进(单位)像素点
    turtle.forward(a)
def backward():#绘制当前画笔方向后退(单位)像素点
    turtle.backward(a)
def right():#顺时针移动90度当前画笔
    turtle.right(90)
def left():#逆时针移动90度当前画笔
    turtle.left(90)
def swivel():#转体180度
    turtle.left(180)
for i in range(0,len(move)):
    if(move[i]=='1'):
        forward()
    if(move[i]=='2'):
        backward()
    if(move[i]=='3'):
        left()
    if(move[i]=='4'):
        right()
    if(move[i]=='5'):
        swivel()
turtle.write("Done", font=('Arial', 30, 'normal'))
turtle.mainloop()
