# -*- coding: utf-8 -*-
import pgzrun
from pgzhelper import *
import winsound
import random
import math
import os

WIDTH = 900
HEIGHT = 600
TITLE = 'Space Hunter'

enemys=[]
missiles=[]
e_shots=[]
u_data=[]

message=["このゲームはシューティングゲームです。",
         "右から飛んでくるロケットを撃てば倒せます。",
         "十字キーで移動、SPACEキーで弾を撃つことができます。",
         "左SHIFTを押しながら十字キーを押すと遅く移動できます。",
         "ESCキーを押すことでゲームを一時停止することができます。",
         "一定時間経つとステージクリアになります。",
         "そのあと次の戦闘で役に立つスキルがもらえます。",
         "左右キーで選択し、ENTERキーかSPACEキーで取得できます。",
         "スキルを選択すると次のステージへ進みます。",
         "合計でステージは5個あり、最後にはボスが現れます。",
         "ボスは弾幕を飛ばしてきます。",
         "赤色の目玉を撃ってボスを倒してください。"]

skill=["       HP+","Multi Angle Shot","   Double Shot","invincible Time+",
       "      Heal","    explode"," EnemyTime Slow","    Fast Move",
       "   Penetration","    Time Cut+","   Charge Shot","   Reflection",
       " Physics Shield","      Bomb","     Attack+","  Miss assist",
       "   Enemy Bond","   Shot Cool+","    Kill Heal","Adversity Revers",
       "      Relive"," "]

sk_mean=["最大体力を1増加させる",
         "弾を打った時多方向に弾が飛んでいく\nだが弾の連射力が落ちる",
         "弾を撃った時に弾が二発でる\nだが弾の連射力が落ちる",
         "ダメージを受けた時の無敵時間を増加させる",
         "体力を最大まで回復する",
         "ダメージを受けたとき敵に向かって散弾を飛ばす",
         "敵の動く速度が遅くなる",
         "移動が速くなる",
         "敵を弾が貫通するようになる",
         "ステージクリアまでの時間が短くなる",
         "溜め攻撃ができるようになる",
         "敵の弾と自分の弾がぶつかったときに\n敵のほうへ100%弾が反射される",
         "敵の本体に当たってもダメージを受けない",
         "一回だけ使用可能なすべてを消せる爆弾を設置する\nZキーを押すと使用できる",
         "弾一発ずつの攻撃力が上昇する",
         "弾が敵に当たらなかったとき5%の確率で\n弾が敵のほうへ追尾していく",
         "敵の種類が一定になる",
         "弾を次打つまでのクールタイムを短縮する",
         "敵を倒した時まれに一時的に体力を回復する",
         "体力が減るごとに攻撃力が増えていく",
         "体力が0になると一度だけ復活できる"]

number = [3,2,1]
skil_ch=[len(sk_mean),len(sk_mean),len(sk_mean),len(sk_mean)]

#ステータス
maxHP = 3
HP = maxHP
sp = 5
sp_back = sp
damhl_time = 120
stage_cl = 1800
bombcnt = 3
multis = 0
shotnum = 1
s_cool_time = 20
attack = 1
sub_HP = 0
refle = False
p_shield = False
expl = False
pane = False
charge = False
mas = False
sub_HP_flg = False
HP_atk_flg = False
live = False

#敵ステータス
sp_e = 2
normal_e_life = 2
motemp = 0.04
thremo = 4
enemy_const = False
e_s_sp = 3

shield_HP = 100
boss_HP = 100

#スコア
killcnt = 0
misscnt = 0
skilcnt = 0
stage = 1

#スキル選択用宣言
i = 0
r = 0
e = 0
r_flg = False
select_sk = 1

#内部向け宣言
gamecount = 0
nowcount = 0
gamemode = 0	#0:タイトル 1:プレイ画面 2:スキル選択 3:スコア表示 #4:設定画面
                #10:1から2へ移動 11:4から1へ移動
come_s = 0
dif_cnt = 180
setting_st_cnt = 1
pf = 0
attack_cnt = 0
bgcnt = 0
chg_time = 0
b_s_mode = 0
boss_delay = 0
sk_se = 1
sk_cnt = 0
b_one_temp = 0
bom_delay = 0
st_cnt = 1
boss_s_cnt = 0
b_a = 1
sound_flg = True
hit = False
sp_flg = False
b_set = True
on_off_flg = True
damagetime = 0
st_se = False
shield_flg = False
skill_flag = True
shutdown_flg = False
difficulty = 1
boss_ani_cnt = 241
boss_not = False
game_co = 0 #クリアかオーバーか確認用

#仮置き
push_shot_cnt = 0
numcnt = 0
rest = 0
st_cnt = 1
total = 0
hitme = False
none_flg = False
stcnt_temp = 0
kil_temp = 0
miss_temp = 0
HP_temp = 0
skcnt_temp = 0
shutcnt = -1
delay = 0
u_d = './data/userdata.txt'

#素材用意
player = Actor('player.png',topleft=(0,HEIGHT / 2))  #スクリプト
chg = Actor('charge_now.png',topleft=(player.x,player.y))
target = Actor("tg.png",topleft=(-100,-100))
sub1_boss = Actor("sub_core.png",topleft=(-100,-100))
sub2_boss = Actor("sub_core.png",topleft=(-100,-100))
shield = Actor("shield.png",center=(-100,-100))
boss = Actor("core.png",topleft=(-100,-100))
shot = Actor('shoot.png',topleft=(0,0))
e_shot = Actor('e_shot.png',topleft=(0,0))
push = Actor('push.png',topleft=(WIDTH / 3.6,HEIGHT / 1.5))  #UI
bomb = Actor('bomb.png',topleft=(0,0))
heart = Actor('heart.png',topleft=(0,0))
heart_no = Actor('heart_dark.png',topleft=(0,0))
heart_inv = Actor('heart_inv.png',topleft=(0,0))
heart_no_inv = Actor('heart_dark_inv.png',topleft=(0,0))
bosbar = Actor('hp_bar.png',topleft=(5,HEIGHT -30))
bo = Actor('bohp.png',topleft=(-100,-100))
log = Actor("log.png",topleft=(0,0))
esc = Actor('esc.png',topleft=(600,550))
menu = Actor('menu.png',topleft=(0,0))      #Back_Ground
b_bg = Actor("boss_back_ground.png",topleft=(0,0))
skill_bg = Actor('skill.png',topleft=(0,0))
bg = Actor('back_ground.png',topleft=(0,0))
s_bg = Actor("back_ground2.png",topleft=(0,0))
pinchi = Actor('pinchi.png',topleft=(0,0))
lg_bg = Actor('black.png',topleft=(0,0))
feed_back = Actor("feed_back.png",topleft=(0,0))

#スコアランキングファイル作成
if os.path.exists(u_d) == False:
    f = open(u_d,'w',encoding='UTF-8')
    f.close()

hide_mouse()

