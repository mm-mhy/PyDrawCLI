from textx import metamodel_from_file 
import turtle
import math
import Basic_trans as bt



#shape类，用于存储模型信息，包含名称、开始位置、顶点点集
class Shape:
    def __init__(self, name: str, x: int, y: int,linecolor:str,linesize:str,fillcolor:str):
        self.name = name
        self.x = x
        self.y = y
        self.linecolor=linecolor
        self.linesize=linesize
        self.fillcolor=fillcolor
        self.points = []
    def __str__(self):
        return self.name


#设置图形线条颜色、线条粗细、填充颜色，含有默认选项
def get_shape_properties(shape):
    # 获取当前形状的属性
    linecolor = getattr(shape.line_color, 'color', 'black') or "black"
    linesize = getattr(shape.line_size, 'size', 1) or 1
    fillcolor = getattr(shape.fill_color, 'color', '') or ""

    # 检查是否存在继承
    parent_shape = shape.extends
    if parent_shape is not None:
        # 遍历 Shape 列表寻找父形状
        for shape in Shapelist:
            if shape.name == parent_shape.name:
                # 仅在当前属性为 None 时才使用父类形状的属性
                linecolor = (getattr(shape.line_color, 'color', None) or shape.linecolor) 
                linesize = (getattr(shape.line_size, 'size', None) or shape.linesize)
                fillcolor = (getattr(shape.fill_color, 'color', None) or shape.fillcolor)
                break  # 找到后可以退出循环

    return linecolor, linesize, fillcolor


#一、解析背景指令
def bgcolor_instrusction(color:str):
    bgcolor=color
    turtle.bgcolor(color)

#二、解析坐标轴指令
def axis_instrusction(isaxis:bool):
    if isaxis:
        draw_axis()

#三、解析绘制指令
def draw_instruction(draw_instructions):
    x=0
    y=0

    for d in draw_instructions:
        x=d.x
        y=d.y
        points=[]
        curves_points=[]
        linecolor, linesize, fillcolor = get_shape_properties(d.shape)
        #解析in命令
        # if d.inwhere is not None:
        #     for s in Shapelist:
        #         if s.name == d.inwhere.shape.name:
        #             x=s.x+d.x
        #             y=s.y+d.y
        #             turtle.goto(x,y)
        turtle.penup()
        turtle.goto(d.x if d.x is not None else 0,d.y if d.y is not None else 0)
        turtle.pendown()
        if "Shape" in str(d.shape):
            draw_shape(d.shape,linecolor,linesize,fillcolor)
            lines_points,curves_points= get_point(d.shape,d.x,d.y)
            points.append(lines_points)
            points.append(curves_points)

        #执行画圆
        elif "Circle" in str(d.shape):
            draw_circle(d.shape,d.x,d.y,linecolor,linesize,fillcolor)
            points=get_point(d.shape,d.x,d.y)
        #执行画矩形
        elif "Square" in str(d.shape):
            draw_square(d.shape,d.x,d.y,linecolor,linesize,fillcolor)
            points=get_point(d.shape,d.x,d.y)

        shape=Shape(d.shape.name,d.x,d.y,linecolor,linesize,fillcolor)
        shape.points=points
        
        Shapelist.append(shape)
        # points=get_point(shape,Shapelist)
        # shape.points=points
        #添加到shape列表中，把绘制过的每一个几何体保存
        #解析内嵌文本命令
        # if d.text is not None:
        #     turtle.goto(x,y-16)
        #     turtle.write(d.text.text)

#四、解析打印指令
def print_instruction(print):
    for p in print:
        turtle.goto(p.x,p.y)
        turtle.write(p.text)

#五、解析变换指令
def transform_instruction(trans):
 
    for t in trans:       
        if t.translate is not None:
            for _ in Shapelist:
                if _.name == t.translate.shape.name:
                    shapeobject=_ 
            transform(t.translate,shapeobject,"translation")
        if t.rotate is not None:
            for _ in Shapelist:
                if _.name == t.rotate.shape.name:
                    shapeobject=_  
            transform(t.rotate,shapeobject,"rotation")
        if t.scale is not None:
            for _ in Shapelist:
                if _.name == t.scale.shape.name:
                    shapeobject=_ 
            transform(t.scale,shapeobject,"scale")

