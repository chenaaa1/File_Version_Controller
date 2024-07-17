import os
import shutil
import tkinter
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox  # 引入弹窗库，防止解释器弹出报错。
import datetime
from tkinter import filedialog

# 初始常量设置
now_page = 0
log_datetime=0

# --------------------------窗口初始化1---------------------------
# 创建图形界面
root = tkinter.Tk()
root.title("坐忘道2.0的文档版本控制器")  # 窗口命名为用户名
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)  # 限制窗口大小

# 创建多行文本框
listbox = ScrolledText(root)
listbox.place(x=5, y=0, width=570, height=320)
# 文本框使用的字体颜色
listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')
listbox.insert(tkinter.END, '欢迎使用坐忘道2.0的文档版本控制器！', 'blue')

# 打开路径文件，读取里面的路径信息保存到变量中，预先设置路径文件保存在与代码同一目录处
# 注意这里的编码方式，要看一下你的txt文件是以什么格式保存的，我的是utf-8，对应下面的encoding解码方式
with open("./path.txt", "r", encoding='utf-8') as f:
    start_path_data = f.readlines()
    start_path = start_path_data[0].strip('\n')
    i = start_path_data[1]  # 这里要让用户自定义i的初始值，我这里设为1
    # start_path = f.readlines()
    # print('当前path.txt中显示的路径为：'+start_path)

# 创建一个保存文档的目录
# 打开当前目录
os.chdir(start_path)
# 判断当前目录是否存在一个叫document和log的文件夹，没有则创建，有则弹窗报错
new_log_folder = 'log'
new_document_folder = "document"
try:
    os.makedirs(new_log_folder)
    os.makedirs(new_document_folder)
    # print('目录创建成功')
except:
    print('folder is exit')
    # tkinter.messagebox.showerror(message='代码目录下document和log文件夹已存在，请删除')
    # exit(0)

# 定义下log和document的绝对路径
log_path = start_path + '\\' + new_log_folder
document_folder = start_path + '\\' + new_document_folder
key_path = start_path + '\\' + 'path.txt'
# print(key_path)
# print(log_path)
# print(document_folder)

# 打开log日志文件夹，在右边界面显示文件夹内信息
# print('log文件夹中内容如下：')
# print(os.listdir(start_path + '\\' + new_log_folder))

# 在右边展开一个新界面出来
root['height'] = 400
root['width'] = 900
# 创建展示log目录文件的列表框--------------
list2 = tkinter.Listbox(root)
list2.place(x=580, y=0, width=230, height=260)

# 展示log目录当前存在的文件
def show_log():
    global now_page
    # 将打印出来的数据截取出对应的文件名(这个有点巧妙）
    dir_res = []
    log_dir = os.listdir(start_path + '\\' + new_log_folder)
    for log_name in log_dir:
        dir_res.append(log_name)
    # print(dir_res)
    # print(len(dir_res))     # 打印列表长度
    # 由文件名判断名称是文件还是目录,然后染色插入列表中
    for i in range(14):
        # 防止数组越界
        if (now_page*14)+i <= len(dir_res)-1:
            name = dir_res[(now_page*14)+i].split(' ')[-1]
            # print(name)
            # 将名称插入列表
            list2.insert(tkinter.END, name)
            # 通过.txt号判断是否为文件或文件夹，从而赋予不同的颜色
            if '.txt' not in name:
                list2.itemconfig(tkinter.END, fg='orange')
            else:
                list2.itemconfig(tkinter.END, fg='blue')
    # print(dir_res[1])

# 下一页,一页最多显示14条数据
def next_page():
    global now_page
    now_page += 1
    list2.delete(0, tkinter.END)  # 清空列表框
    show_log()
# 上一页
def pre_page():
    global now_page
    if (now_page >= 1):
        now_page -= 1
    # print('pre: now_page -->' + str(now_page))
    list2.delete(0, tkinter.END)  # 清空列表框
    show_log()

# 上一页按钮
pre_page_button = tkinter.Button(root, text='上一页', command=pre_page)
pre_page_button.place(x=580, y=330, width=60, height=30)
# 下一页按钮
next_page_button = tkinter.Button(root, text='下一页', command=next_page)
next_page_button.place(x=660, y=330, width=60, height=30)

# 第一次先展示ftp界面，也顺手清一下列表框
list2.delete(0, tkinter.END)  # 清空列表框
show_log()
# --------------------------窗口初始化2---------------------------


# -------------------------增加log日志功能1---------------------------------------
# 获取当前时间，然后给日志文件进行命名，格式为i.时间戳
# 因为字符串拼接时i要为str类型，所以这里做个强转
def add_log():
    global log_path
    global i
    global log_datetime
    # 创建对应的空白txt文件
    file = open(log_path + '\\' + i + '.' + log_datetime + '.txt', 'w', encoding='utf-8')
    file.write('')
    file.close()
    # 然后让用户再打开这个txt文件进行编辑
    path = log_path + '\\' + i + '.' + log_datetime + '.txt'
    path_end = path.replace("/", '\\')
    # print(path_end)
    os.startfile(path)  # 打开txt文件，如果不存在，则创建


# 运行方法
# add_log()
# -------------------------显示log日志功能2---------------------------------------


# -------------------------显示日志信息功能1---------------------------------------
# 显示日志信息函数
def display():
    # 首先是当点击列表中的日志文件时，获取文件名称
    fileName_log = list2.get(list2.curselection())
    # 然后打开文件，读取信息
    with open(log_path + '\\' + fileName_log, "r", encoding='utf-8') as f:  # 打开文件
        data = f.read()  # 读取文件
        # print(data)
    # 将读取到的信息粘贴到显示框中
    listbox.delete("1.0", "end")  # 清空列表框
    listbox.insert(tkinter.END, data)   # 插入新数据

