import cvzone
import cv2
import math
import random
from music import musics
import numpy as np
import time
import threading
from shapely.geometry import LineString

class SnakeGameClass:
    def __init__(self, pathfoods,head):#构造函数
        self.points=[]#蛇的所有点
        self.lengths=[]#distance between each point
        self.currentlength=0# 蛇总长度
        self.allowedlength=600 #允许的总长度
        self.previoushead=0,0#上一时刻蛇头
        self.imghead= cv2.imread(head, cv2.IMREAD_UNCHANGED)#蛇头
        self.imgfood=[]#读取图片
        for path in pathfoods:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            self.imgfood.append(img)

        self.selected_img=None
        self.selected_index =0
        self.hfood=0
        self.wfood=0
        self.foodpoint=0,0#当前音符位置
        self.randomfoodlocation()#改变音符和位置
        self.soundlist=[0,0,0,0,0]#播放记录，集满播放鸡你太美
        self.score=0
        self.gameover=False

        #倒计时字体
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.flag1 = 0
        self.flag2 = 0
        self.flag3 = 0

    #随机角度旋转
    def random_rotate(self, image, angle_range=(-80, 80)):
        height, width = image.shape[:2]
        center_x = width / 2
        center_y = height / 2
        angle = random.uniform(angle_range[0], angle_range[1])
        rotation_matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)

        # 计算旋转后的图像大小
        cos = np.abs(rotation_matrix[0, 0])
        sin = np.abs(rotation_matrix[0, 1])
        new_width = int(height * sin + width * cos)
        new_height = int(height * cos + width * sin)

        # 调整旋转矩阵，以适应新的图像大小
        rotation_matrix[0, 2] += (new_width - width) / 2
        rotation_matrix[1, 2] += (new_height - height) / 2
        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height), flags=cv2.INTER_LINEAR)

        return rotated_image

    def randomfoodlocation(self):
        self.selected_img = random.choice(self.imgfood)#随机选择一张图片
        for i, img in enumerate(self.imgfood):
            if np.array_equal(img, self.selected_img):
                self.selected_index = i
                break
        self.selected_img= self.random_rotate(self.selected_img)#进行随机角度旋转
        self.hfood,self.wfood,_=self.selected_img.shape
        self.foodpoint=random.randint(100,1000), random.randint(100,600)

    def reset_game(self):
        self.points = []  # 蛇的所有点
        self.lengths = []  # distance between each point
        self.currentlength = 0  # 蛇总长度
        self.allowedlength = 600  # 允许的总长度
        self.previoushead = 0, 0  # 上一时刻蛇头
        self.randomfoodlocation()
        self.score = 0
        self.gameover = False
        self.flag1=0
        self.flag2=0
        self.flag3=0

