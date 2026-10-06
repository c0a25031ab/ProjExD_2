import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        bb_accs.append(r)
    return bb_imgs, bb_accs

def check_bound(rect:pg.Rect) -> tuple[bool,bool]:
    yoko,tate = True,True
    if rect.left < 0 or WIDTH <rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:

    go_surf = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_surf, (0,0,0), (0,0,WIDTH,HEIGHT))
    go_surf.set_alpha(150) 
    screen.blit(go_surf, (0,0))

    font = pg.font.Font(None,80)
    txt = font.render("Game Over", True, (255,255,255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH//2, HEIGHT//2
    screen.blit(txt, txt_rct)

    kk_cry = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,0.9)
    kk_r1 = kk_cry.get_rect()
    kk_r1.center = WIDTH//2-220, HEIGHT//2
    kk_r2 = kk_cry.get_rect()
    kk_r2.center = WIDTH//2+220, HEIGHT//2
    screen.blit(kk_cry,kk_r1)
    screen.blit(kk_cry,kk_r2)

    pg.display.update()
    pg.time.wait(5000)

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_base = pg.image.load("fig/3.png")

    left = kk_base
    right = pg.transform.flip(kk_base, True, False)

    kk_imgs = {
        (-5, 0): pg.transform.rotozoom(left, 0, 0.9),  
        (-5,-5): pg.transform.rotozoom(left, -45, 0.9),
        (-5,+5): pg.transform.rotozoom(left, 45, 0.9), 

        (+5, 0): pg.transform.rotozoom(right, 0, 0.9),   
        (+5,-5): pg.transform.rotozoom(right, 45, 0.9),  
        (+5,+5): pg.transform.rotozoom(right, -45, 0.9), 
        (0, -5): pg.transform.rotozoom(right, 90, 0.9),  
        (0, +5): pg.transform.rotozoom(right, -90, 0.9),

        (0, 0): pg.transform.rotozoom(left, 0, 0.9),
    }
    return kk_imgs





def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_imgs = get_kk_imgs()
    kk_rct = kk_imgs[(0,0)].get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]


        kk_img = kk_imgs[tuple(sum_mv)]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
            
        screen.blit(kk_img, kk_rct)

        idx = min(tmr//500, 9)
        bb_img = bb_imgs[idx]
        acc = bb_accs[idx]
        avx = vx * acc
        avy = vy * acc

        bb_rct.move_ip(avx, avy)
    
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        screen.blit(bb_img, bb_rct)

        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *=-1
        if not tate:
            vy *=-1

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
