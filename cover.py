# 桥梁建造师@Pymunk-Pygame
import copy
import os
import pickle
from math import sin, cos, atan, asin, pi, fabs
from sys import exit

import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import *

pygame.init()


# 桥梁部件
class Bridge:
    def __init__(self, st, en, op, sta=0, le=0, fo=0):
        self.start = st
        self.end = en
        self.type = op
        self.state = sta
        self.length = le
        self.force = fo


file1 = open('StringData.dat', 'rb')
StringData = pickle.load(file1)
file1.close()

# 窗口与图层
screen = pygame.display.set_mode((625, 365))  # 窗口大小固定
pygame.display.set_caption('桥梁建造师')  # 程序名称
icon = pygame.image.fromstring(StringData['icon'], (32, 32), 'RGB')
pygame.display.set_icon(icon)
surface = screen.convert_alpha()  # 静态图层
surface1 = screen.convert_alpha()  # 动态图层
surface2 = screen.convert_alpha()  # 帮助窗口
surface3 = screen.convert_alpha()  # 应力显示图层

# 封面背景
cover = pygame.image.fromstring(StringData['cover'], (625, 741), 'RGB')  # 加载menu界面
cover.set_alpha(180)  # 设置menu界面透明度（以显示背景）
cover_back = pygame.image.fromstring(StringData['cover_back'], (625, 365), 'RGB')  # menu界面背景

# 图标（以下均为png图）
point = pygame.image.fromstring(StringData['point'], (12, 12), 'RGB')
point.set_colorkey((255, 255, 255))  # 将白色背景设为透明，下同
blocks = pygame.image.fromstring(StringData['blocks'], (42, 134), 'RGB')  # 三种建筑材料选项
blocks.set_colorkey((255, 255, 255))
steel = pygame.image.fromstring(StringData['steel'], (42, 42), 'RGB')
wood = pygame.image.fromstring(StringData['wood'], (42, 42), 'RGB')
road = pygame.image.fromstring(StringData['road'], (42, 42), 'RGB')
begin = pygame.image.fromstring(StringData['begin'], (42, 42), 'RGB')
begin.set_colorkey((255, 255, 255))
begun = pygame.image.fromstring(StringData['begun'], (42, 42), 'RGB')
begun.set_colorkey((255, 255, 255))
tips = pygame.image.fromstring(StringData['tips'], (42, 42), 'RGB')
tips.set_colorkey((255, 255, 255))
back = pygame.image.fromstring(StringData['back'], (42, 42), 'RGB')
back.set_colorkey((255, 255, 255))
Exit = pygame.image.fromstring(StringData['Exit'], (42, 42), 'RGB')
Exit.set_colorkey((255, 255, 255))
Continue = pygame.image.fromstring(StringData['Continue'], (42, 42), 'RGB')
Continue.set_colorkey((255, 255, 255))
Clear = pygame.image.fromstring(StringData['Clear'], (42, 42), 'RGB')
Clear.set_colorkey((255, 255, 255))
Open = pygame.image.fromstring(StringData['Open'], (42, 42), 'RGB')
Open.set_colorkey((255, 255, 255))
Save = pygame.image.fromstring(StringData['Save'], (42, 42), 'RGB')
Save.set_colorkey((255, 255, 255))
home = pygame.image.fromstring(StringData['home'], (42, 42), 'RGB')
home.set_colorkey((255, 255, 255))
withdraw = pygame.image.fromstring(StringData['withdraw'], (42, 42), 'RGB')
withdraw.set_colorkey((255, 255, 255))
Clear1 = pygame.image.fromstring(StringData['Clear1'], (42, 42), 'RGB')
Clear1.set_colorkey((255, 255, 255))
Open1 = pygame.image.fromstring(StringData['Open1'], (42, 42), 'RGB')
Open1.set_colorkey((255, 255, 255))
Save1 = pygame.image.fromstring(StringData['Save1'], (42, 42), 'RGB')
Save1.set_colorkey((255, 255, 255))
home1 = pygame.image.fromstring(StringData['home1'], (42, 42), 'RGB')
home1.set_colorkey((255, 255, 255))
withdraw1 = pygame.image.fromstring(StringData['withdraw1'], (42, 42), 'RGB')
withdraw1.set_colorkey((255, 255, 255))
cloud_png = pygame.image.fromstring(StringData['cloud_png'], (109, 64), 'RGB')
cloud_png.set_colorkey((255, 255, 255))
cloud1_png = pygame.image.fromstring(StringData['cloud1_png'], (80, 40), 'RGB')
cloud1_png.set_colorkey((255, 255, 255))
cloud2_png = pygame.image.fromstring(StringData['cloud2_png'], (82, 49), 'RGB')
cloud2_png.set_colorkey((255, 255, 255))

# 文本
myFont = pygame.font.SysFont('SimHei', 22)  # 使用Windows自带SimHei字体
myFont1 = pygame.font.SysFont('SimHei', 15)
myFont2 = pygame.font.SysFont('SimHei', 18)
myFont3 = pygame.font.SysFont('SimHei', 48)
headline = myFont.render("规则介绍", True, (0, 0, 0))
line1 = myFont2.render("游戏目标@ 搭建桥梁，让小车顺利到达对岸", True, (0, 0, 0))
line2 = myFont2.render("搭建方法@ 使用钢材/木材/道路，从标记点处开始搭建", True, (0, 0, 0))
line3 = myFont2.render("按下左键以选择起点，拖动鼠标以选择终点", True, (0, 0, 0))
line4 = myFont2.render("释放左键搭建完毕，单击右键以删除", True, (0, 0, 0))
line5 = myFont2.render("测评方法@ 测评时小车匀速前进", True, (0, 0, 0))
line6 = myFont2.render("顺利到达对岸即为成功", True, (0, 0, 0))
line7 = myFont2.render("注意事项@ 道路坡度不得大于45度", True, (0, 0, 0))
line8 = myFont2.render("同一竖直方向上不能有道路重叠", True, (0, 0, 0))
line9 = myFont2.render("材料总费用不能超过预算", True, (0, 0, 0))
win_txt = myFont.render("你成功了！", True, (0, 0, 0))
lose_txt = myFont.render("表现不太理想~", True, (0, 0, 0))
saved = myFont2.render("已保存", True, (0, 0, 0))
guan = myFont.render("关", True, (0, 0, 0))
ka = myFont.render("卡", True, (0, 0, 0))
xuan = myFont.render("选", True, (0, 0, 0))
ze = myFont.render("择", True, (0, 0, 0))