#采用了最笨的方法展示倒计时
    def show1(self,imgmain,currenthead):
        px, py = self.previoushead  # previous xy坐标
        cx, cy = currenthead  # current xy坐标
        self.points.append([cx, cy])  # 为蛇添加当前点
        distance = math.hypot(cx - px, cy - py)  # 计算两个点之间距离
        self.lengths.append(distance)  # 将距离加到总长度上
        self.currentlength += distance  # 计算当前长度
        self.previoushead = cx, cy  # 更新蛇头位置

        #draw snake
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:  # 如果当前点不是第一个点
                    cv2.line(imgmain, self.points[i - 1], self.points[i], (0, 0, 255), 20)  # 画线

            cv2.circle(imgmain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

        #length reduction
        if self.currentlength>self.allowedlength:
            for i,length in enumerate(self.lengths):
                self.currentlength-=length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currentlength<self.allowedlength:
                    break

        #cvzone.putTextRect(imgmain, "1", [630, 400], scale=7, thickness=0, offset=50)
        imgmain= cv2.putText(imgmain, "1", [580, 430], self.font,8, (0,200,200), 11)
        if self.flag1==0:
            musics.countdown.play()
            self.flag1=1
        return imgmain

    def show2(self,imgmain,currenthead):
        px, py = self.previoushead  # previous xy坐标
        cx, cy = currenthead  # current xy坐标
        self.points.append([cx, cy])  # 为蛇添加当前点
        distance = math.hypot(cx - px, cy - py)  # 计算两个点之间距离
        self.lengths.append(distance)  # 将距离加到总长度上
        self.currentlength += distance  # 计算当前长度
        self.previoushead = cx, cy  # 更新蛇头位置

        # draw snake
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:  # 如果当前点不是第一个点
                    cv2.line(imgmain, self.points[i - 1], self.points[i], (0, 0, 255), 20)  # 画线

            cv2.circle(imgmain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

        # length reduction
        if self.currentlength > self.allowedlength:
            for i, length in enumerate(self.lengths):
                self.currentlength -= length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currentlength < self.allowedlength:
                    break

        #cvzone.putTextRect(imgmain, "2", [630, 400], scale=7, thickness=0, offset=50)
        imgmain = cv2.putText(imgmain, "2", [580, 430], self.font,8, (0, 200, 200), 11)
        if self.flag2==0:
            musics.countdown.play()
            self.flag2=1
        return imgmain

    def show3(self,imgmain,currenthead):
        px, py = self.previoushead  # previous xy坐标
        cx, cy = currenthead  # current xy坐标
        self.points.append([cx, cy])  # 为蛇添加当前点
        distance = math.hypot(cx - px, cy - py)  # 计算两个点之间距离
        self.lengths.append(distance)  # 将距离加到总长度上
        self.currentlength += distance  # 计算当前长度
        self.previoushead = cx, cy  # 更新蛇头位置

        # draw snake
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:  # 如果当前点不是第一个点
                    cv2.line(imgmain, self.points[i - 1], self.points[i], (0, 0, 255), 20)  # 画线

            cv2.circle(imgmain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

        # length reduction
        if self.currentlength > self.allowedlength:
            for i, length in enumerate(self.lengths):
                self.currentlength -= length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currentlength < self.allowedlength:
                    break

        #cvzone.putTextRect(imgmain, "3", [630, 400], scale=7, thickness=0, offset=50)
        imgmain = cv2.putText(imgmain, "3", [580, 430], self.font ,8, (0, 200, 200), 11)
        if self.flag3==0:
            musics.countdown.play()
            self.flag3=1
        return imgmain

    def line_segment_intersect(self,p1, p2, p3, p4):

        # calculate line segment lengths
        length1 = np.linalg.norm(p1 - p2)
        length2 = np.linalg.norm(p3 - p4)

        # check if line segments are shorter than threshold
        threshold = 40 # 根据需要调整阈值
        if length1 < threshold and length2 < threshold:
            return False

        # calculate cross products
        d1 = np.cross(p4 - p3, p1 - p3)
        d2 = np.cross(p4 - p3, p2 - p3)
        d3 = np.cross(p2 - p1, p3 - p1)
        d4 = np.cross(p2 - p1, p4 - p1)

        # check if the line segments intersect
        if (d1 * d2 < 0) and (d3 * d4 < 0):
            print(d1*d2)
            print(d3*d4)
            print(length1)
            print(length2)
            return True
        return False

    def play_jntm(self):
        time.sleep(0.3)
        musics.guichu[5].set_volume(0.7)
        musics.guichu[5].play()

    def update(self,imgmain,currenthead):
        if self.gameover==True:
            # draw snake
            head_width = self.imghead.shape[1]
            head_height = self.imghead.shape[0]
            for i, point in enumerate(self.points):
                if i != 0:  # 如果当前点不是第一个点
                    cv2.line(imgmain, self.points[i - 1], self.points[i], (0, 0, 255), 20)  # 画线
            cv2.circle(imgmain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

            x, y = self.points[-1]  # 蛇头位置坐标
            # 确定粘贴的起始和结束坐标
            start_x = x - head_width // 2
            start_y = y - head_height // 2
            imgmain = cvzone.overlayPNG(imgmain, self.imghead, (start_x,start_y))

            imgmain = cv2.putText(imgmain, "because of yuanshen", [150, 400], self.font, 3, (0, 100, 255), 5)
            imgmain=cv2.putText(imgmain, f'Your Score:{self.score}', [300, 550], self.font, 3, (166, 50, 140), 5)
            return imgmain

        else:
            px, py = self.previoushead  # previous xy坐标
            cx, cy = currenthead  # current xy坐标

            self.points.append([cx, cy])  # 为蛇添加当前点
            distance = math.hypot(cx - px, cy - py)  # 计算两个点之间距离
            self.lengths.append(distance)  # 将距离加到总长度上
            self.currentlength += distance  # 计算当前长度
            self.previoushead = cx, cy  # 更新蛇头位置

            # length reduction
            if self.currentlength > self.allowedlength:
                for i, length in enumerate(self.lengths):
                    self.currentlength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentlength < self.allowedlength:
                        break

            # check if snake eats the food
            rx, ry = self.foodpoint
            if rx - self.wfood // 2 < cx < rx + self.wfood // 2 and ry - self.hfood // 2 < cy < ry + self.hfood // 2:
                musics.guichu[self.selected_index].play()
                self.soundlist[self.selected_index]=1
                thread_randomphoto=threading.Thread(target=self.randomfoodlocation)
                thread_randomphoto.start()
                self.allowedlength += 50
                self.score += 1
                if self.score == 18:
                    musics.playlibulihainikunge_music(1)
                if self.score==38:
                    musics.guichu[6].play()
                if self.soundlist==[1,1,1,1,1]:
                    self.soundlist = [0, 0, 0, 0, 0]
                    thread = threading.Thread(target=self.play_jntm)#多线程播放音乐
                    thread.start()
                print(self.score)

            # draw snake
            head_width = self.imghead.shape[1]
            head_height = self.imghead.shape[0]
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:  # 如果当前点不是第一个点
                        cv2.line(imgmain, self.points[i - 1], self.points[i], (0, 0, 255), 20)  # 画线
                cv2.circle(imgmain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)
                x, y = self.points[-1]  # 蛇头位置坐标
                # 边界检查
                if 46 < x < imgmain.shape[1]-46 and 31 < y < imgmain.shape[0]-31:
                    # 确定粘贴的起始和结束坐标
                    start_x = x - head_width // 2
                    start_y = y - head_height // 2
                    imgmain =cvzone.overlayPNG(imgmain, self.imghead, (start_x,start_y))



            # draw food
            rx, ry = self.foodpoint  # random food x,y
            imgmain = cvzone.overlayPNG(imgmain, self.selected_img, (rx - self.wfood // 2, ry - self.hfood // 2))  # 把食物图片覆盖在蛇的背景图上
            cvzone.putTextRect(imgmain, f'Score:{self.score}', [50, 80], scale=3, thickness=3, offset=10)

            # segments = np.array(self.points)  # 转换为NumPy数组
            # # check for self-intersection
            # for i in range(len(segments) - 5):  # 修改循环范围，跳过与蛇头相邻的三个线段
            #     start = segments[i]  # 线段起点坐标
            #     end = segments[i + 1]  # 线段终点坐标
            #
            #     # 判断与其他线段是否相交
            #     for j in range(len(segments) - 4, len(segments) - 1):
            #         intersect_start = segments[j]  # 相交线段起点坐标
            #         intersect_end = segments[j + 1]  # 相交线段终点坐标
            #
            #         line1 = LineString([start, end])
            #         line2 = LineString([intersect_start, intersect_end])
            #
            #         if line1.length<15 and line2.length<15:
            #             continue
            #         if line1.length>15 and line2.length>15 and line1.intersects(line2):  # 判断是否相交
            #             print("hit")
            #             self.gameover = True
            #             break
            # 将点列表转换为NumPy数组
            snake_points1 = np.array(self.points[:-4])
            snake_points2 = np.array(self.points[-3:-1])
            # 构建平滑曲线对象
            smooth_curve1 = LineString(snake_points1)
            smooth_curve2 = LineString(snake_points2)
            # 判断曲线自身是否相交
            if smooth_curve1.intersects(smooth_curve2):  # 判断曲线是否为简单曲线（无自交）
                print("hit")
                self.gameover = True

            return imgmain