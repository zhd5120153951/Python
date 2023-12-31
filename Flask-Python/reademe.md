# Flask框架部署前后端--前端(html,css,jquery,javascript)--后端(Python)

*what is new*

**2023.11.15**

# Django和Flask都是用于构建Web应用程序的Python web框架

1. 相同点：
    都是Python Web框架： Django和Flask都是用Python编写的，因此它们在语法和生态系统上有很多相似之处。

    MVC架构： 两者都支持MVC（模型-视图-控制器）或类似的设计模式，用于组织代码和分离关注点。

    ORM支持： Django和Flask都提供了对ORM（对象关系映射）的支持，使得与数据库的交互更为方便。

    可扩展性： 两者都支持通过插件或扩展来扩展功能。

2. 不同点：
    复杂度和约定大于配置：
    Django被设计为“约定大于配置”的框架，提供了大量内建功能，自动处理很多事情，使得开发更加快速，但有时可能显得笨重。Flask则是一个更轻量级的框架，它更注重灵活性和简单性，允许开发者更多地自行选择组件和工具。
    
    项目结构：
    Django提供了一个固定的项目结构，包括模型、视图、控制器等，这有助于快速开发大型应用。Flask的项目结构更加自由，允许开发者更灵活地组织代码。

    模板引擎：
    Django使用自带的模板引擎，有一套完整的模板语言。Flask允许选择模板引擎，它本身没有默认的模板引擎，但常用的有Jinja2。

    数据库支持：

    Django默认使用ORM系统，提供高级的数据库抽象，使得数据库操作更加方便。Flask对数据库的支持相对较低级，你可以选择使用ORM，也可以使用原生的SQLAlchemy等。

3. 用途和应用场景：
    Django适用于快速开发、大型应用、有强大的内建功能和完整的框架体系结构。
    Flask适用于小型到中型应用、对框架有更多控制权的开发者，以及需要更轻量级框架的项目。

    总体而言，选择使用Django还是Flask取决于项目的需求和开发者的偏好。如果你需要一个全功能的框架，而且你对项目结构和约定大于配置的理念比较认同，那么Django可能更适合你。如果你更喜欢灵活性，想要更自由地选择组件，并对项目的结构有更多控制，那么Flask可能更适合。


# Python线程和进程关系?
## 1. 实现方式：
   多线程：Python中的多线程是基于线程的，即多个线程在同一个进程内并发执行。
   多进程：Python中的多进程是基于进程的，即多个进程并发执行，每个进程都有自己独立的内存空间和系统资源。
## 2. 适用场景：
   多线程：适合于I/O密集型任务，如网络请求、文件读写等，因为这些任务需要等待I/O操作完成后才能继续执行。
   多线程可以在等待I/O操作的同时执行其他线程，提高程序的效率。
   多进程：适合于CPU密集型任务，如图像处理、数值计算等，因为这些任务需要大量的CPU计算资源，而多进程可以充分利用多核CPU，提高程序的效率。

# Json的知识点

## 1.load()和dump()
        1. json.load()：将一个文件中的json对象(str)转化为相对应的python对象
        2. json.loads()：将一个内存中json对象(str)转化为相对应的python对象
        3. json.dump()：将python的对象转化为对应的json对象(str),并存放在文件中
        4. json.dumps()：将python的对象转化为对应的json对象(str),并存在内存中

# logging日志记录

## 多进程日志和线程日志
    1.logging模块不跨进程--单进程或者多线程使用
    2.multiprocess-logging记录日志--需要安装此包,且多进程使用时,不可以进程间传logger,只能全局使用(在if之前)