#六、解析连续绘制直线指令
def drawline_instruction(drawlines):
    for d in drawlines:
        points=points_to_list(d.points)
        turtle.goto(points[0][0],points[0][1])
        turtle.pendown()
        for i in range(1,len(points)):
            turtle.goto(points[i][0],points[i][1])
        turtle.penup()

# 绘制坐标轴的线段
def draw_axis_line(start, end):
    turtle.up()
    turtle.goto(start)
    turtle.down()
    turtle.goto(end)

 #绘制坐标轴的刻度和标签
def draw_tick(x, y, is_vertical=True):
    turtle.up()
    if is_vertical:
        turtle.goto(-10, y)  # 刻度线
        turtle.down()
        turtle.goto(10, y)
        turtle.up()
        turtle.goto(-30, y)  # 标签位置
    else:
        turtle.goto(x, -10)  # 刻度线
        turtle.down()
        turtle.goto(x, 10)
        turtle.up()
        turtle.goto(x, -30)  # 标签位置
    
    # 写标签
    label = y if is_vertical else x
    turtle.write(label, align="center")

#绘制坐标轴的箭头
def draw_arrow(x, y, direction='horizontal'):
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    if direction == 'horizontal':
        turtle.goto(x - 10, y + 10)  # 右侧箭头
        turtle.goto(x - 10, y - 10)
    else:
        turtle.goto(x + 10, y - 10)  # 上侧箭头
        turtle.goto(x - 10, y - 10)
    turtle.goto(x, y)

#绘制坐标轴
def draw_axis():
    turtle.pencolor('black')
    turtle.pensize(2)

    # 绘制X轴
    draw_axis_line((-400, 0), (400, 0))

    # 添加X轴刻度和标签
    for x in range(-400, 401, 50):
        draw_tick(x, 0, is_vertical=False)

    # 绘制Y轴
    draw_axis_line((0, 400), (0, -400))

    # 添加Y轴刻度和标签
    for y in range(-400, 401, 50):
        draw_tick(0, y, is_vertical=True)

    # 添加箭头
    draw_arrow(420, 0, 'horizontal')  # 右侧箭头
    draw_arrow(0, 420, 'vertical')    # 上侧箭头

#将模型的曲线点集转化为一般二维数组
def points_to_list(points):
    list=[]
    for i in points:
        list.append((i.x,i.y))
    return list

#采用二/三次贝塞尔曲线画法
def draw_curve_Bezier(points): 
    turtle.penup()
    turtle.goto(points[0][0],points[0][1])
    turtle.pendown()
    num_points = len(points)
    #判定控制点个数，根据不同情况调用不同函数
    if num_points == 3:
        i=0
        while i<=1:
          f1=(1-i)**2
          f2=2*(1-i)*i
          f3=i**2
          x=f1*points[0][0]+f2*points[1][0]+f3*points[2][0]
          y=f1*points[0][1]+f2*points[1][1]+f3*points[2][1]
          turtle.goto(x,y)
          i+=0.1
    #判定控制点个数，根据不同情况调用不同函数
    elif num_points ==4:
        i = 0
        while i <= 1:
          f1 = (1 - i) ** 3
          f2 = 3 * (1 - i) ** 2 * i
          f3 = 3 * (1 - i) * i ** 2
          f4 = i ** 3
          x = f1 * points[0][0] + f2 * points[1][0] + f3 * points[2][0] + f4 * points[3][0]
          y = f1 * points[0][1] + f2 * points[1][1] + f3 * points[2][1] + f4 * points[3][1]
          turtle.goto(x, y)
          i += 0.01 

#自定义几何图形，可绘制曲线和直线
def draw_shape(shape,linecolor,linesize,fillcolor):
        turtle.pencolor(linecolor)
        turtle.fillcolor(fillcolor)
        turtle.pensize(linesize)
        turtle.pendown()
        turtle.begin_fill()
        #画直线
        for l in shape.lines:
            draw_line(l)
        #画曲线
        if shape.curves is not None:
            for c in shape.curves:
                draw_curve_Bezier(points_to_list(c.ctrlpoint)) 
        turtle.end_fill()
        turtle.penup()
    

