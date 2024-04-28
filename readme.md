## 项目说明
项目基于开源项目魔改,原视频在youtube  
我抄的是b站的 [（强推）OpenCV超实用实战项目](https://www.bilibili.com/video/BV18B4y1c7r4/?buvid=XXFEBBFF261C64214E1B6CFEABEB215A16A68&is_story_h5=false&mid=Y4%2FXgNwV1mMdoN3Znab74g%3D%3D&p=50&plat_id=116&share_from=ugc&share_medium=android&share_plat=android&share_session_id=3a7a93b3-001a-4c59-8735-1f28f8a83e38&share_source=COPY&share_tag=s_i&timestamp=1688711757&unique_k=i6kO3Wu&up_id=46880349&vd_source=681581a43755da31769295c679d5ecad)   
目前是没有bug,但是代码已经能称得上小屎山了  

## 相对于原视频的更新:  
1. 添加前端页面，虽然很烂  
2. 加入原神元素和音效  
3. 添加坤坤音效  
4. 保留死亡时刻蛇身  
5. 添加食物多样性  
6. 添加死亡后弹窗  
7. 添加重启键  
8. 修改碰撞判断算法（这个改了我一个月）  
9. 添加历史最高记录和清空历史  
10. 添加开始时倒计时  
11. 添加连击音效  
12. 右上角添加帧率检测，添加开始时提示语/2024.1.9  

## 游戏效果演示视频：  
[元神，启动！（做了很久的opencv的贪吃蛇。。。勉强算个音游?）](https://www.bilibili.com/video/BV1UP411C7YJ/?share_source=copy_web)

  
## 使用方法：  
1. ### 下载已经打包好的exe游戏文件运行 
百度网盘地址：[opencv贪吃蛇](https://pan.baidu.com/s/1rw7uLH-ReM5BjVyY-mQTzw?pwd=1565)  
<font color="grey">___python文件打包方法我也写了一个文档:___</font>  
[使用pyinstaller打包conda虚拟环境下多文件的python程序](https://www.yuque.com/u39067637/maezfz/qqm6xavvkp00blyb?singleDoc#)
<br>
2. ### 拉取源码运行
python版本：
```
python==3.9.16
```
运行的话最好接电源，本项目吃cpu，不接电源会降频  
main是交互页面  
sg是逻辑页面  
requirements里是依赖库  
cd 到requirements.txt所在目录下执行：  
```
pip install -r requirements.txt
```
具体的依赖（虚拟环境）安装方法可参考下面的文档：  
[Windows系统中在pycharm中使用virtualenv创建虚拟环境](https://www.yuque.com/u39067637/maezfz/mq6euk08x1gybptc?singleDoc#)  
记得修改源为国内源  
最后直接运行main即可  
  
## 玩法说明： 
推荐打开声音玩（也算是个音游）  
运行main.py后，点击开始游戏，把手放在屏幕里面，就可以开始游戏了  
你的食指会被识别为蛇头，确保同时只有一只手出现在屏幕里  
尽可能吃到更多的食物，吃到东西会触发相应的音效。但是蛇头不要碰到蛇身。  

