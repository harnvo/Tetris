from game_objects import *

def pause():
    while True:
        for event in pygame.event.get():  # 遍历事件
            if event.type == pygame.QUIT:  # 退出事件
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        clock.tick(20)

def event_per_tick(tick,player):
    BLOCK_DOWN_INTERVAL=32-2*player.field.level
    if tick%BLOCK_DOWN_INTERVAL==0:
        pygame.event.post(pygame.event.Event(BLOCK_DOWN))

#__________________________________________###

f=field( 10,10 )
current_block=generate_random_block()
next_block = generate_random_block()
player=observer(f,current_block,next_block)

player.field.render_broader()
player.field.display_score()
pygame.display.update()
player.show_next_block()

tick=0
while keep_going:

    event_per_tick(tick,player)
    
    for event in pygame.event.get():  # 遍历事件
        if event.type == pygame.QUIT:  # 退出事件
            keep_going = False
        elif event.type==pygame.KEYDOWN:
            player.deal_with_keydown(event.key)
            if event.key==pygame.K_SPACE:
                pause()
        elif event.type==BLOCK_DOWN:
            player.block_down()
        elif event.type==UPGRADE:
            player.field.upgrade()
        elif event.type==LOSE:
            print("You lose!")
            keep_going = False

    player.render_block()  
    pygame.display.update()  # 刷新屏幕
    clock.tick(60)
    tick+=1
    

# 退出程序
pygame.quit()
