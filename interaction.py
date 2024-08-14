import runpy
import sys
from pynput import keyboard
import interpreter_03

print()
print("PyDL 1.0.0 [Created by: @HuiTu_Cuit]")
print("Type 'exit' to exit the program, 'end' to end the shape creation, 'draw' to draw the shape, 'translate' to translate the shape, 'rotate' to rotate the shape, 'scale' to scale the shape")
print("Type 'help' to see the list of commands")
print()

#存储形状名称和形状类型的列表
class InterShape:
    def __init__(self, name:str, shape:str):
        self.name = name
        self.shape = shape

#自定义异常
class ShapeNameError(Exception):
    pass

#检查形状名称是否存在
def check_shape_name(user_input,name):
    isexist = False
    for shape in InteractionShapeList:
        if shape.name == name:
            isexist = True
            break
    if not isexist:
        raise ShapeNameError("Shape name does not exist")
    else:
        write_to_file(user_input)
        interpreter_03.main()

#写入文件，跟写
def write_to_file(content):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(content + "\n")

def main():
    #清空文件内容，保障下一次运行代码时内容从零开始
    with open(filename,"w", encoding='utf-8') as file:
        pass
    #进入输入循环，等待用户输入
    while True:
        user_input = input(">>> ")
        #提取指令特征
        input_commond=user_input.split()[0]
        #判断指令特征，执行相应操作
        if input_commond == "shape" or input_commond == "square" or input_commond == "circle":
            InteractionShapeList.append(InterShape(user_input.split()[1], user_input.split()[0]))
            shape_name=user_input.split()[1]
            write_to_file(user_input)
        #定义图形结束，写入文件
        elif input_commond == "end":
            print("<<< created a new shape named  "+shape_name)
            write_to_file(user_input)
        #退出，询问是否退出
        elif input_commond == "exit":
            print("<<< Exiting...(Y/N)")
            if input().upper() == "Y":
                sys.exit(0)
        #判断指令特征，执行相应操作
        elif input_commond == "draw" or input_commond == "translate" or input_commond == "rotate" or input_commond == "scale":
            try:
                check_shape_name(user_input,user_input.split()[1])
            except ShapeNameError as SN:
                print("<<< Shape Name Error: ",SN)
                continue
        #其余指令写入文件
        else:
            write_to_file(user_input)
    


if __name__ == "__main__":
    filename="output.turtle"
    InteractionShapeList = []
    shape_name=" "
    main()