# 音效
menu_sound = pygame.mixer.Sound('music/menu.wav')
menu_sound.set_volume(0.3)
road_sound = pygame.mixer.Sound('music/road.wav')
road_sound.set_volume(0.3)
lose_sound = pygame.mixer.Sound('music/lose.wav')
lose_sound.set_volume(0.3)
win_sound = pygame.mixer.Sound('music/win.wav')
win_sound.set_volume(0.3)
broken = pygame.mixer.Sound('music/broken.wav')
broken.set_volume(0.3)

# Pymunk重力空间
space = pymunk.Space()
body = []  # 实体
joint = []  # 节点

# 帧率控制器
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        # 基础参数
        self.level = 0  # 游戏关卡
        self.option = 0  # 选项状态：0未选，1选中木材，2选中道路，3选中钢梁，4测评状态，5打开帮助页面，6成功，7失败
        self.option_cpy = 0  # 选项状态备份（游戏结束点击返回或从帮助界面返回时用以回复原操作状态）
        self.doing = 0  # 表示搭建状态，1为正在搭建（未选定），0为未开始搭建
        self.set_ok = []  # 可选点（游戏设定为仅有已着点可选定搭建，此列表用以保存已着点）
        self.bridge = []  # 桥梁部件参数（依次为起点、终点、类型、状态、长度、张力）
        self.bridge_cpy = []  # 桥梁拷贝1（开始测评师保存完整初始状态，结束测评返回后回复此状态）
        self.bridge_cpy1 = []  # 桥梁拷贝2（测评过程中与实际列表bridge各元素保持对应关系（同时同位删除），但各元素的参量为初始状态）
        self.init_test = 0  # 测试初始化（用以控制仅在开始测评时初始化一次）
        self.winning = 0  # 成功时刻（用以控制仅在胜利时刻更新一次存档数据（获胜次数、最优预算））
        self.color = [[[190, 80, 0, 100], [70, 70, 70, 100], [175, 175, 175, 100]],
                      [[190, 80, 0], [70, 70, 70], [175, 175, 175]]]  # 颜色参数
        self.color1 = [0, 50, 100, 150, 200, 250]  # 透明度参数
        self.Budget = 0  # 当前预算
        self.Cover_tag = 0  # 封面控件缓存
        self.Button_tag = 0  # 游戏控件缓存
        self.slide = 0  # 封面滑动位置坐标
        self.sliding = 0  # 鼠标拖动操作（1表示正在拖动，0表示未有相关操作）
        self.mouse_pos = 0  # 鼠标位置记录
        self.slide_cpy = 0  # 封面位置copy
        self.init_cover = 1  # cover界面初始化（用以控制仅在进入menu界面时读取一次游戏数据存档）
        self.budget_txt = []  # 读取最优预算后在此列表创建信息
        self.wins_txt = []  # 读取成功次数后在此列表创建信息
        self.require_txt = []  # 预算限制信息在此列表创建信息
        self.step_memory = []  # 操作栈，便于撤回、恢复
        self.ok = 0  # 背景图，游戏中导入作为判断条件
        # 初始可选基点
        self.four = ([[168, 210], [336, 336], [504, 210]],
                     [[168, 210], [336, 336], [504, 126]],
                     [[152, 209], [247, 342], [399, 323], [532, 171]],
                     [[152, 209], [247, 342], [399, 323], [532, 95]],
                     [[136, 204], [340, 340], [544, 272]],
                     [[136, 136], [340, 340], [544, 272]],
                     [[120, 180], [225, 330], [435, 330], [540, 180]],
                     [[120, 180], [225, 330], [435, 330], [540, 180]],
                     [[120, 255], [225, 330], [435, 330], [540, 255]],
                     [[104, 208], [182, 325], [468, 312], [572, 156]],
                     [[104, 208], [312, 312], [338, 312], [572, 156]],
                     [[104, 208], [416, 312], [442, 312], [572, 156]])
        # 基点数量
        self.four_num = [3, 3, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4]
        # 栈桥部件列表
        self.edge = ([Bridge((0, 210), (168, 210), 2, 2), Bridge((504, 210), (624, 210), 2, 2)],
                     [Bridge((0, 210), (168, 210), 2, 2), Bridge((504, 126), (624, 126), 2, 2)],
                     [Bridge((0, 209), (152, 209), 2, 2), Bridge((532, 171), (624, 171), 2, 2)],
                     [Bridge((0, 209), (152, 209), 2, 2), Bridge((532, 95), (624, 95), 2, 2)],
                     [Bridge((0, 204), (136, 204), 2, 2), Bridge((544, 272), (624, 272), 2, 2)],
                     [Bridge((0, 136), (136, 136), 2, 2), Bridge((544, 272), (624, 272), 2, 2)],
                     [Bridge((0, 180), (120, 180), 2, 2), Bridge((540, 180), (624, 180), 2, 2)],
                     [Bridge((0, 180), (120, 180), 2, 2), Bridge((540, 180), (624, 180), 2, 2)],
                     [Bridge((0, 255), (120, 255), 2, 2), Bridge((540, 255), (624, 255), 2, 2)],
                     [Bridge((0, 208), (104, 208), 2, 2), Bridge((572, 156), (624, 156), 2, 2)],
                     [Bridge((0, 208), (104, 208), 2, 2), Bridge((572, 156), (624, 156), 2, 2)],
                     [Bridge((0, 208), (104, 208), 2, 2), Bridge((572, 156), (624, 156), 2, 2)])
        # 初始车辆位置列表
        self.cars = (
            [96, 210], [96, 210], [91, 209], [91, 209], [86, 204], [86, 136], [80, 180], [80, 180], [80, 255],
            [71, 208],
            [71, 208], [71, 208])
        # 车辆尺寸列表（两轮间距）
        self.cars_wide = [35, 35, 31, 31, 28, 28, 24, 24, 24, 21, 21, 21]
        # 额定预算
        self.require = [1200, 1400, 1500, 1700, 1800, 2000, 2500, 3800, 3800, 4200, 4000, 4400]
        # 单位区块宽度
        self.width = [21, 21, 19, 19, 17, 17, 15, 15, 15, 13, 13, 13]
        # 动画参数
        self.moment = 0  # 水波振幅
        self.amp = 1  # 水波方向
        self.flow = 0  # 水流
        self.cloud = 20  # 云1起点x
        self.cloud1 = 300  # 云2起点x
        self.cloud2 = 500  # 云3起点x
        self.car = [0, 0]  # 车辆位置坐标
        self.angle = 0  # 车倾斜角度
        self.running = 0  # 表示车辆是否为行进状态，1为行进，0为静止
        self.speed_gap = 0  # 表示车辆行进间隔（用以控制车速）
        self.fall = 0  # 表示车辆下落，1为正在下落，0为正常行驶
        self.drop = 0  # 表示车辆下落速度
        self.angle0 = 0  # 表示车辆抛出角
        self.angle_self = []  # 表示桥梁角度

    def car_angle(self):
        """
        此函数用以计算行进过程中车辆的角度与位置，模拟车辆沿路面前进
        通过几何关系确定车辆在通过两块路面的交界处时的位置、角度
        """
        for one in self.bridge:
            if one.type == 2 and (
                    one.start[0] <= self.car[0] <= one.end[0] or one.end[0] <= self.car[0] <= one.start[0]):
                xielv1 = (one.end[1] - one.start[1]) / (one.end[0] - one.start[0])
                yuxian1 = float(1 + xielv1 ** 2) ** 0.5
                jieju1 = one.start[1] - xielv1 * one.start[0]

                if fabs(self.car[1] - (xielv1 * self.car[0] + jieju1)) > 8:
                    break

                self.car[0] += self.running / yuxian1 * self.cars_wide[self.level - 1] / 21  # 模拟前进
                self.car[1] = xielv1 * self.car[0] + jieju1

                if one.start[0] < one.end[0]:
                    low = one.start[0]
                else:
                    low = one.end[0]

                a1 = atan(xielv1)
                self.angle = -a1
                x_dis = (self.car[0] - low) * yuxian1

                if x_dis >= self.cars_wide[self.level - 1]:
                    break
                else:
                    xielv2 = 0
                    for one1 in self.bridge:
                        if one1.type == 2 and (
                                one1.start[0] <= self.car[0] - self.cars_wide[self.level - 1] * cos(self.angle) <
                                one1.end[0]
                                or one1.end[0] <= self.car[0] - self.cars_wide[self.level - 1] * cos(self.angle) <
                                one1.start[0]):
                            xielv2 = (one1.end[1] - one1.start[1]) / (one1.end[0] - one1.start[0])
                            jieju2 = one1.start[1] - xielv2 * one1.start[0]

                            if xielv1 == xielv2:
                                break

                            cross = (jieju1 - jieju2) / (xielv2 - xielv1)
                            x_dis = (self.car[0] - cross) * yuxian1
                            break

                    a2 = atan(xielv2)
                    nu = x_dis / self.cars_wide[self.level - 1] * sin(a2 - a1)

                    if fabs(nu) > 1:
                        break

                    self.angle = asin(nu) - a2  # 角度计算结果
                break

    def build(self):
        """
        开始测评时在重力空间创建桥梁实体
        桥梁由可伸缩joint模拟，由于pymunk的joint无质量参数，改由节点模拟重力
        基点处设置为静态实体
        """
        body.clear()
        joint.clear()
        self.angle_self.clear()
        space.__init__()
        space.gravity = (0, 400)
        space.damping = 0.5

        # 固定点
        for one in self.four[self.level - 1]:
            joint.append(pymunk.Body(body_type=pymunk.Body.STATIC))
            joint[-1].position = one

        # 节点
        for one in self.set_ok:
            joint.append(pymunk.Body(1, 5000))
            joint[-1].position = one

        # 桥梁
        for one in self.bridge:
            if one == self.bridge[-2]:
                break

            one_bl = []
            for one_j in joint:
                if [one_j.position.x, one_j.position.y] == one.start or [one_j.position.x, one_j.position.y] == one.end:
                    one_bl.append(one_j)

            distance = (one_bl[0].position.x - one_bl[1].position.x) ** 2
            distance += (one_bl[0].position.y - one_bl[1].position.y) ** 2
            distance **= 0.5

            if one.type == 1 or one.type == 2:
                young = 4000
            else:
                young = 8000

            body.append(pymunk.DampedSpring(one_bl[0], one_bl[1], (0, 0), (0, 0), distance, young, 10))

        for one in joint:
            space.add(one)
        for one in body:
            space.add(one)

    def update(self):
        """
        此函数更新重力空间中的实体状态，将实时参数传入bridge列表
        通过joint组件的伸缩比例模拟计算应力并存入bridge列表，当应力达到最大限度时删除桥梁部件
        """
        space.step(0.002)
        for number in range(0, 201):
            if self.bridge[number] == self.bridge[-2]:
                break

            self.bridge[number].start = body[number].a.position
            self.bridge[number].end = body[number].b.position

        for number in range(0, 201):
            if self.bridge[number] == self.bridge[-2]:
                break

            ori_b = (self.bridge_cpy1[number].start[0] - self.bridge_cpy1[number].end[0]) ** 2
            ori_b += (self.bridge_cpy1[number].start[1] - self.bridge_cpy1[number].end[1]) ** 2
            new_b = (self.bridge[number].start[0] - self.bridge[number].end[0]) ** 2
            new_b += (self.bridge[number].start[1] - self.bridge[number].end[1]) ** 2
            force = fabs(ori_b - new_b) / ori_b * 215

            if force >= 8:
                space.remove(body[number])
                self.bridge.pop(number)
                self.bridge_cpy1.pop(number)
                body.pop(number)
                broken.play()
                break

            self.bridge[number].force = int(force * 30)

        for one in joint:
            four_joint = []
            for i in range(0, self.four_num[self.level - 1]):
                four_joint.append(joint[i])

            if one in four_joint:
                continue

            if fabs(one.position.x - self.car[0]) <= 30 and fabs(one.position.y - self.car[1]) <= 20:
                one.mass = 5
            elif one.mass > 1:
                one.mass = 1

    def save(self):  # 保存游戏数据（bridge、set_ok）
        with open(f'level/level{self.level}/bridges.dat', 'w') as br:
            br.seek(0)
            br.truncate()

            for one in self.bridge:
                br.write(
                    f' {one.start[0]} {one.start[1]} {one.end[0]} {one.end[1]} {one.type} {one.state} {one.length} {one.force}\n')

        with open(f'level/level{self.level}/oks.dat', 'w') as ok_s:
            for one in self.set_ok:
                ok_s.write(f' {one[0]} {one[1]}\n')

    def open(self):  # 读取游戏数据（bridge、set_ok）
        with open(f'level/level{self.level}/oks.dat', 'r+') as oks:  # 打开
            self.bridge.clear()
            self.set_ok.clear()
            oks_l = oks.readlines()

            tmp_ok = []
            for one in oks_l:
                tmp_ok.append([])
                for le in one:
                    if le == ' ':
                        tmp_ok[-1].append([])
                        continue
                    if le == '\n':
                        break
                    tmp_ok[-1][-1].append(le)

            for one in tmp_ok:
                self.set_ok.append([int(''.join(one[0])), int(''.join(one[1]))])

        with open(f'level/level{self.level}/bridges.dat', 'r+') as bri:
            bridges = bri.readlines()

            tmp_bri = []
            for one in bridges:
                tmp_bri.append([])
                for le in one:
                    if le == ' ':
                        tmp_bri[-1].append([])
                        continue
                    if le == '\n':
                        break
                    tmp_bri[-1][-1].append(le)

            for one in tmp_bri:
                self.bridge.append(
                    Bridge([int(''.join(one[0])), int(''.join(one[1]))], [int(''.join(one[2])), int(''.join(one[3]))],
                           int(''.join(one[4])), int(''.join(one[5])), int(''.join(one[6])), int(''.join(one[7]))))

    def choose(self, pos_x, pos_y):
        """
        此函数用以判断新创建的部件是否合法，不合法的部件将bridge列表元素的第4参数标记为-2，在后续程序中将被删除
        :param pos_x: 鼠标位置横坐标
        :param pos_y: 鼠标位置纵坐标
        """
        maximum = 0
        if self.option == 3:
            maximum += 42 * (self.width[self.level - 1] ** 2)
        else:
            maximum += 22 * (self.width[self.level - 1] ** 2)

        x_1 = self.bridge[-1].start[0]
        y_1 = self.bridge[-1].start[1]

        if x_1 > pos_x:
            high_x = x_1
            low_x = pos_x
        else:
            high_x = pos_x
            low_x = x_1
        if y_1 > pos_y:
            high_y = y_1
            low_y = pos_y
        else:
            high_y = pos_y
            low_y = y_1

        if (pos_y - y_1) ** 2 + (pos_x - x_1) ** 2 < maximum:
            self.bridge[-1].state = 0
            self.bridge[-1].end = [pos_x, pos_y]  # 添加终点

            for one in self.bridge:  # 淘汰不合要求的模块
                if one != self.bridge[-1] and \
                        (one.start == self.bridge[-1].start and one.end == self.bridge[-1].end) or \
                        (one.start == self.bridge[-1].end and one.end == self.bridge[-1].start):
                    self.bridge[-1].state = -2
                    break
                if one.type == 2 and self.bridge[-1].type == 2 and (
                        one.start[0] < self.bridge[-1].end[0] < one.end[0]
                        or one.end[0] < self.bridge[-1].end[0] < one.start[0]):
                    self.bridge[-1].state = -2
                    break
                if one.state == 2 and self.bridge[-1].state == 2 and (
                        self.bridge[-1].start[0] < one.start[0] < self.bridge[-1].end[0]
                        or self.bridge[-1].end[0] < one.start[0] < self.bridge[-1].start[0]
                        or self.bridge[-1].start[0] < one.end[0] < self.bridge[-1].end[0]
                        or self.bridge[-1].end[0] < one.end[0] < self.bridge[-1].start[0]):
                    self.bridge[-1].state = -2
                    break
                if one != self.bridge[-1] and one.type == 2 and self.bridge[-1].type == 2 and (
                        (one.start[0] == self.bridge[-1].start[0] and one.end[0] == self.bridge[-1].end[0])
                        or (one.start[0] == self.bridge[-1].end[0] and one.end[0] == self.bridge[-1].start[0])):
                    self.bridge[-1].state = -2
                    break
            if self.bridge[-1].type == 2 and (self.bridge[-1].start[0] == self.bridge[-1].end[0] or fabs(
                    (self.bridge[-1].end[1] - self.bridge[-1].start[1]) / (
                            self.bridge[-1].end[0] - self.bridge[-1].start[0])) >= 1):
                self.bridge[-1].state = -2
            if self.bridge[-1].end[0] < self.four[self.level - 1][0][0] or self.bridge[-1].end[0] > \
                    self.four[self.level - 1][-1][0]:
                self.bridge[-1].state = -2
            if self.bridge[-1].start[0] == self.bridge[-1].end[0] and \
                    self.bridge[-1].start[1] == self.bridge[-1].end[1]:
                self.bridge[-1].state = -2

            if x_1 != pos_x:
                k1 = (y_1 - pos_y) / (x_1 - pos_x)
                b1 = (x_1 * pos_y - pos_x * y_1) / (x_1 - pos_x)

                for i in range(low_x, high_x):
                    j = int((k1 * i + b1) // 1)
                    r, s, t, u = self.ok.get_at((i, j))
                    if r < 255 or s < 255 or t < 255:
                        self.bridge[-1].state = -2
                        break

            if y_1 != pos_y:
                k2 = (x_1 - pos_x) / (y_1 - pos_y)
                b2 = (y_1 * pos_x - pos_y * x_1) / (y_1 - pos_y)

                for i in range(low_y, high_y):
                    j = int((k2 * i + b2) // 1)
                    r, s, t, u = self.ok.get_at((j, i))
                    if r < 255 or s < 255 or t < 255:
                        self.bridge[-1].state = -2
                        break

            length = float((x_1 - pos_x) ** 2 + (y_1 - pos_y) ** 2) ** 0.5 // 1
            self.bridge[-1].length = int(length * 13 / self.width[self.level - 1])

    def remove(self, x, y):  # 删除桥梁部件
        for one in self.bridge:
            x1 = one.start[0]
            y1 = one.start[1]
            x2 = one.end[0]
            y2 = one.end[1]
            x_half = (x1 + x2) / 2
            y_half = (y1 + y2) / 2

            radius = (x - x_half) ** 2 + (y - y_half) ** 2
            distance = (x1 - x) * (y2 - y) - (x2 - x) * (y1 - y)
            length = (x1 - x2) ** 2 + (y1 - y2) ** 2

            if length > 0 and distance ** 2 / length < 30 and radius < length / 8:
                if one.start in self.set_ok:
                    self.set_ok.remove(one.start)
                if one.end in self.set_ok:
                    self.set_ok.remove(one.end)

                self.step_memory.append([one, -1])
                self.bridge.remove(one)  # 删除桥梁部件

                for one1 in self.bridge:
                    if one1.start not in self.four[self.level - 1] and one1.start not in self.set_ok:
                        self.set_ok.append(one1.start)
                    if one1.end not in self.four[self.level - 1] and one1.end not in self.set_ok:
                        self.set_ok.append(one1.end)  # 恢复误删可选点
                break

    def withdraw_onestep(self):
        if self.step_memory[-1][1] == 1:
            if self.step_memory[-1][0].start in self.set_ok:
                self.set_ok.remove(self.step_memory[-1][0].start)
            if self.step_memory[-1][0].end in self.set_ok:
                self.set_ok.remove(self.step_memory[-1][0].end)
            for one in self.bridge:
                if one.start == self.step_memory[-1][0].start and one.end == self.step_memory[-1][0].end:
                    self.bridge.remove(one)
            for one1 in self.bridge:
                if one1.start not in self.four[self.level - 1] and one1.start not in self.set_ok:
                    self.set_ok.append(one1.start)
                if one1.end not in self.four[self.level - 1] and one1.end not in self.set_ok:
                    self.set_ok.append(one1.end)  # 恢复误删可选点

        elif self.step_memory[-1][1] == -1:
            self.bridge.append(self.step_memory[-1][0])
            if self.bridge[-1].start not in self.set_ok and self.bridge[-1].start not in self.four[self.level - 1]:
                self.set_ok.append(self.bridge[-1].start)
            if self.bridge[-1].end not in self.set_ok and self.bridge[-1].end not in self.four[self.level - 1]:
                self.set_ok.append(self.bridge[-1].end)

        else:
            if self.step_memory[-1][1] == 2:
                self.bridge.clear()
                self.set_ok.clear()
            for one in self.step_memory[-1][0]:
                self.bridge.append(one)
                if one.start not in self.set_ok and one.start not in self.four[self.level - 1]:
                    self.set_ok.append(one.start)
                if one.end not in self.set_ok and one.start not in self.four[self.level - 1]:
                    self.set_ok.append(one.end)

        self.step_memory.pop(-1)

    def data_update(self):  # 更新游戏纪录
        with open(f'level/level{self.level}/data.dat', 'r+') as data_t:
            data_b = data_t.readlines()
            best_b = int(data_b[1])

            if self.Budget < best_b:
                best_b = self.Budget

            data_t.seek(0)
            data_t.truncate()
            data_t.write(f"{int(data_b[0]) + 1}\n{best_b}")

    def show_car(self, mul, car_png):
        if self.option == 4:
            fall = 1
            for block in self.bridge:
                if block.type == 2 and (block.start[0] <= self.car[0] <= block.end[0]
                                        or block.end[0] <= self.car[0] <= block.start[0]):
                    xielv = (block.end[1] - block.start[1]) / (block.end[0] - block.start[0])
                    jieju = block.start[1] - xielv * block.start[0]

                    if fabs(self.car[1] - (xielv * self.car[0] + jieju)) <= 3:
                        fall = 0  # 如果落在道路上则停止下落
                        self.angle0 = self.angle
                        self.drop = 0.4 * sin(self.angle)
                        break
            # 模拟车辆下落
            if fall == 1:
                self.angle -= 0.001
                self.car[0] += 0.3 * cos(self.angle0) * mul
                self.car[1] -= self.drop
                if self.car[1] < 300:
                    self.drop -= 0.002
                else:
                    self.drop += 0.005
            else:
                self.speed_gap = (self.speed_gap + 1) % 4
                if self.speed_gap == 0:
                    self.car_angle()  # 车辆倾斜度算法
        if self.car[0] > 610:
            self.car[0] = 610
        if self.car[0] < 31:
            self.car[0] = 31
        if self.car[0] == 610 and self.car[1] <= self.four[self.level - 1][self.four_num[self.level - 1] - 1][1]:
            self.option = 6
            if self.winning == 1:
                self.data_update()  # 更新数据
            self.winning = 0
        if -0.05 < self.drop and self.car[1] >= 290:
            if self.option != 7:
                self.bridge.remove(self.edge[self.level - 1][0])
                self.bridge.remove(self.edge[self.level - 1][1])
            self.option = 7
        if self.angle >= 0:
            car_pos = [self.car[0] - 19 * sin(self.angle) * mul - 31 * cos(self.angle) * mul,
                       self.car[1] - 8 * sin(self.angle) * mul - 19 * cos(self.angle) * mul]
        else:
            car_pos = [self.car[0] - 31 * cos(self.angle) * mul,
                       self.car[1] + 31 * sin(self.angle) * mul - 19 * cos(self.angle) * mul]
        car_png1 = pygame.transform.rotate(car_png, 180 / pi * self.angle)
        car_png1.set_colorkey((255, 255, 255))
        surface.blit(car_png1, car_pos)

    def show_bridge(self, mul):
        if self.bridge:
            if self.option == 4 and self.init_test == 1:
                self.build()  # 创建物理桥梁
                self.init_test = 0
            if self.option == 4 and self.init_test == 0:
                self.update()  # 更新桥梁状态
            # 显示桥梁
            thickness = [3, 4, 3]
            for block in self.bridge:
                if self.option != 4 and (block.state == 0 or block.state == 1):
                    pygame.draw.line(surface, self.color[block.state][block.type - 1],
                                     block.start, block.end, int(mul * thickness[block.type - 1]))
                elif block.state == -2:
                    pygame.draw.line(surface, (240, 75, 80), block.start,
                                     block.end, int(mul * thickness[block.type - 1]))
                elif self.option == 4 and block != self.bridge[-1] and block != self.bridge[-2]:
                    pygame.draw.line(surface, self.color[block.state][block.type - 1],
                                     block.start, block.end, int(mul * thickness[block.type - 1]))
            if self.option == 4:
                # 在单独图层上绘制
                surface3.fill((255, 255, 255, 0))
                for block in self.bridge:
                    if block != self.bridge[-1] and block != self.bridge[-2]:
                        pygame.draw.line(surface3, [60, 60, 200, block.force],
                                         [block.start[0], block.start[1] + 4 * mul],
                                         [block.end[0], block.end[1] + 4 * mul], 3)

    def show_icon(self):
        if self.option not in (6, 7):
            surface1.blit(Clear, (563, 201))
            surface1.blit(blocks, (20, 31))
            surface1.blit(Open, (563, 251))
            surface1.blit(Save, (563, 301))
            surface1.blit(home, (563, 31))
            surface1.blit(withdraw, (513, 31))
        if self.Button_tag == 1:
            surface1.blit(Clear1, (563, 201))
        elif self.Button_tag == 2:
            surface1.blit(Open1, (563, 251))
        elif self.Button_tag == 3:
            surface1.blit(Save1, (563, 301))
        elif self.Button_tag == 4:
            surface1.blit(home1, (563, 31))
        elif self.Button_tag == 5:
            surface1.blit(withdraw1, (513, 31))
        if self.option not in (4, 6, 7):
            surface1.blit(begin, (20, 301))
        if self.option not in (5, 6, 7):
            surface1.blit(tips, (20, 251))
        if self.option == 3:
            surface1.blit(steel, (20, 31))
        elif self.option == 1:
            surface1.blit(wood, (20, 77))
        elif self.option == 2:
            surface1.blit(road, (20, 123))
        elif self.option == 4:
            surface1.blit(begun, (20, 301))
        elif self.option == 5:
            surface2.blit(back, (20, 251))
        elif self.option in (6, 7):
            surface2.blit(Continue, (20, 301))
            surface2.blit(Exit, (563, 301))

    def show_data(self):
        if self.option not in (6, 7):
            level_tag = myFont3.render(f'{self.level}', True, (0, 0, 0))
            if self.level < 10:
                surface.blit(level_tag, (90, 15))
            else:
                surface.blit(level_tag, (70, 15))

            self.Budget = 0
            if self.option != 4:
                for budgets in self.bridge:
                    self.Budget += budgets.length * budgets.type
            else:
                for budgets in self.bridge_cpy:
                    self.Budget += budgets.length * budgets.type

            if self.Budget <= self.require[self.level - 1]:
                self.Budget_text = myFont.render(f"{int(self.Budget)}/{self.require[self.level - 1]}", True, (0, 0, 0))
            else:
                self.Budget_text = myFont.render(f"{int(self.Budget)}!/{self.require[self.level - 1]}", True,
                                                 (240, 75, 80))

            surface.blit(self.Budget_text, (120, 10))

            with open(f'level/level{self.level}/data.dat', 'r') as numbers:
                data = numbers.readlines()
                datum1_text = myFont1.render(f"已成功{int(data[0])}次", True, (0, 0, 0))
                surface1.blit(datum1_text, (120, 35))
                if int(data[1]) <= self.require[self.level - 1]:
                    datum2_text = myFont1.render(f"最优预算{int(data[1])}", True, (0, 0, 0))
                    surface1.blit(datum2_text, (120, 55))

    def environment(self, gap):
        # 流动的水
        if (self.option in (0, 1, 2, 3) and gap % 20 == 0) or (self.option == 4 and gap % 24 == 0):
            self.moment += self.amp
            self.flow = (self.flow + 0.1) % 2
        if self.moment >= 4:
            self.amp = -1
        if self.moment <= -4:
            self.amp = 1
        for i in range(1, 625):
            pygame.draw.line(surface1, (0, 150, 220, 80), (i, 365),
                             (i, 289 - self.moment * sin(pi / 20 * i + self.flow * pi)), 1)

        # 飘动的云
        if (self.option in (0, 1, 2, 3) and gap % 20 == 0) or (self.option == 4 and gap % 24 == 0):
            self.cloud += 1
            self.cloud1 += 1
            self.cloud2 += 1
        if self.cloud >= 625:
            self.cloud = -120
        if self.cloud1 >= 625:
            self.cloud1 = -120
        if self.cloud2 >= 625:
            self.cloud2 = -120
        surface1.blit(cloud_png, (self.cloud, 100))
        surface1.blit(cloud1_png, (self.cloud1, 180))
        surface1.blit(cloud2_png, (self.cloud2, 50))

    def init_point(self):
        if self.option in (0, 1, 2, 3):
            need_to_reveal = []
            for i in range(0, self.four_num[self.level - 1]):
                need_to_reveal.append([1, i])
            for part in self.bridge:
                for i in range(0, self.four_num[self.level - 1]):
                    if (self.four[self.level - 1][i] == part.start or self.four[self.level - 1][i] == part.end) and \
                            part.state == 1:
                        need_to_reveal[i][0] = 0
            for one in need_to_reveal:
                if one[0] == 1:
                    point_p = [self.four[self.level - 1][one[1]][0] - 5, self.four[self.level - 1][one[1]][1] - 5]
                    surface.blit(point, point_p)


def del_files(path):
    ls = os.listdir(path)
    for i in ls:
        iPath = os.path.join(path, i)
        os.remove(iPath)


def main():
    bri = Game()
    # 主循环
    gap = 0  # 模拟帧率（主程序采用自定义帧率）
    menu_sound_init = 0
    save_init = 0
    screenshot = 0
    while True:
        surface.fill((255, 255, 255, 0))

        # 事件轮询
        for event in pygame.event.get():
            # 退出
            if event.type == QUIT:
                exit()
            # 鼠标左键按下（选项/选择搭建起点）
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and bri.level:
                x, y = event.pos

                if 21 <= x <= 62:
                    if 31 <= y <= 72 and bri.option in (0, 1, 2, 3):  # 钢梁
                        if bri.option == 3:
                            bri.option = 0
                        else:
                            bri.option = 3

                    elif 77 <= y <= 118 and bri.option in (0, 1, 2, 3):  # 木材
                        if bri.option == 1:
                            bri.option = 0
                        else:
                            bri.option = 1

                    elif 123 <= y <= 164 and bri.option in (0, 1, 2, 3):  # 道路
                        if bri.option == 2:
                            bri.option = 0
                        else:
                            bri.option = 2

                    elif (x - 39.5) ** 2 + (y - 321.5) ** 2 <= 441:
                        if bri.option == 4:
                            bri.option = bri.option_cpy  # 终止测评
                            bri.car[0] = bri.cars[bri.level - 1][0]
                            bri.car[1] = bri.cars[bri.level - 1][1]
                            bri.angle = 0
                            bri.running = 0
                            bri.bridge = bri.bridge_cpy

                        elif bri.option in (0, 1, 2, 3) and bri.Budget <= bri.require[bri.level - 1]:
                            bri.option_cpy = bri.option
                            bri.option = 4  # 开始测评
                            bri.init_test = 1
                            bri.winning = 1
                            bri.running = 1
                            bri.bridge_cpy = copy.deepcopy(bri.bridge)
                            bri.bridge_cpy1 = copy.deepcopy(bri.bridge)
                            bri.bridge.append(bri.edge[bri.level - 1][0])
                            bri.bridge.append(bri.edge[bri.level - 1][1])
                            del_files('./screenshot')
                            screenshot = 0

                        elif bri.option in (6, 7):  # 返回
                            bri.option = bri.option_cpy
                            bri.car[0] = bri.cars[bri.level - 1][0]
                            bri.car[1] = bri.cars[bri.level - 1][1]
                            bri.angle = 0
                            bri.running = 0
                            menu_sound_init = 0
                            bri.bridge = bri.bridge_cpy

                    elif (x - 39.5) ** 2 + (y - 271.5) ** 2 <= 441 and bri.option in (0, 1, 2, 3, 5):
                        if bri.option == 5:
                            bri.option = bri.option_cpy  # 关闭帮助页面
                        else:
                            bri.option_cpy = bri.option
                            bri.option = 5  # 打开帮助页面

                if (x - 583.5) ** 2 + (y - 321.5) ** 2 <= 441 and bri.option in (6, 7):
                    bri.level = 0
                    bri.option = 0
                    bri.angle = 0
                    bri.Cover_tag = 0
                    bri.bridge.clear()
                    bri.set_ok.clear()

                if bri.option in (1, 2, 3) and bri.doing == 0:
                    chu = bri.width[bri.level - 1]
                    xx = (x + chu // 2) // chu + 1
                    yy = (y + chu // 2) // chu + 1
                    x = xx * chu - chu
                    y = yy * chu - chu
                    if [x, y] in bri.set_ok or [x, y] in bri.four[bri.level - 1]:
                        bri.bridge.append(Bridge([x, y], [x, y], bri.option))  # 保存起点
                        bri.doing = 1

            # 鼠标左键移动
            elif event.type == MOUSEMOTION and bri.option in (0, 1, 2, 3):
                x, y = event.pos

                if bri.level != 0:
                    if bri.doing != 1:
                        if (x - 583.5) ** 2 + (y - 221.5) ** 2 <= 441:
                            bri.Button_tag = 1
                        elif (x - 583.5) ** 2 + (y - 271.5) ** 2 <= 441:
                            bri.Button_tag = 2
                        elif (x - 583.5) ** 2 + (y - 321.5) ** 2 <= 441:
                            bri.Button_tag = 3
                        elif (x - 583.5) ** 2 + (y - 51.5) ** 2 <= 441:
                            bri.Button_tag = 4
                        elif (x - 533.5) ** 2 + (y - 51.5) ** 2 <= 441:
                            bri.Button_tag = 5
                        else:
                            bri.Button_tag = 0
                            menu_sound_init = 0
                        if bri.Button_tag != 0 and menu_sound_init == 0:
                            menu_sound.play()
                            menu_sound_init = 1

                    if bri.doing == 1:
                        chu = bri.width[bri.level - 1]
                        xx = (x + chu // 2) // chu + 1
                        yy = (y + chu // 2) // chu + 1
                        x = xx * chu - chu
                        y = yy * chu - chu
                        bri.choose(x, y)

                else:
                    tmp_x = x // 52 + 1
                    tmp_y = (y + bri.slide) // 52 + 2
                    if tmp_x % 3 > 1 or tmp_y % 3 > 1 or tmp_x < 3 or tmp_y < 3 or tmp_x > 10 or tmp_y > 13:
                        bri.Cover_tag = 0
                        menu_sound_init = 0
                    else:
                        bri.Cover_tag = tmp_x // 3 + tmp_y // 3 * 3 - 3
                        if menu_sound_init == 0:
                            menu_sound.play()
                            menu_sound_init = 1
                    if bri.sliding == 1:  # 位置移动
                        bri.slide = int((y - bri.mouse_pos) * 100 / 67 + bri.slide_cpy)
                        if bri.slide < 0:
                            bri.slide = 0
                        if bri.slide > 320:
                            bri.slide = 320

            # 鼠标左键释放
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                x, y = event.pos
                bri.sliding = 0

                if bri.level != 0:
                    if bri.option in (0, 1, 2, 3) and bri.bridge and bri.doing == 1:
                        bri.bridge[-1].state += 1
                        bri.doing = 0
                        if bri.bridge[-1].state == 1:
                            road_sound.play()

                        if bri.bridge[-1].state == -1 or bri.bridge[-1].start == bri.bridge[-1].end:
                            bri.bridge.pop(-1)
                        else:
                            bri.step_memory.append([copy.deepcopy(bri.bridge[-1]), 1])

                        if bri.bridge and bri.bridge[-1].state == 1 and bri.bridge[-1].end not in bri.set_ok \
                                and bri.bridge[-1].end not in bri.four[bri.level - 1]:
                            bri.set_ok.append(bri.bridge[-1].end)

                    if bri.bridge and bri.Button_tag == 1 and (x - 583.5) ** 2 + (y - 221.5) ** 2 <= 441:
                        bri.step_memory.append([[], -2])
                        for one in bri.bridge:
                            bri.step_memory[-1][0].append(copy.deepcopy(one))
                        bri.bridge.clear()
                        bri.set_ok.clear()
                    if bri.Button_tag == 2 and (x - 583.5) ** 2 + (y - 271.5) ** 2 <= 441:
                        bri.step_memory.append([[], 2])
                        for one in bri.bridge:
                            bri.step_memory[-1][0].append(copy.deepcopy(one))
                        bri.open()
                    if bri.Button_tag == 3 and (x - 583.5) ** 2 + (y - 321.5) ** 2 <= 441:
                        bri.save()
                        if save_init == 0:
                            save_init = 1
                    if bri.Button_tag == 4 and (x - 583.5) ** 2 + (y - 51.5) ** 2 <= 441:
                        bri.level = 0
                        bri.init_cover = 1
                        bri.Cover_tag = 0
                        bri.option = 0
                        bri.bridge.clear()
                        bri.set_ok.clear()
                        bri.step_memory.clear()
                    if bri.Button_tag == 5 and (x - 533.5) ** 2 + (y - 51.5) ** 2 <= 441 and bri.step_memory:
                        bri.withdraw_onestep()

                else:
                    tmp_x = x // 52 + 1
                    tmp_y = (y + bri.slide) // 52 + 2
                    if tmp_x % 3 > 1 or tmp_y % 3 > 1 or tmp_x < 3 or tmp_y < 3 or tmp_x > 10 or tmp_y > 13:
                        continue
                    else:
                        bri.level = tmp_x // 3 + tmp_y // 3 * 3 - 3

                    if bri.level != 0:
                        # 车
                        bri.car[0] = bri.cars[bri.level - 1][0]
                        bri.car[1] = bri.cars[bri.level - 1][1]
                        car_png = pygame.image.fromstring(StringData[f'car_png{bri.level}'],
                                                          StringData[f'car_size'][bri.level - 1], 'RGB')

                        # 游戏控件
                        bri.Button_tag = 0
                        frame = pygame.image.fromstring(StringData[f'frame{bri.level}'], (625, 365), 'RGB')
                        frame.set_colorkey((255, 255, 255))
                        frame.set_alpha(120)
                        background = pygame.image.fromstring(StringData[f'background{bri.level}'], (625, 365), 'RGB')
                        background.set_colorkey((255, 255, 255))
                        bri.ok = pygame.image.fromstring(StringData[f'ok{bri.level}'], (625, 365), 'RGB')
                        mul = bri.cars_wide[bri.level - 1] / 21

            # 鼠标右键释放
            elif event.type == MOUSEBUTTONUP and bri.level != 0 and event.button == 3 and bri.option in (
                    0, 1, 2, 3) and bri.bridge:
                x, y = event.pos
                bri.remove(x, y)

            # 鼠标滚轮滑动
            elif event.type == MOUSEBUTTONDOWN and event.button == 5 and bri.level == 0:
                if bri.slide <= 300:
                    bri.slide += 20
            elif event.type == MOUSEBUTTONDOWN and event.button == 4 and bri.level == 0:
                if bri.slide >= 20:
                    bri.slide -= 20

            # 鼠标点击位置条
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and bri.level == 0:
                x, y = event.pos

                if 604 <= x <= 624 and bri.slide * 0.67 <= y <= bri.slide * 0.67 + 150:
                    bri.sliding = 1
                    bri.mouse_pos = y
                    bri.slide_cpy = bri.slide

        # 封面控件
        if bri.level == 0:
            if bri.init_cover == 1:
                bri.init_cover = 0
                for i in range(1, 13):
                    with open(f'level/level{i}/data.dat', 'r+') as data_txt:
                        data = data_txt.readlines()
                        bri.budget_txt.append(myFont1.render(f"已成功{int(data[0])}次", True, (0, 0, 0)))
                        bri.budget_txt[-1].set_alpha(100)
                        bri.wins_txt.append(myFont1.render(f"最优预算{int(data[1])}", True, (0, 0, 0)))
                        bri.wins_txt[-1].set_alpha(100)

                    bri.require_txt.append(myFont1.render(f"额定预算{bri.require[i - 1]}", True, (0, 0, 0)))
                    bri.require_txt[-1].set_alpha(100)

            surface2.fill((255, 255, 255, 0))

            # 显示标题
            surface2.blit(guan, (40, 70))
            surface2.blit(ka, (40, 120))
            surface2.blit(xuan, (40, 170))
            surface2.blit(ze, (40, 220))

            surface.fill((255, 255, 255, 0))
            surface.blit(cover, (0, -bri.slide))

            screen.blit(cover_back, (0, 0))
            screen.blit(surface, (0, 0))

            if bri.Cover_tag != 0 and bri.sliding == 0:
                i = bri.Cover_tag - 1
                po_x = 110 + (i % 3) * 156
                po_y = 52 + i // 3 * 156 - bri.slide
                surface2.blit(bri.require_txt[i], (po_x, po_y + 15))
                surface2.blit(bri.wins_txt[i], (po_x, po_y + 45))
                surface2.blit(bri.budget_txt[i], (po_x, po_y + 75))

                surface1.fill((255, 255, 255, 0))
                cover_png = pygame.image.fromstring(StringData['cover_png'], (105, 105), 'RGB')
                po_x = 104 + ((bri.Cover_tag - 1) % 3) * 156
                po_y = 52 + (bri.Cover_tag - 1) // 3 * 156 - bri.slide
                surface1.blit(cover_png, (po_x, po_y))
                screen.blit(surface1, (0, 0))

            # 显示位置条
            if bri.sliding == 1:
                alpha = 150
            else:
                alpha = 100
            points = [(604, bri.slide * 0.67), (624, bri.slide * 0.67), (624, bri.slide * 0.67 + 150),
                      (604, bri.slide * 0.67 + 150)]
            pygame.draw.polygon(surface2, (183, 183, 183, alpha), points, 0)

            screen.blit(surface2, (0, 0))
            pygame.display.update()

            continue

        # 第一图层（静态元件 桥梁+方格）
        surface.fill((255, 255, 255, 0))
        if bri.option != 4:
            surface.blit(frame, (0, 0))
        surface.blit(background, (0, 0))

        # 第二图层（动态元件 背景动画+桥梁部件+游戏控件）
        surface1.fill((255, 255, 255, 0))

        # 显示车
        bri.show_car(mul, car_png)
        # 显示桥梁部件
        bri.show_bridge(mul)
        # 显示初始可选点
        bri.init_point()
        # 动态环境
        bri.environment(gap)

        # 第三图层
        if bri.option == 5:
            surface2.fill((255, 255, 255, 150))
            surface2.blit(headline, (268, 20))
            surface2.blit(line1, (85, 60))
            surface2.blit(line2, (85, 90))
            surface2.blit(line3, (175, 120))
            surface2.blit(line4, (175, 150))
            surface2.blit(line5, (85, 180))
            surface2.blit(line6, (175, 210))
            surface2.blit(line7, (85, 240))
            surface2.blit(line8, (175, 270))
            surface2.blit(line9, (175, 300))
        elif bri.option == 6:
            surface2.fill((255, 255, 255, 150))
            surface2.blit(win_txt, (260, 150))
            if menu_sound_init == 0:
                win_sound.play()
                menu_sound_init = 1
        elif bri.option == 7:
            surface2.fill((255, 255, 255, 150))
            surface2.blit(lose_txt, (240, 150))
            if menu_sound_init == 0:
                lose_sound.play()
                menu_sound_init = 1

        # 显示图标
        if bri.option != 4:
            bri.show_icon()
        # 显示数据
        # bri.show_data()

        # 显示弹出信息
        if save_init != 0 and save_init < 200:
            save_init += 1
            surface1.blit(saved, (490, 312))
        elif save_init >= 200:
            save_init = 0

        # 显示图层
        screen.fill((230, 245, 250))
        screen.blit(surface, (0, 0))
        if bri.option == 4:
            screen.blit(surface3, (0, 0))
        screen.blit(surface1, (0, 0))
        if bri.option in (5, 6, 7):
            screen.blit(surface2, (0, 0))

        # 保存
        if bri.option == 4 and gap % 10 == 0:
            pygame.image.save(screen, f'./screenshot/cover{screenshot}.png')
            screenshot += 1

        gap = (gap + 1) % 120
        pygame.display.update()


if __name__ == '__main__':
    forder = os.path.exists("./screenshot")
    if not forder:
        os.mkdir('./screenshot')
    main()
