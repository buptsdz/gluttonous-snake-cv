import cv2
from cvzone.HandTrackingModule import HandDetector
import tkinter as tk
from PIL import Image, ImageTk,ImageSequence
import time
from sg import SnakeGameClass
from music import musics
import os
import random

script_dir = os.path.dirname(os.path.abspath(__file__))
donut_path = os.path.join(script_dir, "photos", "Donut.jpg")
chang_path = os.path.join(script_dir, "photos", "chang.png")
tiao_path = os.path.join(script_dir, "photos", "tiao.png")
rap_path = os.path.join(script_dir, "photos", "rap.png")
lanqiu_path = os.path.join(script_dir, "photos", "lanqiu.png")
music_path = os.path.join(script_dir, "photos", "music.png")
head_path = os.path.join(script_dir, "photos", "zhongfen.png")
history_path = os.path.join(script_dir, "history.txt")
beiyou_path=os.path.join(script_dir, "photos", "beiyou.png")

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 800)  # height
prev_frame_time = 0
detector = HandDetector(detectionCon=0.7, maxHands=1)

def close_window():
    window.destroy()

def minimize_window():
    window.iconify()

# 创建窗口
window = tk.Tk()
window.title("Snake Game")
window.attributes("-fullscreen", False)  # 全屏显示

# 创建游戏对象
food_path=[chang_path,tiao_path,rap_path,lanqiu_path,music_path]
game = SnakeGameClass(food_path,head_path)

#图片路径
yanfei_path = os.path.join(script_dir, "photos", "yanfei.png")
shenlilinghua_path =os.path.join(script_dir, "photos", "shenlilinghua.png")
xiaogong_path =os.path.join(script_dir, "photos", "xiaogong.png")
ganyu_path =os.path.join(script_dir, "photos", "ganyu.png")

# 打开原始图片
yanfei = Image.open(yanfei_path)
shenlilinghua = Image.open(shenlilinghua_path)
xiaogong = Image.open(xiaogong_path)
ganyu = Image.open(ganyu_path)

# 缩放图片
yanfei= yanfei.resize((300, 300))
shenlilinghua = shenlilinghua.resize((300, 300))
xiaogong = xiaogong.resize((300, 300))
ganyu = ganyu.resize((300, 300))

# 将缩放后的图片转换为tkinter.PhotoImage对象
yanfei = ImageTk.PhotoImage(yanfei)
shenlilinghua = ImageTk.PhotoImage(shenlilinghua)
xiaogong = ImageTk.PhotoImage(xiaogong)
ganyu = ImageTk.PhotoImage(ganyu)

#转为tk的laber对象
label_wife1= tk.Label(window, image=yanfei)
label_wife2= tk.Label(window, image=shenlilinghua)
label_wife3= tk.Label(window, image=xiaogong)
label_wife4= tk.Label(window, image=ganyu)

canvas = None  # 画布对象
start_button = None  # 开始按钮
quit_button=None
restart_button = None  # 重新开始按钮
reset_flag = 0
update_flag = 0
score_label=None
gameover_label=None
image=None
countdown_flag=0
start_time=0
flag_random=0
score_window=None
history=0

#获取文件
history_file = open(history_path, 'r')
try:
    history = int(history_file.read())
except ValueError:
    history = 0
# 关闭文件
history_file.close()

# 读取 GIF 图像
gif_path=os.path.join(script_dir, "photos", "snake.gif")
gif = Image.open(gif_path)

# 获取 GIF 图像的每一帧
frames = []
for frame in ImageSequence.Iterator(gif):
    frames.append(ImageTk.PhotoImage(frame))

# 创建显示 GIF 图像的 Label
gif_label = tk.Label(window)
gif_label.pack()

# 更新 GIF 图像的显示
def update_frame(index):
    gif_label.config(image=frames[index])
    window.after(100, update_frame, (index + 1) % len(frames))

# 设置 GIF 图像的位置
gif_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# 开始播放 GIF 图像
update_frame(0)

# 创建beiyou的 PhotoImage 对象
beiyou = Image.open(beiyou_path)
beiyou = ImageTk.PhotoImage(beiyou)

def update_high_score(path):#更新文件中最高分
    # 读取txt文件中的数值
    with open(path, 'r') as file:
        content = file.read()
        max_value = int(content) if content else 0

    if game.score >= max_value:
        with open(path, 'w') as file:
            file.write(str(game.score))

def clear_history_callback():#清空历史记录
    global history
    history = 0
    with open(history_path, 'w') as file:
        file.write('0')
    history_label.config(text=f"历史最高: {history}")

def update_history():#清空历史记录
    global history
    with open(history_path, 'r') as file:
        history=int(file.read())

