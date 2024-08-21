import sys
import PyDrawCLI_Interpreter as interpreter
from pyreadline import Readline

#程序开始时用户提示
#该代码由成都信息工程大学数字媒体技术专业2021、22届学生共同完成
#该项目开源，欢迎各位同学共同参与维护、修正、完善
#项目地址：https://github.com/mm-mhy/PyDrawCLI
print()
print("PyDL 1.0.0 [Created by: @HuiTu_Cuit]")
print("Type 'exit' to exit the program, 'end' to end the shape creation, 'draw' to draw the shape, 'translate' to translate the shape, 'rotate' to rotate the shape, 'scale' to scale the shape")
print("Type 'help' to see the list of commands")
print()

#存储形状名称和形状类型的列表
class InterShape:
    def __init__(self,name:str,shape:str):
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
        interpreter.main()

#添加命令
def write_to_file(content):
    command_list.append(content)
    enter_file(command_list)

#撤销命令
def revalcation_from_file():
    string = command_list.pop()
    print(f"   Cancel the instruction: \"{string}\"")
    enter_file(command_list)
    if len(command_list) > 0:
        if command_list[len(command_list)-1].split()[0] in ['draw','translate','rotate','scale','drawline','drawcurve']:
            interpreter.main()

#写入文件
def enter_file(list):
    with open(filename,"w",encoding="utf-8") as file:
        for _ in list:
            file.write(_+"\n")

#指令补全
def complete(text, state):
    options = [i for i in commands if i.startswith(text)] + [None]
    return options[state]

#主函数
def main():
    #定义输入提示符
    command_symbol=">>> "
    #清空文件内容，保障下一次运行代码时内容从零开始
    with open(filename,"w",encoding="utf-8") as file:
        pass
    #进入输入循环，等待用户输入
    while True:
        input = completer.readline(command_symbol)
        #提取指令特征，由于采用readline输入，会多读一个换行
        user_input = input.replace("\n","")
        input_command = user_input.split()[0]
        #判断指令特征，执行相应操作
        if input_command in shapes:
            command_symbol="··· "
            InteractionShapeList.append(InterShape(user_input.split()[1],user_input.split()[0]))
            shape_name=user_input.split()[1]
            write_to_file(user_input)
        #定义图形结束，写入文件
        elif input_command == "end":
            command_symbol=">>> "
            print("   created a new shape named  "+shape_name)
            write_to_file(user_input)
        #退出程序
        elif input_command == 'exit':
            if  completer.readline("   Image not save,derectly exit?(Y/N): ").strip().upper() == "Y":
                print("   Exit the program")
                sys.exit(0)
        #判断指令特征，执行相应操作
        elif input_command in actions:
            try:
                if input_command == 'drawline' or input_command == 'drawcurve':
                    write_to_file(user_input)
                    interpreter.main()
                else:
                    check_shape_name(user_input,user_input.split()[1])
            except ShapeNameError as SN:
                print("   Shape name does not exist",SN)
                continue
        #撤销命令
        elif input_command == 'undo':
            if len(command_list) == 0:
                print("   No command to undo")
            else:
                revalcation_from_file()
        #显示指令列表
        elif input_command == 'help':
            print("   List of commands: ",sorted(commands))
        #其余指令写入文件
        else:
            write_to_file(user_input)
        
#程序主入口
if __name__ == "__main__":
    #定义指令列表
    help_commands = ['exit', 'end', 'draw', 'translate', 'rotate', 'scale', 'help','undo','drawline','drawcurve']
    shapes = ["shape","square","circle"]
    actions = ['draw','translate','rotate','scale','drawline','drawcurve']
    attributes = ['lines','linesize']
    commands = help_commands + shapes + actions + attributes
    #创建readline对象
    completer = Readline()
    #设置指令补全外部方法到对象内
    completer.set_completer(complete)
    #当遇到空格' '，制表符'\t'，换行符'\n'时，停止指令补全
    completer.set_completer_delims(' \t\n;')
    #当按下Tab键时，调用指令补全函数，开始补全指令
    completer.parse_and_bind('tab: complete') 
    #定义代码缓存文件名
    filename="output.turtle"
    shape_name=" "
    #保存图片命令状态
    saveimage_status=False
    #形状列表
    InteractionShapeList = []
    #指令列表，用于写入文件以及撤销操作
    command_list=[]
    main()    