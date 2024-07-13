from textx import metamodel_from_file 
import turtle
class Shape:
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y
    def __str__(self):
        return self.name
#采用二次贝塞尔曲线画法
def draw_curve_Bezier(points): 
    # for p in points:
    #     turtle.goto(p.x,p.y)
    #     turtle.write(str(p.x)+','+str(p.y))
    # turtle.up()
    # turtle.goto(points[0].x,points[0].y)
    # turtle.down()
    i=0
    while i<=1:
        f1=(1-i)**2
        f2=2*(1-i)*i
        f3=i**2
        x=f1*points[0].x+f2*points[1].x+f3*points[2].x
        y=f1*points[0].y+f2*points[1].y+f3*points[2].y
        turtle.goto(x,y)
        i+=0.1

def draw_shape(shape):
        turtle.pencolor(shape.line_color.color if shape.line_color is not None else 'black')
        turtle.fillcolor(shape.fill_color.color if shape.fill_color is not None else 'white')
        turtle.down()
        turtle.begin_fill()
        for l in shape.lines:
            draw_line(l)
        if shape.curves is not None:
            for c in shape.curves:
                draw_curve_Bezier(c.ctrlpoint)
        turtle.up() 
        turtle.end_fill()

#绘制直线
def draw_line(l):
        bearing = l.direction.bearing
        if bearing == 'E':
            turtle.setheading(0)
        elif bearing == 'NE':
            turtle.setheading(45)
        elif bearing == 'SE':
            turtle.setheading(-45)
        elif bearing == 'W':
            turtle.setheading(180)
        elif bearing =='NW':
            turtle.setheading(135)
        elif bearing =='SW':
            turtle.setheading(-135)
        elif bearing =='N':
            turtle.setheading(90)
        elif bearing =='S':
            turtle.setheading(-90)
        else:
            turtle.left(l.direction.angle.degrees)
        turtle.forward(l.length)
#整个场景的语句解析
def algorithm(scene):
    x=0
    y=0
#解析draw命令
    for d in scene.draw_instructions:
        x=d.x
        y=d.y
        turtle.penup()
        turtle.goto(d.x if d.x is not None else 0,
                d.y if d.y is not None else 0)

        #解析in命令
        if d.inwhere is not None:
            for s in Shapelist:
                if s.name == d.inwhere.shape.name:
                    x=s.x+d.x
                    y=s.y+d.y
                    turtle.goto(x,y)
        
        turtle.pendown()
        draw_shape(d.shape)
        shape=Shape(d.shape.name,d.x,d.y)
        Shapelist.append(shape)
        #解析内嵌文本命令
        if d.text is not None:
            turtle.goto(x,y-16)
            turtle.write(d.text.text)
  
            
#解析 print命令
    for p in scene.print:
        turtle.goto(p.x,p.y)
        turtle.write(p.text)
#解析circle命令
    for c in scene.circle:
        turtle.goto(c.x+ c.radius, c.y)
        draw_shape(c.shape)
        turtle.goto(c.x - c.radius, c.y)
        draw_shape(c.shape)
        turtle.goto(c.x, c.y + c.radius)
        draw_shape(c.shape)
        turtle.goto(c.x, c.y - c.radius)
        draw_shape(c.shape)




#主函数
Shapelist=[]
turtle_meta = metamodel_from_file("turtle.tx")
scene = turtle_meta.model_from_file("test_01.turtle")
turtle.Screen().title("图形绘制展示窗口")
turtle.hideturtle()
turtle.speed(0)
algorithm(scene)
turtle.done()
