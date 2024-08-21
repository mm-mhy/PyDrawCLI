该项目由成都信息工程大学计算机学院相关指导老师以及数字媒体技术2021、2022届学生共同完成。

广大同学可以共同维护、优化项目。

该项目是基于textx库构建的一个基于绘图的领域特定语言，其中包含元模型，解析器代码，以及样例代码。
实现效果除简单的绘制基本几何图形，还有图形变换，设置线条颜色、大小，图形嵌套等功能，为脚本编程做支撑。
一些效果如：

![f1827277e1345b9c4e8c98b8b71c1f18_0](https://github.com/user-attachments/assets/0f0c4fbd-0468-4066-8c0c-c08f0c92fcd4)

实现图形变换的效果：

![fa37306c3eecfd045098dbcf27650d23_0](https://github.com/user-attachments/assets/b3f13b6e-f1e6-4d3c-ad4d-24ede424ace4)

DSL代码：

![7009150e52c5d5233d9b07c6127332f7](https://github.com/user-attachments/assets/4ef5229e-4d0f-44ba-a8b4-8316f6dab27a)


图形的线条颜色，线条大小，填充颜色可以继承，但是父类必须要定义出来，不能是空定义，样例如下：
s2,s3继承s1的线条颜色，线条大小，填充颜色，图形定义中s2重写了linesize为1，效果如下：
代码：
![image](https://github.com/user-attachments/assets/7934c26e-486b-4e89-b957-7f378db398ea)

效果图：
![image](https://github.com/user-attachments/assets/903e0b71-ea77-46b5-84ed-ccc48c94fcdf)

参考textx官方教程文档：https://tomassetti.me/domain-specific-languages-in-python-with-textx/