#画圆（含椭圆）
def draw_circle(circle,x,y,linecolor,linesize,fillcolor):
    turtle.pencolor(linecolor)
    turtle.fillcolor(fillcolor)
    turtle.pensize(linesize)
    radii = circle.radius.r   
    turtle.begin_fill()
    

    if len(radii) == 1:
        radius = radii[0]  # 正圆情况
        turtle.penup() 
        turtle.goto(x, y)
        turtle.pendown()
        turtle.circle(radius)  # 绘制圆

    elif len(radii) == 2:       
        a = radii[0]  # 横半轴
        b = radii[1]  # 纵半轴
        # 绘制椭圆
        turtle.penup()
        turtle.goto(x + a, y)
        turtle.pendown()

        for angle in range(360):  # 用角度从 0 到 360 绘制椭圆
            x_coord = x + a * math.cos(math.radians(angle))  # 计算横坐标
            y_coord = y + b * math.sin(math.radians(angle))  # 计算纵坐标
            turtle.goto(x_coord, y_coord)  # 移动到新位置
        turtle.penup()
        turtle.goto(x + a, y)  # 返回到起始位置
    turtle.end_fill()

#正方形（两种方法）
def draw_square(square,x,y,linecolor,linesize,fillcolor):
    turtle.pencolor(linecolor)
    turtle.fillcolor(fillcolor)
    turtle.pensize(linesize)
    turtle.begin_fill()
    if hasattr(square.special, 'width') and hasattr(square.special, 'height'):
        turtle.penup()
        turtle.goto(x,y)
        side_width=square.special.width
        side_height=square.special.height
        turtle.pendown() 

        for _ in range(2):  # 绘制四条边
            turtle.forward(side_width)  # 向前移动宽度
            turtle.right(90)  # 右转90度
            turtle.forward(side_height)  # 向前移动高度
            turtle.right(90)  # 右转90度
        

    elif hasattr(square.special, 'x1') and hasattr(square.special,'y1'):
        x1=square.special.x1
        y1=square.special.y1
        width=x1-x
        height=y-y1
        turtle.penup()
        turtle.goto(x,y)
        turtle.pendown()
        
        for _ in range(2):  # 绘制四条边
            turtle.forward(width)  # 向前移动宽度
            turtle.right(90)  # 右转90度
            turtle.forward(height)  # 向前移动高度
            turtle.right(90)  # 右转90度
        
    turtle.end_fill()   
    turtle.penup() 
   
#绘制直线
def draw_line(l):
    # 定义方向与对应的角度映射
    bearing_map = {
        'E': 0,
        'NE': 45,
        'SE': -45,
        'W': 180,
        'NW': 135,
        'SW': -135,
        'N': 90,
        'S': -90,
    }

    # 获取要设置的角度
    bearing = bearing_map.get(l.direction.bearing, None)
    
    if bearing is not None:
        turtle.setheading(bearing)
    else:
        # 如果没有对应的预定义方向，使用给定角度
        turtle.left(l.direction.angle.degrees)

    # 移动指定的长度
    turtle.forward(l.length)

#得到顶点
def get_point(shape,start_point_X,start_point_Y):

    shape_lines_points=[]
    shape_curves_points=[]
    square_points=[]
    after_trans_points=[]
    
    if "Shape" in str(shape):
        #拿到shape的顶点并发生变换
        shape_lines_points,shape_curves_points=caculate_shape_point(shape,start_point_X,start_point_Y)
        return shape_lines_points,shape_curves_points

    elif "Square" in str(shape):
        #拿到square的顶点并发生变换
        square_points=caculate_square_point(shape,start_point_X,start_point_Y)
        return square_points

    #拿到circle的顶点，似乎没用,这一块留着不动
    elif "Circle" in str(shape):       
        return (start_point_X,start_point_Y)

    else:
        print("error")

