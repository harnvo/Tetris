from init import *
import random

def rotate(x,y,xc,yc):#按中心逆时针旋转90度
    x=x-xc
    y=y-yc
    x_ans=-y
    y_ans=x
    return x_ans+xc,y_ans+yc

def generate_z_block(rand_color,rand_pos):
    is_reversed=random.choice([True,False])
    if is_reversed:
        return reversed_z_block(rand_color,rand_pos)
    else:
        return z_block(rand_color,rand_pos)

def generate_L_block(rand_color,rand_pos):
    is_reversed=random.choice([True,False])
    if is_reversed:
        return reversed_L_block(rand_color,rand_pos)
    else:
        return L_block(rand_color,rand_pos)

def generate_random_block():
    rand_color=random.choice(COLOR_LIST)
    rand_block=random.choice(BLOCK_LIST)

    if rand_block=='square':
        rand_pos=random.randint(1,8)
        return square(rand_color,rand_pos)
    elif rand_block=='z_block':
        rand_pos=random.randint(1,7)
        return generate_z_block(rand_color,rand_pos)
    elif rand_block=='L_block':
        rand_pos=random.randint(1,8)
        return L_block(rand_color,rand_pos)
    elif rand_block=='line':
        rand_pos=random.randint(1,9)
        return line(rand_color,rand_pos)
    elif rand_block=='T_block':
        rand_pos=random.randint(1,8)
        return T_block(rand_color,rand_pos)


###_________________________________________###
### game objects
class field:
    def __init__(self,x=0,y=0) -> None:
        #occupied_field[x][y]
        self.occupied_field=[["BLACK" for i in range(20)] for j in range(10)]#where is occupied with boxes
        self.score=0
        self.level=1
        self.pos=(x,y)

    def update_field_info(self,block)->None:
        original_score=self.score

        eliminated_line=0
        
        for box in block.boxes:
            #update occupied field and lowest available place
            x,y=box.get_pos()
            if y==0:
                pygame.event.post(pygame.event.Event(LOSE))
                return

            self.occupied_field[x][y]=box.color

        for y in range(DISTANCE):
            if self.line_is_full(y):
                print(f"line {y} is full!")
                #eliminate the line
                self.eliminate_line(y)
                eliminated_line+=1

        if eliminated_line>=1:
            self.score+=100*2**(eliminated_line-1)

        if self.score//3000 !=original_score//3000:
            pygame.event.post(pygame.event.Event(UPGRADE))

    def line_is_full(self,y):
        for x in range(10):
            if self.occupied_field[x][y]=="BLACK":
                return False

        return True

    def eliminate_line(self,target_y):
        #animation
        for i in range(9):
            self.occupied_field[i][target_y]="BLACK"
            self.occupied_field[i+1][target_y]="WHITE"
            self.refresh_screen()
            pygame.display.update()
            clock.tick(18)


        for x in range(10):
            #update occupied field
            for y in range(target_y-1,0,-1):
                self.occupied_field[x][y+1]=self.occupied_field[x][y]

    def refresh_screen(self):
        screen.fill((0,0,0))  # 刷新屏幕
        for x in range(10):
            for y in range(DISTANCE):
                color = self.occupied_field[x][y]
                pic=eval(f"pic_{color}")
                screen.blit(pic,(DISTANCE*x+self.pos[0],DISTANCE*y+self.pos[1]))

        self.render_broader()
        self.display_score()

    def display_score(self):
        font_score = pygame.font.SysFont('Tahoma', 35, True, False)
        font_level = pygame.font.SysFont('Tahoma', 25, True, False)
        text_score = font_score.render(f'Score:{int(self.score)}', True, (255, 255, 255))
        text_level = font_level.render(f'Level:{self.level}', True, (255, 255, 255))
        screen.blit(text_score, (250, 500))
        screen.blit(text_level, (250, 550))

    def upgrade(self):
        if self.level<=9:
            self.level+=1
    
    def render_broader(self):
        x=self.pos[0]
        y=self.pos[1]
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(-5+x, -5+y, 10*DISTANCE+x, 20*DISTANCE+y),2)

    def valid_pos(self,x,y):
        if x<0 or x>9 or y>19:
            return False

        if self.occupied_field[x][y] != "BLACK":
            return False
        
        return True

    def actual_pos(self,x,y):
        return x*DISTANCE+self.pos[0],y*DISTANCE+self.pos[1]

class box:
    def __init__(self,color,x=0,y=0) -> None:
        self.color=color
        self.pic = eval(f"pic_{color}")
        self.x=x
        self.y=y

    def down(self,t=1):
        self.y=self.y+t

    def left(self,t=1):
        self.x=self.x-t

    def right(self,t=1):
        self.x=self.x+t

    def up(self,t=1):
        self.y=self.y-t

    def get_pos(self):
        return self.x,self.y

    def set_pos(self,x,y):
        self.x=x
        self.y=y

class block:
    def __init__(self,boxes) -> None:
        self.boxes=boxes

    def down(self):
        for box in self.boxes:
            box.down()

    def right(self):
        for box in self.boxes:
            box.right()

    def left(self):
        for box in self.boxes:
            box.left()

    def rotate(self,xc,yc):
        for box in self.boxes[1:]:
            x,y=box.get_pos()
            x1,y1=rotate(x,y,xc,yc)
            box.set_pos(x1,y1)

