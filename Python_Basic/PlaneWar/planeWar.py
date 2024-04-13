'''
@FileName   :planeWar.py
@Description:飞机大战
@Date       :2023/02/18 10:52:09
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
import pygame as pg
import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
#游戏初始化
pg.init()

#宽
width = 500
#高
height = 600
#主画面
screen = pg.display.set_mode((width, height))
#标题设置
pg.display.set_caption("飞机大战")
#时钟
clock = pg.time.Clock()


#玩家类
class Player(pg.sprite.Sprite):
    '''
    玩家类
    '''

    #构造函数
    def __init__(self) -> None:
        #父类构造
        #super().__init__()
        pg.sprite.Sprite.__init__(self)
        #加载图片
        self.image = pg.Surface((50, 40))
        #图片颜色
        self.image.fill((0, 255, 0))
        #图片轮廓
        self.rect = self.image.get_rect()
        #设置图片位置--固定位置
        #self.rect.center = (width / 2, height / 2)
        self.rect.x = width / 2
        self.rect.y = height - 50
        self.speedX = 3
        self.speedY = 2

    #更新位置--如果会多线程，可以用多线程判断按键
    def update(self):
        #得到所有按键的结果值列表
        key_pressed = pg.key.get_pressed()
        #按下右键
        if key_pressed[pg.K_RIGHT]:
            self.rect.x += self.speedX
            if self.rect.right > width:
                self.rect.right = width
        elif key_pressed[pg.K_LEFT]:
            self.rect.x -= self.speedX
            if self.rect.left < 0:
                self.rect.left = 0
        elif key_pressed[pg.K_UP]:
            self.rect.y -= self.speedY
            if self.rect.top < 0:
                self.rect.top = 0
        elif key_pressed[pg.K_DOWN]:
            self.rect.y += self.speedY
            if self.rect.bottom > height:
                self.rect.bottom = height


#敌机类
class Rock(pg.sprite.Sprite):
    def __init__(self) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 30))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height or self.rect.left > width or self.rect.right < 0:
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

            self.speedx = random.randrange(2, 10)
            self.speedy = random.randrange(-3, 3)


#玩家对象列表--序列
all_sprites = pg.sprite.Group()
#游戏玩家对象
player = Player()
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
#添加玩家对象到序列
all_sprites.add(player)
#游戏主循环
running = True
while running:
    clock.tick(60)
    #每次循环监控是否关闭按键被按下
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    #更新玩家和敌人
    all_sprites.update()
    #更改屏幕颜色
    screen.fill((255, 255, 255))
    #显示界面
    all_sprites.draw(screen)
    #刷新界面
    pg.display.update()

#退出
pg.quit()