def draw():
    global gamecount,nowcount,gamemode,pf,killcnt,misscnt,stage_cl,damagetime,sk_se
    global skilcnt,stage,r,e,select_sk,bombcnt,bgcnt,refle,HP,damhl_time,sk_cnt
    global p_shield,expl,number,numcnt,delay,pane,shutdown_flg,message,maxHP
    global st_cnt,setting_st_cnt,chg_time,bom_delay,b_s_mode,boss_HP,attack,HP,kil_temp
    global miss_temp,HP_temp,skcnt_temp,stcnt_temp,stcnt_temp,total,hitme,none_flg
    global u_data,difficulty,hit,shield_flg,boss_ani_cnt,boss_not,shield_HP,sub_HP
    global live,sound_flg
    set_flg = False
    u_te_back = 0
    u_temp = 0
    chg_cnt = 0
    
    if sound_flg:
        if stage < 5 and gamemode == 1:
            sounds.bgm.play(-1)
            sound_flg = False
        if gamemode == 1 and stage == 5:
            sounds.bgm_boss.play(-1)
            sound_flg = False
    
    screen.clear()
    if stage <= 2:
        bg.draw()
    else:
        if stage <= 4:
            s_bg.draw()
        else:
            b_bg.draw()

    if stage == 5:
        if b_s_mode == 2:
            target.draw()

    if gamemode != 15:
        for e_shot in e_shots:    #敵の弾表示
            e_shot.draw()
            
        if damagetime == 0 or damagetime % 5 == 0:
            player.draw()

        for obj in enemys:
            obj.draw()

        for missile in missiles:
            missile.draw()

    if gamemode == 0:  #タイトル画面
        screen.draw.text("Space Hunter",(WIDTH / 4,HEIGHT  / 3),color='YELLOW',owidth=1,fontsize=100)
        if gamecount >= 30 and gamecount < 60:
            push.draw()
        if gamecount >= 60:
            gamecount = 0

    if gamemode == 1:   #ゲームプレイ画面
        if gamecount < stage_cl:
            if stage <= 2:    #背景出力
                if bgcnt < 53:
                    bgcnt += 0.01
                bg.topleft=(3180 / (stage_cl / 30 ) * ( -1 * bgcnt),0)
            else:
                if stage <= 4:      #ステージ4以降の背景
                    if bgcnt < 53:
                        bgcnt += 0.01
                    s_bg.topleft=(3180 / (stage_cl / 30 ) * ( -1 * bgcnt),0)
        for enemy in enemys:
            for missile in missiles:
                if enemy.colliderect(missile):
                    if pane:
                        missile.x = enemy.x + 40
                        enemy.life -= missile.dmg
                    else:
                        if missile.ss:
                            enemy.life -= missile.dmg
                            if enemy.life >= 1:
                                missile.x + 70
                        else:
                            hitme = True
                            enemy.life -= missile.dmg
                    if enemy.life <= 0:
                        hit = True
                        killcnt += 1
                        if sub_HP_flg:
                            if missile.random_kill == 1:
                                winsound.PlaySound('sub_heal.wav',winsound.SND_ASYNC)
                                sub_HP += 1
                    else:
                        if enemy.mode == 1:
                            enemy.next_image()

                if hitme:
                    missiles.remove(missile)
                    hitme = False
                    
            if enemy.x <= -15:
                hit = True
                misscnt+= 1
            if enemy.colliderect(player):
                if p_shield == False:
                    if damagetime == 0:
                        hit = True
                        if sub_HP  >= 1:
                            sub_HP -= 1
                        else:
                            HP -= 1
                        damagetime = damhl_time
                        if expl:
                            for i in range(5):
                                missile = MultiShot("shoot",random.randrange(-45,45),0,1,1)
                                missiles.append(missile)
                else:
                    hit = True
                    misscnt += 1
                    winsound.PlaySound('reflect.wav.',winsound.SND_ASYNC)

            if hit:
                enemys.remove(enemy)
                hit = False

        for e_shot in e_shots:
            if e_shot.colliderect(player):
                if damagetime == 0:
                    hit = True
                    if sub_HP >= 1:
                            sub_HP -= 1
                    else:
                        HP -= 1
                    if HP_atk_flg:
                        attack += 1
                    damagetime = damhl_time
                    if expl:
                        for i in range(5):
                            missile = MultiShot("shoot",random.randrange(-45,45),0,1,1)
                            missiles.append(missile)
            if hit:
                e_shots.remove(e_shot)
                hit = False

        for missile in missiles:
            for e_shot in e_shots:
                if missile.colliderect(e_shot):
                    if refle:
                        if stage != 5:
                            e_shots.remove(e_shot)
                            if missile.re == False:
                                hit = True
                                missile = Refle_Shot("e_shot.png",attack,True,False)
                                missile.x = e_shot.x - 35
                                missile.y = e_shot.y
                                missiles.append(missile)
                            else:
                                hit = True
                missile.draw()

            if missile.colliderect(boss):
                hit = True
                if boss_HP > 0:
                    if boss_not == False:
                        boss_HP -= attack
            if shield.colliderect(missile):
                hit = True
                if shield_HP > 0:
                    shield_HP -= attack
                else:
                    boss_not = False
            if hit:
                missiles.remove(missile)
                hit = False
        if boss_HP <= 0:
            b_s_mode = 0
            bom_delay = 60
            screen.fill((255,255,255))
            winsound.PlaySound('voices.wav.',winsound.SND_ASYNC)
            Next_Stage()


        if stage == 5:          #ボス表示
            boss.draw()
            if b_s_mode == 3 or b_s_mode == 4:
                sub1_boss.draw()
                sub2_boss.draw()

            if b_s_mode == 5:
                log.draw()
                if shield_HP <= 0:
                    shield.center=(-100,-100)
                else:
                    shield.center=(boss.x,boss.y)
                    shield.draw()
                    

                if boss_ani_cnt % 30 == 0:
                    log.center=(WIDTH / 2,HEIGHT + 40 - (10 * (boss_ani_cnt / 30)))
                screen.draw.text("少しだけ休憩!!",center=(WIDTH / 2,HEIGHT + 40 - (10 * (boss_ani_cnt / 30))),fontsize=50,fontname="senobi-gothic")
            else:
                shield.center=(-100,-100)

            for i in range(boss_HP):
                bo.topleft=(20 + 8 * i,HEIGHT - 16)
                bosbar.draw()
                bo.draw()
                

    if chg_time > 0:
        chg.center=(player.x + 50,player.y)
        if chg_time > 20:
            if chg_time < 40:
                chg.scale = 0.8
            else:
                if chg_time < 60:
                    chg.scale = 1
                else:
                    if chg_time < 80:
                        chg.scale = 1.3
                    else:
                        if chg_time <= 120:
                            chg.scale = 1.5
                        if chg_time == 119:
                            winsound.PlaySound('charge_full.wav.',winsound.SND_ASYNC)
                chg.draw()
    else:
        chg.scale = 1

    if HP == 1:
        pinchi.draw()

    if bom_delay > 0:
        screen.fill((255,255,255))

    if gamemode != 15:
        if bombcnt >= 0:
            for x in range(bombcnt):    #爆弾の使用可能数
                bomb.topleft=(WIDTH - (70 * (x + 1)),HEIGHT - 72)
                bomb.draw()
                
        if player.y >  80:
            if maxHP != HP:
                for i in range(maxHP - HP):  #最大体力
                    heart_no.topleft=((HP * 62) + (62 * i),0)
                    heart_no.draw()

            for i in range(HP): #現在の体力
                heart.topleft=(62 * i,0)
                heart.draw()

            if sub_HP >= 1:
                heart.scale = 0.5
                for i in range(sub_HP):
                    heart.topleft=((62 * maxHP) + 16 + (62 * i),16)
                    heart.draw()
                heart.scale = 1
        else:
            if maxHP != HP:
                for i in range(maxHP - HP):  #最大体力
                    heart_no_inv.topleft=((HP * 62) + (62 * i),0)
                    heart_no_inv.draw()

            for i in range(HP): #現在の体力
                heart_inv.topleft=(62 * i,0)
                heart_inv.draw()

            if sub_HP >= 1:
                heart_inv.scale = 0.5
                for i in range(sub_HP):
                    heart_inv.topleft=((62 * maxHP) + 16 + (62 * i),16)
                    heart_inv.draw()
                heart_inv.scale = 1
    
    if gamemode == 2:   #スキルの選択画面
        skill_bg.draw()
        esc.topleft=(480,0)
        esc.draw()
        screen.draw.text("でスキルを選ばずに進む",(550,0),fontsize=30,fontname="senobi-gothic")

        screen.draw.text(str(skill[r]),(WIDTH / 11.25,HEIGHT / 3.33),color="WHITE",fontsize=40,fontname="misaki_gothic")
        screen.draw.text(str(skill[e]),(WIDTH / 1.8,HEIGHT / 3.33),color="WHITE",fontsize=40,fontname="misaki_gothic")

        if select_sk == 1:
            screen.draw.text(str(sk_mean[r]),(WIDTH /  7.5,HEIGHT / 1.2),color="WHITE",fontsize=30,fontname="misaki_gothic")
        else:
            screen.draw.text(str(sk_mean[e]),(WIDTH /  7.5,HEIGHT / 1.2),color="WHITE",fontsize=30,fontname="misaki_gothic")

        if select_sk == 1:
            screen.draw.text("____________",(WIDTH / 11.25,HEIGHT / 3.33),color="WHITE",fontsize=70)
        else:
            screen.draw.text("____________",(WIDTH / 1.8,HEIGHT / 3.33),color="WHITE",fontsize=70)
            
        if nowcount >= 30 and nowcount < 60:
            screen.draw.text("Select Enter",(WIDTH / 2.57,HEIGHT / 1.5),color="WHITE",fontsize=40,fontname="misaki_gothic")
        if nowcount >= 60:
            nowcount = 0

    if gamemode == 3:   #スコア表示
        menu.draw()
        screen.draw.text("SCORE",(WIDTH / 1.43,HEIGHT / 20),color="WHITE",fontsize=70)
        screen.draw.text("ENEMY KILL:" + str(killcnt),(WIDTH / 1.64,HEIGHT / 7.5),color="WHITE",fontsize=60)
        screen.draw.text("MISS ENEMY:" + str(misscnt),(WIDTH / 1.64,HEIGHT / 4),color="WHITE",fontsize=60)
        screen.draw.text("HEALTH :",(WIDTH / 1.64,HEIGHT / 2.73),color="WHITE",fontsize=60)
        screen.draw.text("GET SKILL :" + str(skilcnt),(WIDTH / 1.64,HEIGHT / 2.07),color="WHITE",fontsize=60)
        screen.draw.text("CLEAR STAGE:" + str(stage -1),(WIDTH / 1.64,HEIGHT / 1.62),color="WHITE",fontsize=55)
        screen.draw.text("Get Skills",(80,200),color="WHITE",fontsize=70)
        for i in range(4):
            screen.draw.text("・" + str(skill[skil_ch[i]]),(80,250 + (60 * i)),color="WHITE",fontsize=45,fontname="senobi-gothic")
        heart.scale = 0.4
        heart_no.scale = 0.4
        for i in range(maxHP):
            heart_no.topleft=(750 + (26 * i),225)
            heart_no.draw()

        for i in range(HP):
            heart.topleft=(750 + (26 * i),225)
            heart.draw()
        heart.scale = 1
        heart_no.scale = 1
            
    if gamemode == 4:
        menu.draw()
        screen.draw.text("音楽：BGMer",center=(700,HEIGHT - 40),color="YELLOW",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("Setting",(WIDTH / 1.42,HEIGHT / 20),color="WHITE",fontsize=65)
        if st_cnt == 1:
            screen.draw.text("ゲームを再開",(580,90),color="RED",fontsize=40,fontname="senobi-gothic")
        else:
            screen.draw.text("ゲームを再開",(580,90),color="WHITE",fontsize=36,fontname="senobi-gothic")
        if st_cnt == 2:
            screen.draw.text("操作方法",(580,160),color="RED",fontsize=40,fontname="senobi-gothic")
        else:
            screen.draw.text("操作方法",(580,160),color="WHITE",fontsize=36,fontname="senobi-gothic")
        if st_cnt == 3:
            screen.draw.text("リセット",(580,230),color="RED",fontsize=40,fontname="senobi-gothic")
        else:
            screen.draw.text("リセット",(580,230),color="WHITE",fontsize=36,fontname="senobi-gothic")
        if st_cnt == 4:
            screen.draw.text("スキル内容",(580,300),color="RED",fontsize=40,fontname="senobi-gothic")
        else:
            screen.draw.text("スキル内容",(580,300),color="WHITE",fontsize=36,fontname="senobi-gothic")
        if st_cnt == 5:
            screen.draw.text("ゲームを終了",(580,370),color="RED",fontsize=40,fontname="senobi-gothic")
        else:
            screen.draw.text("ゲームを終了",(580,370),color="WHITE",fontsize=36,fontname="senobi-gothic")

        screen.draw.text("Now Score",(WIDTH / 11.25,HEIGHT / 10),color="WHITE",fontsize=70)
        screen.draw.text("ENEMY KILL:" + str(killcnt),(WIDTH / 9,HEIGHT / 5.45),color="WHITE",fontsize=40)
        screen.draw.text("MISS ENEMY:" + str(misscnt),(WIDTH / 9,HEIGHT / 4),color="WHITE",fontsize=40)
        screen.draw.text("HEALTH :",(100,HEIGHT / 3.16),color="WHITE",fontsize=40)
        screen.draw.text("GET SKILL :" + str(skilcnt),(WIDTH / 9,HEIGHT / 2.61),color="WHITE",fontsize=40)
        screen.draw.text("CLEAR STAGE:" + str(stage -1),(100,HEIGHT / 2.22),color="WHITE",fontsize=40)
        screen.draw.text("Get Skills",(80,350),color="WHITE",fontsize=70)
        for i in range(4):
            screen.draw.text("・" + str(skill[skil_ch[i]]),(80,400 + (40 * i)),color="WHITE",fontsize=40,fontname="senobi-gothic")

        heart.scale = 0.5
        heart_no.scale = 0.5
        for i in range(maxHP):
            heart_no.topleft=((WIDTH / 3.83) + (37 * i),HEIGHT / 3.24)
            heart_no.draw()

        for i in range(HP):
            heart.topleft=((WIDTH / 3.83) + (37 * i),HEIGHT / 3.24)
            heart.draw()

        heart.scale = 1
        heart_no.scale = 1

    if gamemode == 5:
        lg_bg.draw()
        if st_cnt == 1:
            screen.draw.text("スタート",center=(WIDTH / 2,HEIGHT / 2),color="RED",fontsize=70,fontname="senobi-gothic")
            screen.draw.text("遊び方",center=(WIDTH / 2,350),color="WHITE",fontsize=48,fontname="senobi-gothic")
            screen.draw.text("ランキング",center=(WIDTH / 2,420),color="WHITE",fontsize=30,fontname="senobi-gothic")
            screen.draw.text("ゲームを終了",center=(WIDTH / 2,460),color="WHITE",fontsize=20,fontname="senobi-gothic")
        if st_cnt == 2:
            screen.draw.text("スタート",center=(WIDTH / 2,240),color="WHITE",fontsize=35,fontname="senobi-gothic")
            screen.draw.text("遊び方",center=(WIDTH / 2,HEIGHT / 2),color="RED",fontsize=70,fontname="senobi-gothic")
            screen.draw.text("ランキング",center=(WIDTH / 2,370),color="WHITE",fontsize=35,fontname="senobi-gothic")
            screen.draw.text("ゲームを終了",center=(WIDTH / 2,410),color="WHITE",fontsize=25,fontname="senobi-gothic")
        if st_cnt == 3:
            screen.draw.text("スタート",center=(WIDTH / 2,180),color="WHITE",fontsize=25,fontname="senobi-gothic")
            screen.draw.text("遊び方",center=(WIDTH / 2,240),color="WHITE",fontsize=48,fontname="senobi-gothic")
            screen.draw.text("ランキング",center=(WIDTH / 2,HEIGHT / 2),color="RED",fontsize=63,fontname="senobi-gothic")
            screen.draw.text("ゲームを終了",center=(WIDTH / 2,370),color="WHITE",fontsize=35,fontname="senobi-gothic")
        if st_cnt == 4:
            screen.draw.text("スタート",center=(WIDTH / 2,120),color="WHITE",fontsize=20,fontname="senobi-gothic")
            screen.draw.text("遊び方",center=(WIDTH / 2,150),color="WHITE",fontsize=35,fontname="senobi-gothic")
            screen.draw.text("ランキング",center=(WIDTH / 2,210),color="WHITE",fontsize=48,fontname="senobi-gothic")
            screen.draw.text("ゲームを終了",center=(WIDTH / 2,HEIGHT / 2),color="RED",fontsize=63,fontname="senobi-gothic")

    if gamemode == 6:
        menu.draw()
        if setting_st_cnt == 1:
            screen.draw.text("難易度",(635,20),fontsize=50,fontname="senobi-gothic")
            screen.draw.text("・ステージの難易度を選択",(50,80),fontsize=30,fontname="senobi-gothic")
            screen.draw.text("・敵の体力",(50,140),fontsize=40,fontname="senobi-gothic")
            screen.draw.text("・移動速度",(50,230),fontsize=40,fontname="senobi-gothic")
            screen.draw.text("・敵の出現速度",(50,330),fontsize=40,fontname="senobi-gothic")
            if st_cnt == 1:
                screen.draw.text("やさしい",(580,90),color="RED",fontsize=44,fontname="senobi-gothic")
                screen.draw.text("普通の敵の体力が1と2しかない",(30,180),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("ゆっくりとのんびりと",(30,270),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("あなたのためにガソリンスタンドで\n給油待ちのような速度でお届けします",(30,370),fontsize=30,fontname="senobi-gothic")
            else:
                screen.draw.text("やさしい",(580,90),color="WHITE",fontsize=40,fontname="senobi-gothic")
            if st_cnt == 2:
                screen.draw.text("ふつう",(580,160),color="RED",fontsize=44,fontname="senobi-gothic")
                screen.draw.text("普通の敵の体力が1と2しかない",(30,180),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("ゆっくりとのんびりと",(30,270),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("夜中の改札の人通りの\nような速度でお届けします",(30,370),fontsize=30,fontname="senobi-gothic")
            else:
                screen.draw.text("ふつう",(580,160),color="WHITE",fontsize=40,fontname="senobi-gothic")
            if st_cnt == 3:
                screen.draw.text("むずかしい",(580,230),color="RED",fontsize=44,fontname="senobi-gothic")
                screen.draw.text("全部の敵の体力が2となっています",(30,180),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("早歩きで行きますよ",(30,270),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("通勤ラッシュの自転車の\nような速度でお届けします",(30,370),fontsize=30,fontname="senobi-gothic")
            else:
                screen.draw.text("むずかしい",(580,230),color="WHITE",fontsize=40,fontname="senobi-gothic")
            if st_cnt == 4:
                screen.draw.text("めちゃむず",(580,300),color="RED",fontsize=44,fontname="senobi-gothic")
                screen.draw.text("2ですよ",(30,180),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("飛行機雲ができるほどの速度",(30,270),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("満員電車に乗り込む人たちの\nような速度でお届けします",(30,370),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("・自分の体力",(50,450),fontsize=40,fontname="senobi-gothic")
                screen.draw.text("体力が2だなんて辛くて息切れを起こしそう",(30,490),fontsize=30,fontname="senobi-gothic")

            else:
                screen.draw.text("めちゃむず",(580,300),color="WHITE",fontsize=40,fontname="senobi-gothic")
        if setting_st_cnt == 2:
            screen.draw.text("スキル",(635,20),fontsize=50,fontname="senobi-gothic")
            screen.draw.text("・ステージをクリアするごとに\n          手に入るスキルの有無",(50,200),fontsize=30,fontname="senobi-gothic")

            if st_cnt == 1:
                screen.draw.text("あり",(580,125),color="RED",fontsize=44,fontname="senobi-gothic")
            else:
                screen.draw.text("あり",(580,125),color="WHITE",fontsize=40,fontname="senobi-gothic")
            if st_cnt == 2:
                screen.draw.text("なし",(580,265),color="RED",fontsize=44,fontname="senobi-gothic")
            else:
                screen.draw.text("なし",(580,265),color="WHITE",fontsize=40,fontname="senobi-gothic")

    if gamemode == 10:
        screen.draw.text("ステージクリア",(WIDTH / 6,HEIGHT / 2.73),color='WHITE',owidth=1,fontsize=70,fontname="senobi-gothic")

    if gamemode == 11:
        if rest % 60 != 0:
            if numcnt < 3:
                screen.draw.text(str(number[numcnt]),(WIDTH / 2.5,HEIGHT / 10),fontsize=400,fontname="senobi-gothic")
        else:
            if numcnt <= 2:
                numcnt += 1
            else:
                numcnt = 0
        if numcnt == 3:
            gamemode = 1

    if gamemode == 12:
        bgcnt += 3
        lg_bg.draw()
        feed_back.topleft=(0,-900 + bgcnt)
        feed_back.draw()
            
        if shutdown_flg:
            screen.draw.text("ゲームを終了しています...",(30,200),fontsize=70,fontname="senobi-gothic")

    if gamemode == 13:
        lg_bg.draw()
        esc.topleft=(600,550)
        esc.draw()
        screen.draw.text("で画面を閉じる",(680,550),fontsize=30,fontname="senobi-gothic")
        for i in range(12):
            screen.draw.text(message[i],(10,10 + (50 * i)),fontsize=30,fontname="senobi-gothic")
        
    if gamemode == 15:      #スキル解説表示
        lg_bg.draw()
        esc.topleft=(600,0)
        esc.draw()
        screen.draw.text(str(sk_se) + "/3",(850,550),fontsize=25,fontname="senobi-gothic")        
        screen.draw.text("上下キーで移動",(350,0),fontsize=25,fontname="senobi-gothic")        
        screen.draw.text("で画面を閉じる",(680,0),fontsize=30,fontname="senobi-gothic")
        screen.draw.text("スキル説明",(10,50),owidth=1,fontsize=40,fontname="senobi-gothic")
        if sk_se == 1:
            sk_cnt = 0
            for sk_cnt in range(7):
                screen.draw.text(skill[sk_cnt],(50,110 + (70 * sk_cnt)),fontsize=30,fontname="misaki_gothic")
                screen.draw.text(sk_mean[sk_cnt],(320,110 + (70 * sk_cnt)),fontsize=20,fontname="misaki_gothic")
                screen.draw.text("____________________",(50,90 +(70 * sk_cnt)),fontsize=100)
        if sk_se == 2:
            sk_cnt = 7
            while True:
                screen.draw.text(skill[sk_cnt],(50,-380 + (70 * sk_cnt)),fontsize=30,fontname="misaki_gothic")
                screen.draw.text(sk_mean[sk_cnt],(320,-380 + (70 * sk_cnt)),fontsize=20,fontname="misaki_gothic")
                screen.draw.text("____________________",(50,-400 +(70 * sk_cnt)),fontsize=100)
                sk_cnt += 1
                if sk_cnt == 14:
                    break
        if sk_se == 3:
            sk_cnt = 14
            while True:
                screen.draw.text(skill[sk_cnt],(50,-870 + (70 * sk_cnt)),fontsize=30,fontname="misaki_gothic")
                screen.draw.text(sk_mean[sk_cnt],(320,-870 + (70 * sk_cnt)),fontsize=20,fontname="misaki_gothic")
                screen.draw.text("____________________",(50,-890 +(70 * sk_cnt)),fontsize=100)
                sk_cnt += 1
                if sk_cnt == len(sk_mean):
                    break

    if gamemode == 17:
        u_te_back_y = 0
        u_te_back_x = 0
        u_temp = 0
        data_temp = []
        int_data = []
        
        lg_bg.draw()
        esc.topleft=(600,0)
        esc.draw()
        screen.draw.text("で画面を閉じる",(680,0),fontsize=30,fontname="senobi-gothic")
        if none_flg:
            screen.draw.text("まだ誰も挑戦していません!!\n遊んで記録を残しましょう!!",(100,250),fontsize=50,fontname="senobi-gothic")
        else:
            with open(u_d,'r',encoding='UTF-8') as f:
                data_temp = f.readlines()
            int_data = list(map(int,data_temp))
            u_data = sorted(int_data,reverse=True)

            screen.draw.text("上下キーで移動",(350,0),fontsize=25,fontname="senobi-gothic")        
            screen.draw.text("で画面を閉じる",(680,0),fontsize=30,fontname="senobi-gothic")
            screen.draw.text("ランキング",(10,50),owidth=1,fontsize=40,fontname="senobi-gothic")
            while True:
                if u_temp +1 > 0 and u_temp +1 <= 3:
                    screen.draw.text(str(u_temp + 1),(60 + (30 * u_te_back_y),(100 - u_te_back_y * 70) + (70 * u_temp)),color="RED",ocolor="WHITE",owidth=0.5,fontsize=80)
                else:
                    screen.draw.text(str(u_temp + 1),(60 + (30 * u_te_back_y),(100 - u_te_back_y * 70) + (70 * u_temp)),fontsize=40,fontname="senobi-gothic")
                screen.draw.text(str(u_data[u_temp]) + "点",(115 + (30 * u_te_back_y),(110 - u_te_back_y * 70) + (70 * u_temp)),fontsize=30,fontname="senobi-gothic")
                screen.draw.text("_____________________",(50,90 +(70 * u_temp)),fontsize=100)
                u_temp += 1
                if u_temp % 7 == 0:
                    u_te_back_y = u_temp
                    u_te_back_x += 1
                if u_temp >= len(u_data):
                    break

    if gamemode == 21:
        lg_bg.draw()
        screen.draw.text("Enemy Kill:    " +str(killcnt) + " × 10 = " + str(kil_temp),(50,10),color="WHITE",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("－",(300,60),color="WHITE",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("Miss Enemy:  " + str(misscnt) + " × 10 = " + str(miss_temp),(50,110),color="WHITE",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("＋",(300,160),color="WHITE",fontsize=40,fontname="senobi-gothic")        
        screen.draw.text("Health:          " + str(HP) + "      =      " + str(HP_temp),(50,210),color="WHITE",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("－",(300,260),color="WHITE",fontsize=40,fontname="senobi-gothic")        
        screen.draw.text("Get Skill:       " + str(skilcnt) + " × 50 = " + str(skcnt_temp),(50,310),color="WHITE",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("＋",(300,360),color="WHITE",fontsize=40,fontname="senobi-gothic")        
        screen.draw.text("Clear Stage:  " + str(stage -1) + " × 100 = " + str(stcnt_temp),(50,410),color="WHITE",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("÷",(300,460),color="WHITE",fontsize=40,fontname="senobi-gothic")        
        screen.draw.text("Difficulty Point:" + str(difficulty) + "      =      " + str(difficulty),(0,510),color="WHITE",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("＝",(600,220),color="WHITE",fontsize=90,fontname="senobi-gothic")        
        screen.draw.text(str(total),(750,250),color="WHITE",fontsize=40,fontname="senobi-gothic")
        screen.draw.text("__________",(700,280),color="WHITE",fontsize=40)        
        screen.draw.text("Enter または Spaceキーで次へ",(300,550),color="WHITE",fontsize=40,fontname="senobi-gothic")        

    if gamemode == 22:
        lg_bg.draw()
        screen.draw.text("このスコアをランキングに入れますか?",(100,150),color="WHITE",fontsize=40,fontname="senobi-gothic")
        if st_cnt == 1:
            screen.draw.text("はい",(250,300),color="RED",fontsize=55,fontname="senobi-gothic")
        else:
            screen.draw.text("はい",(250,300),color="WHITE",fontsize=50,fontname="senobi-gothic")
        if st_cnt == 2:
            screen.draw.text("いいえ",(450,300),color="RED",fontsize=55,fontname="senobi-gothic")
        else:
            screen.draw.text("いいえ",(450,300),color="WHITE",fontsize=50,fontname="senobi-gothic")

    if gamemode == 1:
        if HP == 0:
            if live == False:
                gamemode = 23
            else:
                live = False
                winsound.PlaySound('heal.wav',winsound.SND_ASYNC)
                HP = 1
        if stage > 6:
            gamemode = 23

    if gamemode == 23:
        if HP == 0:
            if set_flg == False:
                game_co = 1
                screen.draw.text("GAME OVER",(WIDTH / 9,HEIGHT / 2.73),color="WHITE",owidth=1,fontsize=100,fontname="senobi-gothic")
                set_flg = True

        if stage > 6:
            if set_flg == False:
                game_co = 2
                screen.draw.text("GAME CLEAR",(WIDTH / 9,HEIGHT / 2.73),color="WHITE",owidth=1,fontsize=100,fontname="senobi-gothic")
                set_flg = True

def update():
    global gamecount,gamemode,sp_e,misscnt,nowcount,shutcnt,enemy_const,b_s_mode
    global rest,delay,numcnt,dif_cnt,temp,damagetime,charge,chg_time,b_a,sp_back
    global boss_s_cnt,b_one_temp,on_off_flg,boss_delay,mas,attack_cnt,sp,sp_flg
    global bom_delay,b_set,kil_temp,miss_temp,HP_temp,skcnt_temp,stcnt_temp,stcnt_temp
    global total,hitme,stage,difficulty,hit,shield_flg,boss_ani_cnt,boss_not,shield_HP
    cnt_ki_flg = True
    cnt_mi_flg = False
    cnt_st_flg = False
    cnt_sk_flg = False
    cnt_HP_flg = False
    total_flg = False
    next_shot_flg = False
    
    if damagetime > 0:
        damagetime -= 1
    
    if gamemode <= 1 or gamemode == 21:               #ゲーム内スコア加算
        gamecount += 1

    if gamemode >= 2:               #スキル選択画面用スコア加算
        nowcount += 1

    if gamecount >= stage_cl:       #ステージクリア演出
        if HP > 0:
            if stage < 5:
                gamemode = 10
                delay = 10
                nowcount = 0
                gamecount = 0

    if bom_delay > 0:
        bom_delay -= 1

    if gamemode == 1:
        if rest <= 60:              #敵の弾出しと削除
            for enemy in enemys:
                if enemy.x <= -48:
                    enemys.remove(enemy)
                    misscnt += 1
                if enemy.ammo_speed == 0:
                    e_shot = Enemy_Shot()
                    e_shot.x = enemy.x - 35
                    e_shot.y = enemy.y
                    enemy.ammo_speed = enemy.ammo_backup
                    e_shots.append(e_shot)
                if enemy.y >= HEIGHT:
                    enemy.y = HEIGHT - 37
                    
        if damagetime == 0:
            if charge:      #チャージショット
                if keyboard.SPACE:
                    if chg_time < 120:
                        chg_time += 1
                else:
                    if chg_time == 120:
                        missile = Super_Shot("charge_now.png",attack)
                        missile.scale = 1.5
                        missiles.append(missile)
                    chg_time = 0

        for enemy in enemys:        #敵の更新
            enemy.update()

        for e_shot in e_shots:      #敵の弾の更新
            e_shot.update()
            if stage != 5:
                if e_shot.x >= WIDTH + 35:
                    hit = True
                if e_shot.y >= HEIGHT + 35:
                    hit = True
                if e_shot.y < -35:
                    hit = True
                if e_shot.x < -35:
                    hit = True

            if hit:
                e_shots.remove(e_shot)
                hit = False

            if b_s_mode == 2 or b_s_mode == 3:
                e_shot.move_forward(8)

            if b_s_mode == 4:
                e_shot.move_forward(2)

        for missile in missiles:
            missile.update()
            
        if mas:
            for enemy in enemys:
                for missile in missiles:
                    if missile.x >= WIDTH + 24:
                        if missile.random == 1:     #5%の確率
                            missile.point_towards(enemy)
                            missile.assist = True
                        if missile.assist:
                            hitme = False

                    if hitme:
                        missiles.remove(missile)
                        hitme = False

        if gamecount % dif_cnt == 0:
            if stage <= 4:
                if enemy_const:
                    enemy = Enemy()
                    enemys.append(enemy)
                else:
                    numcnt = random.randrange(1,11)
                    if numcnt <= 6:
                        enemy = Enemy()
                        enemys.append(enemy)
                    if numcnt >= 7 and numcnt <= 8:
                        enemy = Enemy("enemy2.png",normal_e_life,1000,2,1)
                        enemys.append(enemy)
                    if numcnt >= 9:
                        enemy = Enemy("enemy3.png",normal_e_life,1000,3,1)
                        enemys.append(enemy)
            
        if rest <= 60:              #移動
            if keyboard.UP == 1:
                if stage == 5:
                    if player.y >= 13:
                        player.y -= sp - 1
                else:
                    if player.y >= 36:
                        player.y -= sp

                
            if keyboard.DOWN == 1:
                if stage == 5:
                    if player.y <= HEIGHT - 16:
                            player.y += sp - 1
                else:
                    if player.y <= HEIGHT - 33:
                        player.y += sp

            if keyboard.RIGHT == 1:
                if stage == 5:
                    if player.x <= WIDTH - 20:
                        player.x += sp - 1
                else:
                    if player.x <= WIDTH - 26:
                        player.x += sp

            if keyboard.LEFT == 1:
                if stage == 5:
                    if player.x > 15:
                        player.x -= sp - 1
                else:
                    if player.x > 30:
                        player.x -= sp

            if keyboard.LSHIFT == 1:
                if sp_flg == False:
                    sp_flg = True
                    sp -= 2
            else:
                sp_flg = False
                sp = sp_back

        if b_s_mode == 5:
            if boss_ani_cnt < 240:
                boss_ani_cnt += 1

    for missile in missiles:
        if hitme:
            missiles.remove(missile)
            hitme = False
              
    if stage == 5:
        player.scale = 0.5
        if boss_delay == 0:
            if b_s_mode == 1:               #ボスの攻撃
                if gamecount % 35 == 0:
                    if attack_cnt < 12:
                        for i in range(0,360,20):   #全方向攻撃
                            if 360 - i >= 0:
                                i -= 360
                            e_shot = Boss_Attack("boss_one.png",i - b_one_temp,280)
                            e_shot.x = boss.x
                            e_shot.y = boss.y
                            e_shot.scale = 2
                            e_shots.append(e_shot)
                        if on_off_flg:
                            b_one_temp += 5
                            if b_one_temp == 20:
                                b_one_temp = 0
                            boss_s_cnt += 1
                            if boss_s_cnt == 8:
                                boss_s_cnt = 0
                                on_off_flg = False
                        else:
                            b_one_temp -= 5
                            if b_one_temp == -20:
                                b_one_temp = 0
                            boss_s_cnt -= 1
                            if boss_s_cnt == -8:
                                boss_s_cnt = 0
                                on_off_flg = True
                                boss_delay = 120
                        attack_cnt += 1
                    else:
                        next_shot_flg = True

            if b_s_mode == 2:
                if gamecount % 30 == 0:    #追尾弾
                    if attack_cnt < 11:
                        target.x = player.x
                        target.y = player.y
                        for i in range(2):
                            e_shot = Boss_Attack("boss_two.png",0,100)
                            e_shot.x = boss.x + (10 * i)
                            e_shot.y = boss.y
                            e_shot.scale = 2
                            e_shot.angle = e_shot.direction_to(target)
                            e_shots.append(e_shot)
                        boss_delay = 10
                        attack_cnt += 1
                    else:
                        next_shot_flg = True

            if b_s_mode == 3:           #常に追尾
                if attack_cnt < 30:
                    if gamecount % 15 == 0:
                        sub1_boss.topleft=(boss.x,boss.y + 100)
                        sub2_boss.topleft=(boss.x,boss.y - 100)
                        e_shot = Boss_Attack("boss_three.png",0,100)
                        e_shot.scale = 1
                        e_shot.x = sub1_boss.x
                        e_shot.y = sub1_boss.y
                        e_shot.angle = e_shot.direction_to(player)
                        e_shots.append(e_shot)
                        e_shot = Boss_Attack("boss_three.png",0,100)
                        e_shot.scale = 1
                        e_shot.x = sub2_boss.x
                        e_shot.y = sub2_boss.y
                        e_shot.angle = e_shot.direction_to(player)
                        e_shots.append(e_shot)
                        attack_cnt += 1
                else:
                    next_shot_flg = True

            if b_s_mode == 4:               #半円形弾幕移動
                if attack_cnt < 8:
                    if b_set:
                        boss.y = 0
                        sub1_boss.y = HEIGHT + 48
                        boss.x = 720
                        sub1_boss.x = boss.x
                        b_set = False
                    if gamecount % 60 == 0:
                        for i in range(-200,-140,15):
                            e_shot = Boss_Attack("boss_one.png",i,390)
                            e_shot.scale = 1
                            e_shot.x = boss.x
                            e_shot.y = boss.y
                            e_shots.append(e_shot)
                        for i in range(-200,-140,15):
                            e_shot = Boss_Attack("boss_one.png",i,390)
                            e_shot.scale = 1
                            e_shot.x = sub1_boss.x
                            e_shot.y = sub1_boss.y
                            e_shots.append(e_shot)
                        attack_cnt += 1
                else:
                    next_shot_flg = True


                boss.y += 3
                sub1_boss.y -= 3

            if b_s_mode == 5:
                if attack_cnt < 480:
                    shield_flg = True
                    attack_cnt += 1
                else:
                    next_shot_flg = True
                
        if boss_HP <= 0:
            Next_Stage()

        for e_shot in e_shots:
            if e_shot.time <= 0:
                e_shots.remove(e_shot)
            
            
        if b_s_mode == 4:
            if boss.y >= HEIGHT + 48:
                b_set = True

        if next_shot_flg:
            if e_shots[:] == []:
                attack_cnt = 0
                target.topleft=(-100,-100)
                sub1_boss.topleft=(-100,-100)
                sub2_boss.topleft=(-100,-100)
                shield.topleft=(-100,-100)
                next_shot_flg = False
                boss.topleft=(random.randrange(8,16) * 48,random.randrange(1,10) * 48)
                if player.x - boss.x <= 48 or player.y - boss.y <= 48:
                    boss.topleft=(random.randrange(8,16) * 48,random.randrange(1,10) * 48)
                b_s_mode = random.randrange(1,6)
                if b_s_mode == 5:
                    if shield_HP > 0:
                        boss_not = True
                    else:
                        boss_not = False
                    boss_ani_cnt = 0
                else:
                    shield.topleft=(-100,-100)
                    boss_not = False
    else:
        if boss.topleft != (-100,-100):
            boss.topleft=(-100,-100)
            sub1_boss.topleft=(-100,-100)
            sub2_boss.topleft=(-100,-100)
            shield.topleft=(-100,-100)

    if delay > 0:
        delay -= 1

    if shutcnt > 0:
        shutcnt -= 1

    if boss_delay > 0:
        boss_delay -= 1

    if shutcnt == 0:
        exit()
                        
    if gamemode == 11 or gamemode == 1:
        if rest > 0:
            rest -= 1

    if gamemode == 21:
        if gamecount % 3 == 0:
            if cnt_ki_flg:
                if kil_temp < killcnt * 10:
                    kil_temp += 1
                    winsound.PlaySound('count.wav',winsound.SND_ASYNC)

                else:
                    cnt_ki_flg = False
                    cnt_mi_flg = True
            if cnt_mi_flg:
                if miss_temp < misscnt * 10:
                    miss_temp += 1
                    winsound.PlaySound('count.wav',winsound.SND_ASYNC)
                else:
                    cnt_mi_flg = False
                    cnt_HP_flg = True

        if cnt_HP_flg:
            if HP_temp <int(( HP / maxHP ) * 100):
                HP_temp += 1
                winsound.PlaySound('count.wav',winsound.SND_ASYNC)
            else:
                cnt_HP_flg = False
                cnt_sk_flg = True

        if cnt_sk_flg:
            if skcnt_temp < skilcnt * 50:
                skcnt_temp += 1
                winsound.PlaySound('count.wav',winsound.SND_ASYNC)
            else:
                cnt_sk_flg = False
                cnt_st_flg = True

        if cnt_st_flg:
            if stcnt_temp < (stage -1) * 100:
                stcnt_temp += 2
                winsound.PlaySound('count.wav',winsound.SND_ASYNC)
            else:
                cnt_st_flg = False
                total_flg = True
        if total_flg:
            if total < int(((kil_temp - miss_temp) + (HP_temp - skcnt_temp) + stcnt_temp) / difficulty):
                if int(((kil_temp - miss_temp) + (HP_temp - skcnt_temp) + stcnt_temp) / difficulty) < 0:
                    total -= 2
                else:
                    total += 2
                winsound.PlaySound('count.wav',winsound.SND_ASYNC)
            else:
                total_flg = False

def on_key_down(key):
    global gamemode,select_sk,bombcnt,shotnum,damagetime,numcnt,sk_se,bgcnt,s_cool_time
    global multis,push_shot_cnt,HP,rest,delay,shutcnt,shutdown_flg,skilcnt
    global st_cnt,st_se,setting_st_cnt,skill_flag,stage,nowcount,push_shot_cnt,charge
    global chg_time,b_s_mode,sp_back,bom_delay,maxHP,normal_e_life,sp_e,e_s_sp
    global kil_temp,miss_temp,HP_temp,skcnt_temp,stcnt_temp,killcnt,stage,i
    global total,none_flg,game_co,difficulty,stage_cl,r,e,boss_HP

    if key == keys.SPACE or key == keys.RETURN:
        if gamemode != 1:
            winsound.PlaySound('en_sp.wav',winsound.SND_ASYNC)
    
    if gamemode == 0:
        if key == keys.SPACE:
            gamemode = 5
            delay = 10
            winsound.PlaySound('enter.wav.',winsound.SND_ASYNC)

    if gamemode == 1:   #ゲームプレイ

        if HP <= -1 or stage == 6:
            if key == keys.SPACE or key == keys.RETURN:
                gamemode = 23

        if bom_delay == 0:
            if key == keys.Z and bombcnt >= 1:  #使用可能なら爆弾を使用する
                winsound.PlaySound('explode.wav.',winsound.SND_ASYNC)
                bom_delay = 10
                bombcnt -= 1
                enemys[:] = []
                e_shots[:] = []

        if key == keys.SPACE:       #自機から弾を発射
            if damagetime == 0:
                if gamecount - push_shot_cnt >= s_cool_time:
                    push_shot_cnt = gamecount
                    for i in range(shotnum):
                        missile = MultiShot("shoot",0,i,attack)
                        missiles.append(missile)
                        if multis == 1:
                            missile = MultiShot("shoot",10,i,attack)
                            missiles.append(missile)
                            missile = MultiShot("shoot",-10,i,attack)
                            missiles.append(missile)
                        
        if key == keys.ESCAPE:  #設定画面へ移行
            if rest == 0:
                st_cnt = 1
                delay = 10
                numcnt = 0
                gamemode = 4
        
    if gamemode == 2:   #スキル選択
        if delay == 0:
            if select_sk == 1:
                if key == keys.RIGHT:
                    winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                    select_sk = 0
            else:
                if key == keys.LEFT:
                    winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                    select_sk = 1
            if key == keys.SPACE or key == keys.RETURN:
                Select_Skill_Enter()

            if key == keys.ESCAPE:
                skil_ch[i] = len(sk_mean)
                i += 1
                Next_Stage()
                skill_flag = True

    if gamemode == 3:
        if delay == 0:
            if key == keys.SPACE or key == keys.RETURN:
                gamemode = 21
                delay = 10
                st_se = 1

    if gamemode == 4:       #設定画面
        if key == keys.UP:
            if st_cnt != 1:
                winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                st_cnt -= 1
        if key == keys.DOWN:
            if st_cnt != 5:
                winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                st_cnt += 1

        if delay == 0:
            if key == keys.ESCAPE:  #設定からゲーム画面へ
                if rest == 0:
                    rest = 240
                    gamemode = 11
                    
        if key == keys.SPACE or key == keys.RETURN:
            if st_cnt == 1:     #ゲームに戻る
                if rest == 0:
                    rest = 240
                    gamemode = 11
                    
            if st_cnt == 2:     #操作方法
                gamemode = 13
                
            if st_cnt == 3:     #再スタート
                Restart()
                gamemode = 5
                delay = 10
                
            if st_cnt == 4:     #スキル説明
                gamemode = 15
                sk_se = 1
                
            if st_cnt == 5:     #シャットダウン
                gamemode = 12
                bgcnt = 0
                shutdown_flg = True
                shutcnt = 300

    if gamemode == 5:       #スタート画面の操作
        if key == keys.UP:
            if st_cnt > 1:
                winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                st_cnt -= 1
        if key == keys.DOWN:
            if st_cnt < 4:
                winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                st_cnt += 1
                
        if delay == 0:
            if key == keys.SPACE or key == keys.RETURN:
                if st_cnt == 1:
                    gamemode = 6
                    delay = 10
                if st_cnt == 2:
                    gamemode = 13
                    sk_se = 1
                    st_se = True
                if st_cnt == 3:
                    delay = 10
                    gamemode = 17
                    with open(u_d,'r',encoding='UTF-8') as f:
                        if f.read() == '':
                            none_flg = True
                
                if st_cnt == 4:
                    gamemode = 12
                    bgcnt = 0
                    shutdown_flg = True
                    shutcnt = 300

    if gamemode == 6:       #スタート開始した後の難易度とスキル有無選択
        if setting_st_cnt == 1:
            if key == keys.UP:
                if st_cnt > 1:
                    winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                    st_cnt -= 1
            if key == keys.DOWN:
                if st_cnt < 4:
                    winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                    st_cnt += 1
                    
            if delay == 0:
                if key == keys.SPACE or key == keys.RETURN:
                    if st_cnt == 1:
                        difficulty = 1.2
                        dif_cnt = 180
                        maxHP = 3
                        normal_e_life = 1
                        setting_st_cnt = 2
                        delay = 10
                    if st_cnt == 2:
                        difficulty = 1.0
                        dif_cnt = 120
                        maxHP = 3
                        normal_e_life = 1
                        st_cnt = 1
                        setting_st_cnt = 2
                        delay = 10
                    if st_cnt == 3:
                        difficulty = 0.8
                        dif_cnt = 120
                        maxHP = 3
                        HP = 3
                        e_s_sp = 4
                        sp_e = 3
                        normal_e_life = 2
                        st_cnt = 1
                        setting_st_cnt = 2
                        delay = 10
                    if st_cnt == 4:
                        difficulty = 0.6
                        dif_cnt = 90
                        maxHP = 2
                        HP = 2
                        sp_e = 4
                        e_s_sp = 5
                        normal_e_life = 2
                        st_cnt = 1
                        setting_st_cnt = 2
                        delay = 10

        if setting_st_cnt == 2:
            if key == keys.UP:
                if st_cnt > 1:
                    winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                    st_cnt -= 1
            if key == keys.DOWN:
                if st_cnt < 2:
                    winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                    st_cnt += 1

            if delay == 0:
                if key == keys.SPACE or key == keys.RETURN:
                    if st_cnt == 1:
                        skill_flag = True
                        gamemode = 1
                        delay = 10
                    if st_cnt == 2:
                        
                        gamemode = 1
                        delay = 10
                        
    if gamemode == 10:      #ステージクリア後のスキル選択移動画面操作
        if delay == 0:
            if key == keys.SPACE or key == keys.RETURN:
                if skill_flag:
                    gamemode = 2
                    Skill_set()
                    delay = 30
                else:
                    Next_Stage()
                        
    if gamemode == 13:      #操作方法画面操作
        if key == keys.ESCAPE:
            if st_se:
                gamemode = 5
                st_se = False
            else:
                delay = 10
                gamemode = 4

    if gamemode == 15:      #スキル説明操作画面
        if key == keys.DOWN:
            if sk_se < 3:
                winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                sk_se += 1
        
        if key == keys.UP:
            if sk_se > 1:
                winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                sk_se -= 1

        if key == keys.ESCAPE:
            delay = 10
            gamemode = 4

    if gamemode == 17:
        if delay == 0:
            if key == keys.ESCAPE:
                delay = 10
                gamemode = 5

    if gamemode == 21:
        if delay == 0:
            if key == keys.SPACE or key == keys.RETURN:
                if kil_temp != killcnt * 10:
                    kil_temp = killcnt * 10
                else:
                    if miss_temp != misscnt * 10:
                        miss_temp = misscnt * 10
                    else:
                        if HP_temp != int(( HP / maxHP ) * 100):
                            HP_temp = int(( HP / maxHP ) * 100)
                        else:
                            if skcnt_temp != skilcnt * 50:
                                skcnt_temp = skilcnt * 50
                            else:
                                if stcnt_temp != (stage -1) * 100:
                                    stcnt_temp = (stage -1) * 100
                                else:
                                    if total != int(((kil_temp - miss_temp) + (HP_temp - skcnt_temp) + stcnt_temp) / difficulty):
                                        total = int(((kil_temp - miss_temp) + (HP_temp - skcnt_temp) + stcnt_temp) / difficulty)
                                    else:
                                        delay = 10
                                        gamemode = 22
                delay = 10

    if gamemode == 22:
        if delay == 0:
            if key == keys.LEFT:
                if st_cnt > 1:
                    winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                    st_cnt -= 1
            if key == keys.RIGHT:
                if st_cnt < 2:
                    winsound.PlaySound('move.wav',winsound.SND_ASYNC)
                    st_cnt += 1
            if key == keys.SPACE or key == keys.RETURN:
                if st_cnt == 1:
                    delay = 10
                    with open(u_d,'a', encoding='UTF-8') as f:
                        f.write(str(total) + "\n")
                    delay = 10
                    Restart()
                    gamemode = 5
                if st_cnt == 2:
                    delay = 10
                    Restart()
                    gamemode = 5
        
                    

    if gamemode == 23:
        if key == keys.SPACE or key == keys.RETURN:
            if game_co == 2:
                gamemode = 3
                delay = 10
            else:
                delay = 10
                gamemode = 3
#デバッグ操作
#    if key == keys.R:
#        r += 1
#        if r == len(sk_mean):
#            r = 0

#    if key == keys.E:
#        e += 1
#        if e == len(sk_mean):
#            e = 0

#    if key == keys.L:
#        Skill_set()
#        gamemode += 1

#    if key == keys.B:
#        boss_HP = 1

#ここから下は宣言------------------------------------------------------------#

class MultiShot(Actor):
    global attack
    def __init__(self,name,angle,i,dmg = 1,re = False,ss = False,assist=False):
        super().__init__(name)
        self.x = player.x + 70 * i
        self.y = player.y
        self.dmg = dmg
        self.angle = angle
        self.re = re
        self.ss = ss
        self.assist = assist
        self.random = random.randrange(1,21)
        self.random_kill = random.randrange(1,11)
    def update(self):
        if self.assist:
            self.move_forward(20)
        else:
            self.x += math.cos(math.radians(self.angle)) * 8
            self.y -= math.sin(math.radians(self.angle)) * 8
        

class Super_Shot(Actor):
    def __init__(self,name = "heart.png",dmg = 1,ss = True):
        super().__init__(name)
        self.x = player.x + 70 * i
        self.y = player.y
        self.dmg = dmg * 2
        self.ss = ss
        self.random = random.randrange(1,6)
        self.random_kill = random.randrange(1,11)
    def update(self):
        self.x += 8

class Refle_Shot(Actor):
    def __init__(self,name = "e_shot.png",dmg = 1,re = True,ss = False):
        super().__init__(name)
        self.re = re
        self.dmg = dmg
        self.ss = ss
    def update(self):
        self.x += 15

class Enemy(Actor):
    global normal_e_life
    def __init__(self,file_name = "enemy.png",life = normal_e_life,ammo_speed = 120,mode = 1,temp = 1,ammo_backup=120):
        super().__init__(file_name)
        self.images = [file_name,'enemy_ani2.png']
        self.life = life
        self.ammo_speed = ammo_speed
        self.ammo_backup = ammo_speed
        self.mode = mode
        self.temp = temp
        self.x = WIDTH + 36
        self.y = 70 * random.randrange(1,10)
    def update(self):
        if self.ammo_speed > 0:
            self.ammo_speed -= 1
        if self.mode == 1:
            self.x -= sp_e
        if self.mode == 2:
            self.temp -= motemp
            self.x -= self.temp * self.temp
        if self.mode == 3:
            self.x -= sp_e
            if  player.x <= self.x:
                self.flip_x = True
                self.point_towards(player)
                self.move_towards(player,thremo)
            else:
                self.flip_x = True
                if player.x - self.x <= 200:
                    self.point_towards(player)
                    self.move_towards(player,thremo)
                else:
                    self.flip_x = False
                    self.angle = 0
                    self.x -= sp_e


class Enemy_Shot(Actor):
    global e_s_sp
    def __init__(self,name = "e_shot.png",re = False):
        super().__init__(name)
        self.x = -70
        self.y = -70
        self.re = re
    def update(self):
        self.x -= e_s_sp

class Boss_Attack(Actor):   #ボスの攻撃
    global b_s_mode
    def __init__(self,name,angle,time = 240):
        super().__init__(name)
        self.angle = angle
        self.time = time
        if b_s_mode == 1 or b_s_mode == 2 or self.scale == 4:
            self.sstage_clcale = 2
    def update(self):
        if b_s_mode == 1:
            self.x += math.cos(math.radians(self.angle)) * 3
            self.y -= math.sin(math.radians(self.angle)) * 3
        if self.time > 0:
            self.time -= 1


def Next_Stage():
    global r_flg,nowcount,stage,bgcnt,dif_cnt,push_shot_cnt,gamemode,b_s_mode,boss_delay
    r_flg = False
    player.scale = 1
    shield.center=(-100,-100)
    boss.topleft=(-100,-100)
    nowcount = 0
    if stage < 6:
        stage += 1
    bgcnt = 0
    dif_cnt /= 1.2
    dif_cnt = int(dif_cnt)
    if dif_cnt <= 0:
        dif_cnt = 1
    missiles[:] =[]
    e_shots[:] =[]
    enemys[:] =[]
    push_shot_cnt = 0
    gamemode = 1
    sounds.bgm_boss.stop()
    sounds.bgm.stop()
    sound_flg = True
    if stage == 5:
        winsound.PlaySound('warning.wav',winsound.SND_ASYNC)
        boss_delay = 240
        b_s_mode = 1
        boss.topleft=(random.randrange(10,16) * 48,random.randrange(1,10) * 48)
        if player.x - boss.x <= 48 or player.y - boss.y <= 48:
            boss.topleft=(random.randrange(10,16) * 48,random.randrange(1,10) * 48)

def Restart():
    global maxHP,HP,sp,sp_back,damhl_time,stage_cl,bombcnt,multis,shotnum,s_cool_time
    global attack,refle,shield,expl,pane,charge,sp_e,normal_e_life,motemp,thremo
    global enemy_const,e_s_sp,boss_HP,killcnt,misscnt,skilcnt,stage,i,r,e,r_flg
    global select_sk,gamecount,nowcount,come_s,dif_cnt,setting_st_cnt,pf,attack_cnt
    global bgcnt,chg_time,b_s_mode,boss_delay,st_cnt,boss_s_cnt,b_a,sp_flg,b_set
    global on_off_flg,mas,damagetime,st_se,skill_flag,shutdown_cnt,game_co,live
    global push_shot_cnt,numcnt,rest,st_cnt,total,hitme,stcnt_temp,sub_HP,HP_atk_flg
    global kil_temp,miss_temp,HP_temp,skcnt_temp,shutcnt,delay,number,skil_ch,sound_flg

    skil_ch=[len(sk_mean),len(sk_mean),len(sk_mean),len(sk_mean)]
    enemys[:] = []
    e_shots[:] = []
    missiles[:] = []
    #ステータス
    maxHP = 3
    HP = maxHP
    sp = 5
    sp_back = sp
    damhl_time = 120
    stage_cl = 1800
    bombcnt = 0
    multis = 0
    shotnum = 1
    s_cool_time = 20
    attack = 1
    refle = False
    p_shield = False
    expl = False
    pane = False
    charge = False
    sub_HP_flg = False
    HP_atk_flg = False
    live = False
    #敵ステータス
    sp_e = 2
    normal_e_life = 2
    motemp = 0.04
    thremo = 4
    enemy_const = False
    e_s_sp = 3

    boss_HP = 100

    #スコア
    killcnt = 0
    misscnt = 0
    skilcnt = 0
    stage = 1

    #スキル選択用宣言
    i = 0
    r = 0
    e = 0
    r_flg = False
    select_sk = 1

    #内部向け宣言
    gamecount = 0
    nowcount = 0
    come_s = 0
    dif_cnt = 180
    setting_st_cnt = 1
    pf = 0
    attack_cnt = 0
    bgcnt = 0
    chg_time = 0
    b_s_mode = 0
    boss_delay = 0
    sk_se = 1
    sk_cnt = 0
    b_one_temp = 0
    bom_delay = 0
    st_cnt = 1
    boss_s_cnt = 0
    b_a = 1
    sp_flg = False
    b_set = True
    on_off_flg = True
    sound_flg = True
    mas = False
    damagetime = 0
    st_se = False
    skill_flag = True
    shutdown_flg = False
    game_co = 0 #クリアかオーバーか確認用

    #仮置き
    push_shot_cnt = 0
    numcnt = 0
    rest = 0
    st_cnt = 1
    total = 0
    hitme = False
    stcnt_temp = 0
    kil_temp = 0
    miss_temp = 0
    HP_temp = 0
    skcnt_temp = 0
    shutcnt = -1
    delay = 0
    sounds.bgm_boss.stop()
    sounds.bgm.stop()
    player.scale = 1
    player.topleft = (0,HEIGHT / 2)
 
def Select_Skill_Enter():
    global i,skilcnt,r,e,r_flg,skil_ch,gamemode,stage
    global select_sk,nowcount,push_shot_cnt,bgcnt
    winsound.PlaySound('get.wav.',winsound.SND_ASYNC)
    bgcnt = 0
    if select_sk == 1:
        skil_ch[i] = r
        Skill_Get()
    else:
        skil_ch[i] = e
        Skill_Get()
    skilcnt += 1
    i += 1
    Next_Stage()

    
def Skill_set():
    global r,e,r_flg
    
    sounds.bgm_boss.stop()
    sounds.bgm.stop()
    if r_flg == False:
        r = random.randrange(0,len(sk_mean))
        e = random.randrange(0,len(sk_mean))
        r_flg = True
        Skill_check()

def Skill_check():
    global r,e,r_flg,maxHP,HP,i

    if maxHP == HP:
        if r == 4:
            r_flg = False
            Skill_set()
        if e == 4:
            r_flg = False
            Skill_set()
    else:
        if maxHP == 5:
            if r == 1:
                r = 0
            if e == 1:
                e = 0

    if r == e:
        r_flg = False
        Skill_set()

    for a in range(i):
        if skil_ch[a] == r or skil_ch[a] == e:
            if skil_ch[a] != 3 and skil_ch[a] != 4:
                r_flg = False
                Skill_set()

def Skill_Get():
    global skil_ch,i,maxHP,HP,damhl_time,sp,stage_cl,attack,thremo,enemy_const
    global bombcnt,sp_e,shotnum,multis,refle,p_shield,expl,motemp,pane,charge,mas
    global sp_back,s_cool_time,sub_HP_flg,HP_atk_flg,live
    temp_HP = maxHP
    
    if skil_ch[i] == 0:
        maxHP += 1
        HP += 1
        
    if skil_ch[i] == 1:
        multis = 1
        s_cool_time *= 3

    if skil_ch[i] == 2:
        shotnum = 2
        s_cool_time *= 2

    if skil_ch[i] == 3:
        damhl_time = 180

    if skil_ch[i] == 4:
        if HP_atk_flg:
            attack -= maxHP - HP
        HP = maxHP

    if skil_ch[i] == 5:
        expl = True

    if skil_ch[i] == 6:
        sp_e = 1
        motemp = 0.02
        thremo = 4

    if skil_ch[i] == 7:
        sp = 8
        sp_back = 8

    if skil_ch[i] == 8:
        pane = True

    if skil_ch[i] == 9:
        stage_cl = 1200

    if skil_ch[i] == 10:
        charge = True

    if skil_ch[i] == 11:
        refle = True
        
    if skil_ch[i] == 12:
        p_shield = True
        
    if skil_ch[i] == 13:
        bombcnt += 1
        
    if skil_ch[i] == 14:
        attack *= 2 

    if skil_ch[i] == 15:
        mas = True

    if skil_ch[i] == 16:
        enemy_const = True

    if skil_ch[i] == 17:
        s_cool_time -= 10

    if skil_ch[i] == 18:
        sub_HP_flg = True

    if skil_ch[i] == 19:
        HP_atk_flg = True
        while temp_HP != HP:
            temp_HP -= 1
            attack += 1

    if skil_ch[i] == 20:
        live = True
            
        
pgzrun.go()