# 创建日志显示按钮
image_button = tkinter.Button(root, text='显示日志信息', command=display)
image_button.place(x=10, y=320, width=100, height=30)
# -------------------------显示日志信息功能2---------------------------------------


# --------------------------------------文档上传功能1---------------------------
def upload():
    global log_datetime
    global i
    # 首先是打开文件夹，然后让用户选择单个文件，获取到对应的文件的完整路径
    fileName_upload = tkinter.filedialog.askopenfilename()
    # 通过文件名截取出它的文件类型，类型命名为suffix
    suffix = fileName_upload.split('.')[-1]
    # 获取时间戳，调用add_log()功能来生成这个文档对应的日志
    log_datetime = datetime.datetime.now().strftime('%Y-%m-%d`%H`%M`%S')
    add_log()

    # 然后复制这个文件到document文件夹中，命名为i.时间戳.suffix
    creat_fileName_upload = document_folder + '\\' + i + '.' + log_datetime + '.' + suffix
    # print(creat_fileName_upload)
    # 开始复制
    if not os.path.isfile(fileName_upload):     # 如果要上传的文件不存在
        # print("%s not exist!" % (fileName_upload))
        tkinter.messagebox.showerror(message='你要上传的文件不存在！')
        exit(0)
    else:
        shutil.copy(fileName_upload, creat_fileName_upload)  # 复制文件
        # print("copy %s -> %s" % (fileName_upload, creat_fileName_upload))
    # 复制完成后，刷新一下右边的显示目录
    list2.delete(0, tkinter.END)  # 清空列表框
    show_log()

    # log和文档都创建完成后，再令i+1
    i = str(int(i) + 1)
    # 然后还要将i的值写回path.txt文件中
    file = open(key_path, 'w', encoding='utf-8')
    file.write(start_path + '\n' + i)
    file.close()

# 创建文档上传按钮
upload_button = tkinter.Button(root, text='上传文档', command=upload)
upload_button.place(x=150, y=320, width=100, height=30)
# --------------------------------------文档上传功能2---------------------------


# --------------------------------------下载对应文档功能1---------------------------
def download_docuemnt():
    # print('download_docuemnt is run')
    # 先获取document文件夹中的文件类型后缀suffix
    log_dir = os.listdir(document_folder)
    # 通过文件名截取出它的文件类型，类型命名为suffix
    suffix = log_dir[0].split('.')[-1]
    # 然后是获取用户点击的日志名称
    fileName_log = list2.get(list2.curselection())
    # 对名称进行处理，把其后缀由txt转为suffix
    download_filename = fileName_log.split('.txt')[0] + '.' + suffix
    # 拼接出要下载的文件的绝对路径
    download_path_filename = document_folder + '\\' + download_filename
    # 让用户打开电脑文件夹来选择文件存储路径（路径为文件夹类型）
    dir_path = tkinter.filedialog.askdirectory()
    # 这里要对目录路径进行一些小替换以符合格式，最后拼接成最终下载路径
    dir_path_end = dir_path.replace("/", '\\') + '\\' + download_filename
    # 然后拷贝文件即可
    shutil.copy(download_path_filename, dir_path_end)  # 复制文件


# 创建文档上传按钮
download_button = tkinter.Button(root, text='下载对应文档', command=download_docuemnt)
download_button.place(x=290, y=320, width=100, height=30)
# --------------------------------------下载对应文档功能2---------------------------


# --------------------------------------右边目录框中进入目录功能1---------------------------
# def join():
#     global now_page
#     # 获取到要进入的文件夹的名称，注意这里获取到的不是绝对路径
#     fileName_join = list2.get(list2.curselection())
#     print(fileName_join)
#     # 将打印出来的数据截取出对应的文件名(这个有点巧妙）
#     dir_res = []
#     log_dir = os.listdir(log_path + '\\' + fileName_join)
#     print(log_dir)
#     for log_name in log_dir:
#         dir_res.append(log_name)
#     # 首先要清空目录，再重载
#     list2.delete(0, tkinter.END)  # 清空列表框
#     # 由文件名判断名称是文件还是目录,然后染色插入列表中
#     for i in range(14):
#         # 防止数组越界
#         if (now_page * 14) + i <= len(dir_res) - 1:
#             name = dir_res[(now_page * 14) + i].split(' ')[-1]
#             # print(name)
#             # 将名称插入列表
#             list2.insert(tkinter.END, name)
#             # 通过.txt号判断是否为文件或文件夹，从而赋予不同的颜色
#             if '.txt' not in name:
#                 list2.itemconfig(tkinter.END, fg='orange')
#             else:
#                 list2.itemconfig(tkinter.END, fg='blue')
# # 进入子目录按钮
# download_button_ftp = tkinter.Button(root, text='进入目录', command=join)
# download_button_ftp.place(x=740, y=330, width=60, height=30)
# --------------------------------------右边目录框中进入目录功能2---------------------------


# --------------------------------------右边目录框中返回上一层目录功能1---------------------------
# def Back():
#     print('Back funcition')
# # 返回上一层目录按钮
# download_button_ftp = tkinter.Button(root, text='返回上一层目录', command=Back)
# download_button_ftp.place(x=720, y=360, width=105, height=30)
# --------------------------------------右边目录框中返回上一层目录功能2---------------------------


# 让显示框一直存在不消失
root.mainloop()