#计算shape的顶点
def caculate_shape_point(shape,x1,y1):
    lines_points=[]#保存直线的顶点，直线是连续的
    lines_points.append((x1,y1))
    curves_points=[]#保存曲线的顶点
    for line in shape.lines:
        if line.direction.bearing == 'E':
            x2=x1+line.length
            y2=y1

        elif line.direction.bearing == 'NE':
            x2=x1+math.cos(45)*line.length
            y2=y1+math.sin(45)*line.length

        elif line.direction.bearing == 'SE':
            x2=x1+math.cos(45)*line.length
            y2=y1-math.sin(45)*line.length

        elif line.direction.bearing == 'W':
            x2=x1-line.length
            y2=y1

        elif line.direction.bearing =='NW':
            x2=x1-math.cos(45)*line.length
            y2=y1+math.sin(45)*line.length

        elif line.direction.bearing =='SW':
            x2=x1-math.cos(45)*line.length
            y2=y1-math.sin(45)*line.length
            
        elif line.direction.bearing =='N':
            x2=x1
            y2=y1+line.length

        elif line.direction.bearing =='S':
            x2=x1
            y2=y1-line.length

        else:
            turtle.left(line.direction.angle.degrees)
            x2=x1+math.cos(line.direction.angle.radians)*line.length
            y2=y1+math.sin(line.direction.angle.radians)*line.length

        x1=x2
        y1=y2
        lines_points.append((x2,y2))

    for curve in shape.curves:
        ctrl_points=[]
        for cp in curve.ctrlpoint:
            ctrl_points.append((cp.x,cp.y))
        curves_points.append(ctrl_points)

    return lines_points,curves_points

#计算square的顶点
def caculate_square_point(shape,x1,y1):
    points=[]
    if hasattr(shape.special, 'width') and hasattr(shape.special, 'height'):
        points.append((x1,y1))
        points.append((x1+shape.special.width,y1))
        points.append((x1+shape.special.width,y1-shape.special.height))
        points.append((x1,y1-shape.special.height))
    elif hasattr(shape.special, 'x1') and hasattr(shape.special,'y1'):
        points.append((x1,y1))
        points.append((shape.special.x1,y1))
        points.append((shape.special.x1,shape.special.y1))
        points.append((x1,shape.special.y1))
    return points