class square(block):
    def __init__(self,color,x,y=0) -> None:
        LD=box(color,x+1,y)
        LU=box(color,x,y)
        RD=box(color,x+1,y+1)
        RU=box(color,x,y+1)
        self.center_box=LD

        super().__init__([LD,LU,RD,RU])

    def rotate(self):
        #square cannot rotate
        pass

class z_block(block):
    def __init__(self,color,x,y=0) -> None:
        self.center_box=box(color,x,y)
        LD=box(color,x+1,y)
        RD=box(color,x+1,y+1)
        RU=box(color,x+2,y+1)

        super().__init__([self.center_box,LD,RD,RU])

    def rotate(self):
        xc,yc=self.center_box.get_pos()
        super().rotate(xc,yc)

class reversed_z_block(block):
    def __init__(self,color,x,y=0) -> None:
        self.center_box=box(color,x,y+1)
        LD=box(color,x+1,y)
        RD=box(color,x+1,y+1)
        RU=box(color,x+2,y)

        super().__init__([self.center_box,LD,RD,RU])

    def rotate(self):
        xc,yc=self.center_box.get_pos()
        super().rotate(xc,yc)

class L_block(block):
    def __init__(self,color,x,y=0) -> None:
        self.center_box=box(color,x,y)
        LD=box(color,x,y+1)
        RD=box(color,x,y+2)
        RU=box(color,x+1,y+2)

        super().__init__([self.center_box,LD,RD,RU])

    def rotate(self):
        xc,yc=self.center_box.get_pos()
        super().rotate(xc,yc)

class reversed_L_block(block):
    def __init__(self,color,x,y=0) -> None:
        self.center_box=box(color,x,y)
        LD=box(color,x,y+1)
        RD=box(color,x,y+2)
        RU=box(color,x-1,y+2)

        super().__init__([self.center_box,LD,RD,RU])

    def rotate(self):
        xc,yc=self.center_box.get_pos()
        super().rotate(xc,yc)

class line(block):
    def __init__(self,color,x,y=0) -> None:
        self.center_box=box(color,x,y)
        LD=box(color,x,y+1)
        RD=box(color,x,y+2)
        RU=box(color,x,y+3)

        super().__init__([self.center_box,LD,RD,RU])

    def rotate(self):
        xc,yc=self.center_box.get_pos()
        super().rotate(xc,yc)

class T_block(block):
    def __init__(self,color,x,y=0) -> None:
        self.center_box=box(color,x,y)
        LD=box(color,x+1,y)
        RD=box(color,x-1,y)
        RU=box(color,x,y+1)

        super().__init__([self.center_box,LD,RD,RU])

    def rotate(self):
        xc,yc=self.center_box.get_pos()
        super().rotate(xc,yc)

###_________________________________________###

class observer:
    def __init__(self,field:field,block:block,next_block:block) -> None:
        self.field=field
        self.block=block
        self.next_block=next_block

    def unrender_block(self):
        for box in self.block.boxes:
            x,y=box.get_pos()
            x,y=self.field.actual_pos(x,y)
            screen.blit(pic_BLACK,(x,y))

    def render_block(self):
        for box in self.block.boxes:
            x,y=box.get_pos()
            x,y=self.field.actual_pos(x,y)
            screen.blit(box.pic,(x,y))

    def valid_transition(self,movement):
        dx,dy=0,0
        if movement=='down':
            dy=1
        elif movement=='left':
            dx=-1
        elif movement=='right':
            dx=1

        for box in self.block.boxes:
            x,y=box.get_pos()
            if not self.field.valid_pos(x+dx,y+dy):
                return False

        return True

    def valid_rotation(self):
        xc,yc=self.block.boxes[0].get_pos()
        for box in self.block.boxes[1:]:
            x,y=box.get_pos()
            x1,y1=rotate(x,y,xc,yc)
            if not self.field.valid_pos(x1,y1):
                return False

        return True

    def block_down(self):
        if self.valid_transition('down'):
            self.unrender_block()
            self.block.down()
            self.render_block()
        else:
            #post event BLOCK_ON_GROUND
            pygame.event.post(pygame.event.Event(BLOCK_ON_GROUND))
            return

    def block_left(self):
        if self.valid_transition('left'):
            self.unrender_block()
            self.block.left()
            self.render_block()

    def block_right(self):
        if self.valid_transition('right'):
            self.unrender_block()
            self.block.right()
            self.render_block()

    def block_rotate(self):
        if self.valid_rotation():
            self.unrender_block()
            self.block.rotate()
            self.render_block()

    def deal_with_keydown(self,key:pygame.event):
        if key==pygame.K_s:
            self.block_down()
        elif key==pygame.K_d:
            self.block_right()
        elif key==pygame.K_a:
            self.block_left()
        elif key==pygame.K_r:
            self.block_rotate()

    def deal_with_BLOCK_ON_GROUND(self):
        self.field.update_field_info(self.block)
        self.block=self.next_block
        self.next_block=generate_random_block()
        self.field.score+=7
        self.field.refresh_screen()
        self.show_next_block()

    def show_next_block(self):
        x,y=self.next_block.boxes[0].get_pos()
        dx=12*DISTANCE-x*DISTANCE+self.field.pos[0]
        dy=2*DISTANCE+self.field.pos[1]
        for box in self.next_block.boxes:
            x,y=box.get_pos()
            screen.blit(box.pic,(x*DISTANCE+dx,y*DISTANCE+dy))

###_____________________________________###



