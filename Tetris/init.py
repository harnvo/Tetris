import pygame
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'box file')
#custom event
BLOCK_DOWN     =pygame.USEREVENT+1
LOSE           =pygame.USEREVENT+2
UPGRADE        =pygame.USEREVENT+3
# 初始设置
pygame.init() # 初始化pygame
screen = pygame.display.set_mode((500,600)) # Pygame窗口
pygame.display.set_caption("俄罗斯方块") # 标题
keep_going = True
DISTANCE=20

clock=pygame.time.Clock()

pic_BLUE = pygame.image.load(filename+"\\blue.jpg")
pic_RED  = pygame.image.load(filename+"\\red.jpg")
pic_GREEN= pygame.image.load(filename+"\\green.jpg")
pic_YELLOW= pygame.image.load(filename+"\\yellow.jpg")
pic_BLACK= pygame.image.load(filename+"\\black.jpg")
pic_WHITE= pygame.image.load(filename+"\\white.jpg")

COLOR_LIST=["RED","BLUE","GREEN","YELLOW"]
BLOCK_LIST=["square","z_block","L_block","line","T_block"]