# 变换主函数
def transform(trans,shapeobject,transform_type):
    turtle.clear()
    shape=trans.shape
    start_point_X=shapeobject.x
    start_point_Y=shapeobject.y
    trans_X=0
    trans_Y=0
    roate_angle=0
    scale_X=0
    scale_Y=0
    points=shapeobject.points
    if transform_type=='translation':
        trans_X=trans.x
        trans_Y=trans.y

    elif transform_type=='rotation':
        roate_angle=trans.angle

    elif transform_type=='scale':
        scale_X=trans.x
        scale_Y=trans.y

    if "Shape" in str(shape):
        shape_lines_points,shape_curves_points=shapeobject.points
        # print(shapeobject.points)
        """这里填顶点平移变换函数,用一个或多个列表保存变换后的顶点，后续我来对这个新顶点列表处理,这里有直线和曲线的列表，应当调用两次变换函数，用两个列表保存变换后的顶点"""
        #############
        if shape_lines_points is not None:
            if(transform_type=='translation'):
                new_shape_lines_points=bt.translation(shape_lines_points,trans_X,trans_Y)
                shapeobject.points[0]=new_shape_lines_points

            elif (transform_type=='rotation'):
                new_shape_lines_points=bt.rotation(shape_lines_points,roate_angle)
                shapeobject.points[0]=new_shape_lines_points

            elif (transform_type=='scale'):
                new_shape_lines_points=bt.scale(shape_lines_points,scale_X,scale_Y)
                shapeobject.points[0]=new_shape_lines_points

            turtle.penup()
            turtle.goto(new_shape_lines_points[0][0],new_shape_lines_points[0][1])
            linecolor, linesize, fillcolor = get_shape_properties(shape)
            turtle.pencolor(linecolor)
            turtle.fillcolor(fillcolor)
            turtle.pensize(linesize)
            turtle.pendown()
            turtle.begin_fill()
            for i in range(len(new_shape_lines_points)):
                turtle.goto(new_shape_lines_points[i][0],new_shape_lines_points[i][1])
            turtle.end_fill()
            turtle.penup()

        if shape_curves_points is not None:
            for i in range(len(shape_curves_points)):
                if(transform_type=='translation'):
                    new_shape_curves_points=bt.translation(shape_curves_points[i],trans_X,trans_Y)
                    shapeobject.points[1][i]=new_shape_curves_points

                elif (transform_type=='rotation'):
                    new_shape_curves_points=bt.rotation(shape_curves_points[i],roate_angle)
                    shapeobject.points[1][i]=new_shape_curves_points
                    
                elif (transform_type=='scale'):
                    new_shape_curves_points=bt.scale(shape_curves_points[i],scale_X,scale_Y)
                    shapeobject.points[1][i]=new_shape_curves_points

                turtle.penup()
                turtle.goto(new_shape_curves_points[0][0],new_shape_curves_points[0][1])
                linecolor, linesize, fillcolor = get_shape_properties(shape)
                turtle.pencolor(linecolor)
                turtle.fillcolor(fillcolor)
                turtle.pensize(linesize)
                turtle.begin_fill()
                turtle.pendown()
                draw_curve_Bezier(new_shape_curves_points)
                turtle.end_fill()
                turtle.penup()
        #############

    elif "Square" in str(shape):
        square_points=shapeobject.points
        print(square_points)
        #############
        if (transform_type=='translation'):
            new_square_points=bt.translation(square_points,trans_X,trans_Y)
            shapeobject.points=new_square_points
            
        elif (transform_type=='rotation'):
            new_square_points=bt.rotation(square_points,roate_angle)
            shapeobject.points=new_square_points

        elif (transform_type=='scale'):
            new_square_points=bt.scale(square_points,scale_X,scale_Y)
            print(new_square_points)
            shapeobject.points=new_square_points

        turtle.penup()
        turtle.goto(new_square_points[0][0],new_square_points[0][1])
        linecolor, linesize, fillcolor = get_shape_properties(shape)
        turtle.pencolor(linecolor)
        turtle.fillcolor(fillcolor)
        turtle.pensize(linesize)
        turtle.pendown()
        turtle.begin_fill()
        for i in range(len(new_square_points)):
            turtle.goto(new_square_points[i][0],new_square_points[i][1])
        turtle.goto(new_square_points[0][0],new_square_points[0][1])
        turtle.end_fill()
        turtle.penup()
        #############

    elif "Circle" in str(shape):
            circle_points = [(shapeobject.x, shapeobject.y)]
            if (transform_type=='translation'):
                new_circle_points=bt.translation(circle_points,trans_X,trans_Y)
        #后期应用椭圆   圆也可以
            elif (transform_type=='rotation'):
                new_circle_points=bt.rotation(circle_points,roate_angle)
            
            elif (transform_type=='scale'):
                new_circle_points=bt.scale(circle_points,scale_X,scale_Y)
            

            linecolor,linesize,fillcolor=get_shape_properties(shape)
            x=new_circle_points[0][0]
            y=new_circle_points[0][1]
            draw_circle(shape,x,y,linecolor,linesize,fillcolor)
        
    else:
        print("error")
    

#整个场景的语句解析
def algorithm(scene):
    #一、解析背景颜色指令
    bgcolor_instrusction(scene.background_color.color if scene.background_color is not None else "white")
    #二、解析坐标轴指令
    axis_instrusction(scene.axis.isaxis if scene.axis is not None else False)
    #三、解析绘制指令
    draw_instruction(scene.draw_instructions)
    #四、解析打印指令
    print_instruction(scene.print)
    #五、解析变换指令
    transform_instruction(scene.transform)
    #六、解析连续绘制直线指令
    drawline_instruction(scene.drawlines)

#主函数
def main():
    try:
        turtle_meta = metamodel_from_file("test_01/turtle.tx")
        scene = turtle_meta.model_from_file("test_01/test.turtle")
        turtle.Screen().title("图形绘制展示窗口")
        turtle.hideturtle()
        turtle.speed(0)
        algorithm(scene)
        turtle.done()
    except FileNotFoundError:
        print("Error: Required file not found. Please ensure 'turtle.tx' and 'test.turtle' are in the correct location.")
    except turtle.Terminator:
        print("Error: The drawing process was unexpectedly terminated.")
    except Exception as e:
        # 捕获其他未处理的异常，并提供用户提示
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    Shapelist=[]
    main()