def close_score_window():
    global score_window
    score_window.destroy()

def show_score(score):
    global flag_random,history_path,history,score_window,history
    # 创建一个新窗口
    score_window = tk.Toplevel()
    score_window.title("玩原神导致的")
    score_window.protocol("WM_DELETE_WINDOW", close_score_window)

    # 设置窗口尺寸
    width = 350
    height = 250
    # 获取屏幕尺寸
    screen_width = score_window.winfo_screenwidth()
    screen_height = score_window.winfo_screenheight()

    if flag_random==0:
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        score_window.geometry(f"{width}x{height}+{x}+{y}")
        score_window.resizable(False, False)  # 禁用窗口的调整大小功能

    else:
        # 计算窗口位置的随机范围
        x_range = screen_width - width
        y_range = screen_height - height

        # 生成随机位置坐标
        xran = random.randint(0, x_range)
        yran = random.randint(0, y_range)

        # 设置窗口位置
        score_window.geometry(f"{width}x{height}+{xran}+{yran}")
        score_window.resizable(False, False)  # 禁用窗口的调整大小功能

    def reopen():
        global flag_random
        if score_window.winfo_exists():  # 检查窗口是否存在
            score_window.destroy()  # 删除当前窗口
        if flag_random==0:
            flag_random=1
        show_score(game.score)  # 重新打开当前窗口

    # 创建显示得分的标签
    score_label = tk.Label(score_window, text=f"你的得分: {score}", font=("Helvetica", 14))
    score_label.place(relx=0.5, rely=0.2, anchor="center")

    if score<=history:
        #历史得分
        history_label =tk.Label(score_window, text=f"历史最高: {history}", font=("Helvetica", 12))
        history_label.place(relx=0.5, rely=0.3, anchor="center")

        # 创建标签并显示图片
        beiyou_label = tk.Label(score_window, image=beiyou)
        beiyou_label.place(relx=0.5, rely=0.55, anchor="center")

        # 创建其他文本标签
        text_label = tk.Button(score_window, text="原神", font=("Helvetica", 12), command=reopen,
                               padx=48, pady=2)
        text_label.place(relx=0.27, rely=0.85, anchor="center")

        # 添加关闭按钮
        close_button = tk.Button(score_window, text="启动！", font=("Helvetica", 12), command=reopen,
                                 padx=47, pady=2)
        close_button.place(relx=0.73, rely=0.85, anchor="center")

    else:
        history_label = tk.Label(score_window, text=f"恭喜你！成为历史最高: {score}", font=("Helvetica", 12))
        history_label.place(relx=0.5, rely=0.45, anchor="center")

        # 添加关闭按钮
        close_button = tk.Button(score_window, text="原神怎么你了", font=("Helvetica", 12), command=close_score_window,
                                 padx=45, pady=3)
        close_button.place(relx=0.5, rely=0.85, anchor="center")

    def update_window():
        if score_window.winfo_exists():  # 检查窗口是否存在
            score_window.update()  # 更新窗口，处理事件
            score_window.after(100, update_window)  # 定时调用更新函数
        else:
            pass
    # 第一次调用更新函数
    update_window()

def show_start_screen():
    global canvas, start_button, quit_button, image, history_label,history

    # 清空画布
    if canvas:
        canvas.destroy()

    # 创建开始按钮
    start_button = tk.Button(window, text="Start Game", command=start_game,relief=tk.RAISED, borderwidth=5)
    start_button.place(in_=gif_label, relx=0.5, rely=1, anchor=tk.N)
    button_font1 = ("Arial", 36)
    start_button.configure(font=button_font1)

    # 创建退出按钮
    quit_button = tk.Button(window, text="Quit", command=window.quit)
    quit_button.place(in_=start_button, relx=0.5, rely=1, anchor=tk.N, y=10)
    button_font2 = ("Arial", 24)
    quit_button.configure(font=button_font2)

    # 历史得分
    history_label = tk.Label(window, text=f"历史最高: {history}", font=("Helvetica", 20),height=1,width=10)
    history_label.place(relx=0.3, rely=0.7, anchor="center")

    # 清空历史按钮
    clear_history_button = tk.Button(window, text="Clear History", command=clear_history_callback)
    clear_history_button.place(relx=0.3, rely=0.75, anchor="center")

    # 放置图片
    label_wife2.place(relx=0.02, rely=0.3)
    label_wife3.place(relx=0.78, rely=0.3)

    # 播放音乐
    musics.playpagemusic()

