import pygame
import pickle

pygame.init()

StringData = {}
CoverPicture = []

# 初始动画
for pic in range(0, 185):
    picture = pygame.image.load(f'screenshot/cover{pic}.png')
    CoverPicture.append(pygame.image.tostring(picture, 'RGB'))

# 封面
icon = pygame.image.load('icon.png')  # 图标
StringData['icon'] = pygame.image.tostring(icon, 'RGB')
cover = pygame.image.load('screen/menu.png')  # 加载menu界面
StringData['cover'] = pygame.image.tostring(cover, 'RGB')
cover_back = pygame.image.load('screenshot/cover184.png')  # menu界面背景
StringData['cover_back'] = pygame.image.tostring(cover_back, 'RGB')

# 图标（以下均为png图）
point = pygame.image.load('screen/point.png')
StringData['point'] = pygame.image.tostring(point, 'RGB')
blocks = pygame.image.load('blocks/three_blocks.png')  # 三种建筑材料选项
StringData['blocks'] = pygame.image.tostring(blocks, 'RGB')
steel = pygame.image.load('blocks/steel.png')
StringData['steel'] = pygame.image.tostring(steel, 'RGB')
wood = pygame.image.load('blocks/wood.png')
StringData['wood'] = pygame.image.tostring(wood, 'RGB')
road = pygame.image.load('blocks/road.png')
StringData['road'] = pygame.image.tostring(road, 'RGB')
begin = pygame.image.load('blocks/begin.png')
StringData['begin'] = pygame.image.tostring(begin, 'RGB')
begun = pygame.image.load('blocks/begun.png')
StringData['begun'] = pygame.image.tostring(begun, 'RGB')
tips = pygame.image.load('blocks/help.png')
StringData['tips'] = pygame.image.tostring(tips, 'RGB')
back = pygame.image.load('blocks/back.png')
StringData['back'] = pygame.image.tostring(back, 'RGB')
Exit = pygame.image.load('blocks/exit.png')
StringData['Exit'] = pygame.image.tostring(Exit, 'RGB')
Continue = pygame.image.load('blocks/continue.png')
StringData['Continue'] = pygame.image.tostring(Continue, 'RGB')
Clear = pygame.image.load('blocks/clear.png')
StringData['Clear'] = pygame.image.tostring(Clear, 'RGB')
Open = pygame.image.load('blocks/open.png')
StringData['Open'] = pygame.image.tostring(Open, 'RGB')
Save = pygame.image.load('blocks/save.png')
StringData['Save'] = pygame.image.tostring(Save, 'RGB')
home = pygame.image.load('blocks/home.png')
StringData['home'] = pygame.image.tostring(home, 'RGB')
withdraw = pygame.image.load('blocks/withdraw.png')
StringData['withdraw'] = pygame.image.tostring(withdraw, 'RGB')
Clear1 = pygame.image.load('blocks/clear1.png')
StringData['Clear1'] = pygame.image.tostring(Clear1, 'RGB')
Open1 = pygame.image.load('blocks/open1.png')
StringData['Open1'] = pygame.image.tostring(Open1, 'RGB')
Save1 = pygame.image.load('blocks/save1.png')
StringData['Save1'] = pygame.image.tostring(Save1, 'RGB')
home1 = pygame.image.load('blocks/home1.png')
StringData['home1'] = pygame.image.tostring(home1, 'RGB')
withdraw1 = pygame.image.load('blocks/withdraw1.png')
StringData['withdraw1'] = pygame.image.tostring(withdraw1, 'RGB')
cloud_png = pygame.image.load(f'screen/cloud.png')
StringData['cloud_png'] = pygame.image.tostring(cloud_png, 'RGB')
cloud1_png = pygame.image.load(f'screen/cloud1.png')
StringData['cloud1_png'] = pygame.image.tostring(cloud1_png, 'RGB')
cloud2_png = pygame.image.load(f'screen/cloud2.png')
StringData['cloud2_png'] = pygame.image.tostring(cloud2_png, 'RGB')

# 车
StringData['car_size'] = ((65, 31), (65, 31), (56,28), (56, 28), (51, 25), (51, 25), (44, 21), (44, 21)
                          , (44, 21), (39, 19), (39, 19), (39, 19))
for level in range(1, 13):
    car_png = pygame.image.load(f'screen/level{level}/car.png')
    StringData[f'car_png{level}'] = pygame.image.tostring(car_png, 'RGB')
    frame = pygame.image.load(f'screen/level{level}/frame.png')
    StringData[f'frame{level}'] = pygame.image.tostring(frame, 'RGB')
    background = pygame.image.load(f'screen/level{level}/background.png')
    StringData[f'background{level}'] = pygame.image.tostring(background, 'RGB')
    ok = pygame.image.load(f'screen/level{level}/ok.png')
    StringData[f'ok{level}'] = pygame.image.tostring(ok, 'RGB')

cover_png = pygame.image.load('screen/1.png')
StringData['cover_png'] = pygame.image.tostring(cover_png, 'RGB')

In = open('StringData.dat', 'wb')
In2 = open('CoverPicture.dat', 'wb')
pickle.dump(StringData, In)
pickle.dump(CoverPicture, In2)
In.close()
In2.close()
