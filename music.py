import pygame
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
eat_music_path=os.path.join(script_dir,"musicpackegs","eat.mp3")
page_music_path=os.path.join(script_dir,"musicpackegs","pagemusic.mp3")
bg_music_path = os.path.join(script_dir, "musicpackegs","backgroundmusic.mp3")
death_music_path = os.path.join(script_dir, "musicpackegs","niganma.mp3")
libulihai_music_path=os.path.join(script_dir,"musicpackegs","libulihai.mp3")
chang_music_path=os.path.join(script_dir,"musicpackegs","chang.mp3")
tiao_music_path=os.path.join(script_dir,"musicpackegs","tiao.mp3")
rap_music_path=os.path.join(script_dir,"musicpackegs","rap.mp3")
lanqiu_music_path=os.path.join(script_dir,"musicpackegs","lanqiu.mp3")
music_music_path=os.path.join(script_dir,"musicpackegs","music.mp3")
jntm_music_path=os.path.join(script_dir,"musicpackegs","jntm.mp3")
zhendeshiniya_music_path=os.path.join(script_dir,"musicpackegs","wazhendeshiniya.mp3")
countdown_path= os.path.join(script_dir,"musicpackegs","countdown.mp3")

guichu_path=[chang_music_path,
             tiao_music_path,
             rap_music_path,
             lanqiu_music_path,
             music_music_path,
             jntm_music_path,
             zhendeshiniya_music_path]

class music_class:
    def __init__(self, path_eat, path_bkbgm, path_diemusic,path_libulihai,path_pagemusic,
                 guichu_path,countdown_path):
        pygame.init()
        pygame.mixer.init()
        self.bkmusic = pygame.mixer.Sound(path_bkbgm)
        self.diemusic = pygame.mixer.Sound(path_diemusic)
        self.eatmusic=pygame.mixer.Sound(path_eat)
        self.libulihaimusic = pygame.mixer.Sound(path_libulihai)
        self.pagemusic=pygame.mixer.Sound(path_pagemusic)
        self.guichu=[]
        for path in guichu_path:
            sound = pygame.mixer.Sound(path)
            self.guichu.append(sound)
        self.countdown=pygame.mixer.Sound(countdown_path)

    def playbkmusic(self, volume):
        self.diemusic.set_volume(volume)  # 设置音量
        self.bkmusic.play(-1)

    def playdiemusic(self, volume):
        self.diemusic.set_volume(volume)  # 设置音量
        self.diemusic.play()

    def stopbkmusic(self):
        self.bkmusic.stop()

    def playeatmusic(self, volume):
        self.eatmusic.set_volume(volume)  # 设置音量
        self.eatmusic.play()

    def playlibulihainikunge_music(self,volume):
        self.libulihaimusic.set_volume(volume)
        self.libulihaimusic.play()

    def playpagemusic(self):
        self.pagemusic.play(-1)

#创建音频对象
musics=music_class(eat_music_path,
                   bg_music_path,
                   death_music_path,
                   libulihai_music_path,
                   page_music_path,
                   guichu_path,
                   countdown_path
                   )