def update_game():
    global update_flag,prev_frame_time
    if update_flag:
        success, img= cap.read()
        img = cv2.flip(img, 1)
        # 更新当前帧的时间
        new_frame_time = time.time()

        # 计算帧率
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)

        cv2.putText(img, f'FPS: {fps}', (1140, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)

        hands = detector.findHands(img, flipType=False, draw=False)
        if hands:
            lmList = hands[0]['lmList']
            pointindex = lmList[8][0:2]
            img = game.update(img, pointindex)

        # 将OpenCV图像转换为Tkinter图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        # 更新画布上的图像
        canvas.img = img
        canvas.create_image(0, 0, anchor=tk.NW, image=img)

        # 检查游戏是否结束
        if game.gameover:
            if reset_flag == 0:
               end_game()
            window.after(1, update_game)
        else:
            # 继续更新游戏画面
            window.after(1, update_game)

def countdown():
    global countdown_flag,update_flag,start_time
    if countdown_flag:
        success, img1 = cap.read()
        img1 = cv2.flip(img1, 1)
        hands, img1 = detector.findHands(img1, flipType=False)
        if not hands:
            # 如果没有检测到手，显示提示信息
            text = "put your hand in the screen"
            font_scale = 2
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
            text_x = (img1.shape[1] - text_size[0]) // 2
            text_y = (img1.shape[0] + text_size[1]) // 2
            cv2.putText(img1, text, (text_x, text_y), font, font_scale, (255, 255, 255), 2)
        if hands and start_time == 0:
            start_time = time.time()
        if hands and start_time!=0:
            lmList = hands[0]['lmList']
            pointindex = lmList[8][0:2]
            if 0<= (time.time() - start_time) <=1.5:
                img1 = game.show3(img1, pointindex)
            elif  1.5< (time.time() - start_time) <=2.8:
                img1 = game.show2(img1, pointindex)
            else:
                img1 = game.show1(img1, pointindex)

        # 将OpenCV图像转换为Tkinter图像
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img1 = Image.fromarray(img1)
        img1 = ImageTk.PhotoImage(image=img1)

        # 更新画布上的图像
        canvas.img = img1
        canvas.create_image(0, 0, anchor=tk.NW, image=img1)

        if start_time == 0:
            window.after(1, countdown)
        elif start_time!=0 and (time.time() - start_time)<=4.1 :
            window.after(1, countdown)
        else:
            countdown_flag = 0
            update_flag = 1
            update_game()

def start_game():
    global canvas, start_button, reset_flag, update_flag,quit_button,countdown_flag,start_time
    musics.pagemusic.stop()
    # 移除开始按钮
    reset_flag = 0
    countdown_flag=1

    #计数标志打开
    start_time = 0

    label_wife2.place_forget()
    label_wife3.place_forget()
    start_button.place_forget()
    quit_button.place_forget()

    if restart_button!=None:
        restart_button.pack_forget()

    # 创建画布用于显示游戏画面
    canvas = tk.Canvas(window, width=1280, height=720)
    canvas.pack(side=tk.TOP)  # 设置画布位于窗口顶部

    #播放背景音乐
    musics.playbkmusic(0.6)

    #更新画布
    countdown()

def end_game():
    global restart_button, reset_flag,score_label,gameover_label,history
    reset_flag = 1

    canvas_height = canvas.winfo_height()

    # 创建最终得分标签并放置在画布下方靠左位置
    score_label = tk.Label(window, text=f"Final Score: {game.score}", font=("Arial", 18))
    score_label.place(x=470, y=canvas_height+10)

    # 创建游戏结束标签并放置在最终得分标签下方靠左位置
    gameover_label = tk.Label(window, text="Game Over", font=("Arial", 20))
    gameover_label.place(in_=score_label,relx=1,rely=0,x=45,y=-5)  # 调整垂直间距

    # 创建重新开始按钮并放置在文字右边
    restart_button = tk.Button(window, text="Restart Game", command=restart_game)
    restart_button.place(in_=score_label,relx=1, rely=1, anchor=tk.N,x=310,y=-30)
    button_font3 = ("Arial", 18)
    restart_button.configure(font=button_font3)

    musics.stopbkmusic()
    musics.playdiemusic(0.6)

    update_high_score(history_path)

    show_score(game.score)

def restart_game():
    global restart_button, game, canvas, update_flag,gameover_label,score_label,flag_random,history
    # 移除重新开始按钮
    if score_window.winfo_exists()==False:
        restart_button.place_forget()
        # 重置游戏状态
        game.reset_game()
        update_flag = 0
        flag_random=0
        update_history()

        #去除下方组件
        gameover_label.place_forget()
        score_label.place_forget()

        #重启开始界面
        show_start_screen()
    else:
        pass

#运行主页面
show_start_screen()

# 运行窗口事件循环
window.mainloop()
