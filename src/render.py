"""Render original 1080p / 24 fps teaching animation, with burned-in captions.

No generative image/video model is used. Frames are deterministic vector drawings
and the separately credited research photograph. S–N values and crack counters
are illustrative, not experimental data or a fatigue-life prediction.
"""
import argparse, json, math, subprocess, sys, time, uuid
from pathlib import Path
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from lesson import SCENES

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'; OUT=ROOT/'output'
W,H,FPS=1920,1080,24
BG='#F3F5F2'; INK='#142C39'; MUTED='#596B73'; GRID='#D8E1DF'
TEAL='#007F83'; RED='#D94C43'; GOLD='#AD7419'; BLUE='#2366AD'; WHITE='#FFFFFF'
PALE='#E5EEEC'; ORANGE='#C87332'
TIMELINE=json.loads((ASSETS/'timeline.json').read_text())
Q={c['id']:c for c in TIMELINE}
PHOTO=Image.open(ASSETS/'bolt-fatigue-fracture.jpg').convert('RGB')

@lru_cache(None)
def font(size,bold=False,mono=False):
    name='DejaVuSansMono.ttf' if mono else ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')
    return ImageFont.truetype(str(ASSETS/'fonts'/name),int(size))

def clamp(x):return max(0.,min(1.,x))
def ease(x):x=clamp(x);return x*x*(3-2*x)
def phase(t,start,duration):return ease((t-start)/max(.01,duration))

class Canvas:
    def __init__(self):self.im=Image.new('RGB',(W,H),BG);self.d=ImageDraw.Draw(self.im)
    def text(self,x,y,s,size=32,color=INK,bold=False,anchor=None,mono=False):
        self.d.text((x,y),s,font=font(size,bold,mono),fill=color,anchor=anchor,spacing=10)
    def lines(self,x,y,ls,size=32,color=INK,bold=False,step=None):
        for i,s in enumerate(ls):self.text(x,y+i*(step or size*1.38),s,size,color,bold)
    def line(self,pts,color=INK,width=3):self.d.line(pts,fill=color,width=width,joint='curve')
    def rr(self,box,fill=WHITE,outline=None,r=22,width=2):self.d.rounded_rectangle(box,r,fill,outline,width)
    def circle(self,x,y,r,fill,outline=None,width=2):self.d.ellipse((x-r,y-r,x+r,y+r),fill,outline,width)
    def arrow(self,x1,y1,x2,y2,color=TEAL,width=7,head=17,both=False):
        self.line([(x1,y1),(x2,y2)],color,width)
        theta=math.atan2(y2-y1,x2-x1)
        def tip(x,y,a):self.d.polygon([(x,y),(x-head*math.cos(a-.48),y-head*math.sin(a-.48)),(x-head*math.cos(a+.48),y-head*math.sin(a+.48))],fill=color)
        tip(x2,y2,theta)
        if both:tip(x1,y1,theta+math.pi)
    def dashed(self,p1,p2,color=MUTED,width=3,dash=13):
        x,y=p1;dx=p2[0]-x;dy=p2[1]-y;length=math.hypot(dx,dy)
        if length<.1:return
        for s in np.arange(0,length,dash*2):
            e=min(s+dash,length);self.line([(x+dx*s/length,y+dy*s/length),(x+dx*e/length,y+dy*e/length)],color,width)
    def pill(self,x,y,s,color=TEAL,size=27,fill=WHITE):
        tw=self.d.textlength(s,font=font(size,True));self.rr((x,y,x+tw+34,y+size+22),fill,r=12)
        self.text(x+17,y+8,s,size,color,True)
    def symbol(self,x,y,base='K',sub='I',size=58,color=INK):
        self.text(x,y,base,size,color)
        dx=self.d.textlength(base,font=font(size));self.text(x+dx,y+size*.45,sub,int(size*.5),color)
        return dx+self.d.textlength(sub,font=font(int(size*.5)))+6

def header(c,sc,t):
    s,e,num,title,sub=SCENES[sc]
    c.text(85,42,'MATERIALS SCIENCE  /  ENGINEERING EXPLAINED',25,MUTED,True)
    c.text(1835,42,f'{num} / 07',25,MUTED,anchor='ra')
    c.line([(85,85),(1835,85)],GRID,2)
    c.text(85,110,title+(':' if sc==0 else ''),60 if sc!=4 else 54,INK,True)
    c.text(89,192,sub,38 if sc==0 else 31,MUTED)
    c.d.rectangle((0,1068,W,1080),fill=GRID)
    c.d.rectangle((0,1068,int(W*t/180),1080),fill=TEAL)

def foot(c,text):c.text(88,898,text,24,MUTED)

def captions(c,t):
    cue=next((x for x in TIMELINE if x['start']<=t<x['end']),None)
    if not cue:return
    lines=cue['caption'].splitlines()
    assert len(lines)<=2
    f=40
    while max(c.d.textlength(s,font=font(f)) for s in lines)>1740:f-=1
    top=947 if len(lines)==2 else 967
    c.rr((64,934,1856,1052),INK,r=17)
    for i,s in enumerate(lines):c.text(W/2,top+i*47,s,f,WHITE,anchor='ma')

def specimen(c,cx,cy,w=480,h=330,a=.0,load=.6,split=0,dim=True,ligament=False,small=False):
    """Single edge crack; a is a fraction of width, loaded normal to crack plane."""
    x=cx-w/2;y=cy-h/2;right=x+w;tip=x+w*min(a,1)
    shade='#A8B6BD';edge='#647C89';grip='#8195A1'
    if split<=0:
        c.rr((x,y,right,y+h),shade,edge,r=10,width=3)
        # subtle longitudinal material texture, no photographic simulation
        for xx in np.arange(x+15,right,32):c.line([(xx,y+4),(xx,y+h-4)],'#AFBCC3',1)
        c.rr((x-13,y-4,right+13,y+39),grip,r=6)
        c.rr((x-13,y+h-39,right+13,y+h+4),grip,r=6)
        if a>0:
            op=(4+14*load)*(.6+min(a,.6))
            c.d.polygon([(x-2,cy-op),(tip,cy),(x-2,cy+op)],fill=BG)
            c.line([(x,cy-op),(tip,cy),(x,cy+op)],RED,5 if small else 7)
            c.circle(tip,cy,7 if small else 10,RED)
        if a>0 and dim:
            yy=cy-65
            c.line([(x,yy-10),(x,cy-20)],RED,2);c.line([(tip,yy-10),(tip,cy-17)],RED,2)
            c.arrow(x,yy,tip,yy,RED,3,12,True)
            c.text((x+tip)/2,yy-45,'a',34,RED,True,anchor='ma')
        if ligament and a>0 and a<.95:
            c.line([(tip+12,cy+40),(right-3,cy+40)],TEAL,6)
            c.text((tip+right)/2,cy+52,'Intact section',24,TEAL,anchor='ma')
    else:
        shift=split*50
        zig=[(x,cy-4),(x+w*.18,cy+2),(x+w*.34,cy-5),(x+w*.51,cy+5),(x+w*.73,cy-4),(right,cy+3)]
        top=[(x,y-shift),(right,y-shift)]+[(xx,yy-shift) for xx,yy in reversed(zig)]
        bot=[(xx,yy+shift) for xx,yy in zig]+[(right,y+h+shift),(x,y+h+shift)]
        c.d.polygon(top,fill=shade,outline=edge);c.d.polygon(bot,fill=shade,outline=edge)
        c.line([(xx,yy-shift) for xx,yy in zig],RED,6);c.line([(xx,yy+shift) for xx,yy in zig],RED,6)
        c.rr((x-13,y-4-shift,right+13,y+35-shift),grip,r=6)
        c.rr((x-13,y+h-35+shift,right+13,y+h+4+shift),grip,r=6)
    length=42+65*load;offset=split*50
    for ax in [cx-w*.28,cx,cx+w*.28]:
        c.arrow(ax,y-10-offset,ax,y-10-length-offset,TEAL,6,16)
        c.arrow(ax,y+h+10+offset,ax,y+h+10+length+offset,TEAL,6,16)
    return x,tip,right

def waveform(c,x,y,w,h,t,label=True,cycles=2):
    c.line([(x,y+h),(x+w,y+h)],GRID,2)
    pts=[(x+i*w/120,y+h/2-math.sin(i/120*2*cycles*math.pi-t*2.8)*h*.35) for i in range(121)]
    c.line(pts,TEAL,5)
    if label:c.text(x,y+h+15,'Time →',25,MUTED)

def intro(c,t):
    u=t
    c.text(100,312,'ONE LOAD',26,TEAL,True)
    c.lines(100,358,['Below the breaking load.', 'Repeated thousands', 'or millions of times.'],43,INK,step=60)
    waveform(c,115,590,630,115,t)
    c.pill(105,785,'Damage can accumulate',TEAL,30,PALE)
    load=.25+.75*(.5+.5*math.sin(t*4))
    specimen(c,1335,555,w=490,h=330,a=.0,load=load,dim=False)
    c.text(1335,825,'Repeated tensile loading',32,TEAL,True,anchor='ma')
    foot(c,'Schematic — not to scale   •   Teaching source: UNSW Sydney / Fatigue failure')

def photo(c,t):
    # Original image is unaltered apart from resizing. No failure zones are inferred.
    p=PHOTO.resize((720,629),Image.Resampling.LANCZOS)
    c.im.paste(p,(95,252))
    c.pill(115,267,'Real specimen photograph',INK,27)
    c.text(906,282,'Published evidence',35,TEAL,True)
    c.lines(906,344,['Fractured high-strength bolt', 'Wang Hui-li & Qin Si-feng · 2014'],29,INK)
    c.arrow(880,465,686,465,INK,4,16)
    c.text(904,443,'Fracture surface',33,INK,True)
    if t>=Q['root']['start']:
        c.lines(906,525,['Thread roots can concentrate stress.'],31,INK)
    if t>=Q['unmapped']['start']:
        c.rr((893,591,1810,680),PALE,r=15)
        c.text(915,615,'Exact crack origin is not mapped in the source.',29,MUTED)
    if t>=Q['surfaces']['start']:
        c.lines(906,715,['General tendency — appearance varies:', 'smoother growth / rougher final fracture'],30,INK)
    foot(c,'Photo: Figure 2, doi:10.1155/2014/567318   •   CC BY 3.0 (original article)   •   Resized for display')

def crack(c,t):
    start=Q['initiation']['start'];gstart=Q['growth']['start'];fstart=Q['fracture']['start']
    birth=phase(t,start+1,3)
    growth=phase(t,gstart,max(3,fstart-gstart))
    fast=phase(t,fstart+1.7,.36)
    a=.035*birth+.66*growth
    load=.2+.8*(.5+.5*math.sin((t-35)*4.5))
    split=phase(t,fstart+2.06,.6)
    if fast>0:a=a+(1-a)*fast
    stage=0 if t<gstart else (1 if t<fstart+1.7 else 2)
    stages=['Crack initiation','Crack propagation','Final fracture']
    for i,name in enumerate(stages):
        y=310+i*170;active=i==stage
        c.circle(130,y+31,29,RED if active else GRID)
        c.text(130,y+10,str(i+1),30,WHITE if active else MUTED,True,anchor='ma')
        c.text(181,y,name,34,INK if active else MUTED,active)
        sub=['A scratch raises local stress.', 'Many cycles. Gradual extension.', 'Rapid, unstable extension.'][i]
        c.text(183,y+57,sub,26,MUTED)
    specimen(c,1275,559,w=550,h=340,a=a,load=load,split=split,ligament=True)
    n=int(100+120000*growth)
    c.rr((95,802,775,878),WHITE,r=16)
    c.text(121,820,f'N = {n:,} cycles',31,INK,mono=True)
    if stage==0:
        c.circle(1000,559,34,None,RED,3)
        c.text(850,656,'Surface scratch',27,RED,True)
        c.arrow(989,646,1000,601,RED,3,11)
    foot(c,'Schematic — not to scale   •   Cycle count and growth speed are illustrative, not test results')

def sn(c,t):
    x0,x1,y0,y1=205,1270,793,305
    X=lambda logn:x0+(logn-3)/5*(x1-x0)
    Y=lambda s:y0-s/400*(y0-y1)
    c.text(206,249,'Stress amplitude, S (MPa)',33,INK,True)
    for s in [0,100,200,300,400]:
        yy=Y(s);c.line([(x0,yy),(x1,yy)],GRID,2);c.text(x0-22,yy,str(s),29,MUTED,anchor='rm')
    for i,lab in enumerate(['10³','10⁴','10⁵','10⁶','10⁷','10⁸']):
        xx=X(i+3);c.line([(xx,y1),(xx,y0+9)],GRID,2);c.text(xx,y0+18,lab,31,MUTED,anchor='ma')
    c.arrow(x0,y0,x0,y1-12,INK,4,14);c.arrow(x0,y0,x1+15,y0,INK,4,14)
    c.text((x0+x1)/2,850,'Cycles to failure, N  (log scale)',33,INK,True,anchor='ma')
    steel=lambda x:max(180,480-45*x)
    rev=phase(t,65.5,3.3)
    xs=np.linspace(3,3+5*rev,max(2,int(150*rev)))
    c.line([(X(x),Y(steel(x))) for x in xs],BLUE,7)
    c.rr((1370,255,1825,872),WHITE,r=22)
    c.text(1395,280,'ONE STRESS CYCLE',25,TEAL,True)
    wx,wy,ww,wh=1410,354,345,120
    waveform(c,wx,wy,ww,wh,0,False,cycles=1)
    c.dashed((wx,wy+wh*.15),(wx+ww,wy+wh*.15),MUTED,2)
    c.dashed((wx,wy+wh*.85),(wx+ww,wy+wh*.85),MUTED,2)
    c.text(wx,wy-35,'maximum stress',24,MUTED)
    c.text(wx,wy+wh+1,'minimum stress',24,MUTED)
    c.dashed((wx,wy+wh*.5),(wx+ww,wy+wh*.5),GRID,2)
    c.arrow(1786,wy+wh*.15,1786,wy+wh*.5,GOLD,3,10,True)
    c.text(1796,wy+wh*.23,'S',23,GOLD,True)
    c.lines(1395,524,['S = (max stress −', '      min stress) / 2'],28,INK,step=39)
    rs=Q['sn_read']['start'];rd=Q['sn_read']['end']-rs
    def guides(logn,s,color,amount,label):
        xx,yy=X(logn),Y(s)
        hp=clamp(amount*2);vp=clamp(amount*2-1)
        if hp>0:c.dashed((x0,yy),(x0+(xx-x0)*hp,yy),color,4)
        if vp>0:c.dashed((xx,yy),(xx,yy+(y0-yy)*vp),color,4)
        if hp<1:c.circle(x0+(xx-x0)*hp,yy,10,color)
        elif vp<1:c.circle(xx,yy+(y0-yy)*vp,10,color)
        else:
            c.circle(xx,yy,11,color);c.circle(xx,yy,4,WHITE)
            c.pill(xx+16,yy-43,label,color,25)
    if t>=rs:
        amt=phase(t,rs,rd*.88);guides(4,300,BLUE,amt,'A')
        c.text(1395,648,'A   300 MPa → 10⁴',28,BLUE,True)
    if t>=Q['lower']['start']:
        amt=phase(t,Q['lower']['start'],2.8);guides(6,210,TEAL,amt,'B')
        c.text(1395,695,'B   210 MPa → 10⁶',28,TEAL,True)
        c.text(1395,750,'Lower S → longer life',26,INK,True)
    if t>=Q['scatter']['start']:
        for lx,off in [(3.7,14),(4.2,-18),(4.8,16),(5.4,-14),(5.8,12)]:
            c.circle(X(lx),Y(steel(lx)+off),5,MUTED)
        c.text(520,340,'Illustrative scatter',25,MUTED)
    if t>=Q['steel']['start']:
        c.line([(X(6.67),Y(180)),(X(8),Y(180))],BLUE,10)
        c.text(923,475,'Some steels: fatigue limit',23,BLUE,True)
        c.arrow(1120,512,1120,Y(180)-9,BLUE,3,12)
    if t>=Q['aluminum']['start']:
        p=phase(t,Q['aluminum']['start'],1.5)
        xs=np.linspace(3,3+5*p,110)
        c.line([(X(x),Y(325-46*(x-3))) for x in xs],ORANGE,6)
        c.text(970,718,'Aluminum: no plateau',25,ORANGE,True)
    foot(c,'Illustrative curves — not design data   •   Same material / conditions for A vs B   •   help.solidworks.com')

def kformula(c):
    x=105;y=252
    x+=c.symbol(x,y,'K','I',65,INK)
    c.text(x,y,' = Y × σ × √(π × a)',65,INK)
    c.rr((1450,252,1830,333),PALE,r=16)
    c.text(1475,268,'K units: MPa√m',32,TEAL,True)

def gauge(c,x,y,w,value,label='K_I',critical=False):
    c.rr((x,y,x+w,y+30),GRID,r=8)
    c.rr((x,y,x+w*clamp(value),y+30),RED if critical else TEAL,r=8)
    c.line([(x+w*.87,y-12),(x+w*.87,y+47)],GOLD,5)
    c.symbol(x+w*.87-30,y-59,'K','Ic',38,GOLD)
    c.text(x,y+49,'Qualitative indicator',24,MUTED)

def toughness(c,t):
    kformula(c)
    cmp=Q['compare']['start'];crit=Q['critical']['start'];sub=Q['subcritical']['start']
    a=.22;load=.40;split=0
    if cmp<=t<cmp+2.0:load=.25+.7*phase(t,cmp,1.8)
    elif cmp+2.0<=t<crit:
        a=.22+.31*phase(t,cmp+2.0,2.7);load=.6
    elif t>=crit:
        a=.53+.15*phase(t,crit,5.0);load=.6
        split=phase(t,crit+5.1,.5)
    if t>=sub:a=.39;load=.45;split=0
    specimen(c,480,600,w=475,h=220,a=a,load=load,split=split,dim=True)
    c.text(480,854,'a = edge-to-tip crack length' if split==0 else 'Rapid separation',28,RED,True,anchor='ma')
    c.rr((885,364,1828,859),WHITE,r=22)
    if t<cmp:
        items=[('K_I','Mode I: opening / crack-tip loading'),('Y','Geometry factor (dimensionless)'),('σ','Applied tensile stress · MPa'),('a','Edge to crack tip · meters')]
        for i,(sym,desc) in enumerate(items):
            yy=398+i*90
            if sym=='K_I':c.symbol(918,yy,'K','I',42,TEAL)
            else:c.text(918,yy,sym,42,RED if sym=='a' else TEAL,True)
            c.text(1011,yy+8,desc,29,INK)
    elif t<cmp+2.0:
        c.text(921,405,'1  Keep crack size fixed',35,INK,True)
        c.text(921,478,'Raise stress σ',40,TEAL,True)
        c.arrow(1305,487,1395,487,TEAL,5,16)
        c.symbol(1440,470,'K','I',48,TEAL);c.text(1525,480,'increases',32,TEAL)
        gauge(c,927,651,800,.30+.45*phase(t,cmp,1.8))
    elif t<crit:
        c.text(921,405,'2  Keep applied stress fixed',35,INK,True)
        c.text(921,478,'Lengthen crack a',40,RED,True)
        c.arrow(1330,487,1400,487,RED,5,16)
        c.symbol(1440,470,'K','I',48,RED);c.text(1525,480,'increases',32,RED)
        gauge(c,927,651,800,.37+.42*phase(t,cmp+2.0,2.7))
        if t>=Q['kic']['start']:
            c.text(921,790,'K_Ic: material plane-strain fracture toughness',28,GOLD,True)
    elif t<sub:
        c.text(921,405,'Critical condition',38,RED,True)
        c.symbol(922,475,'K','I, max',51,TEAL);c.text(1085,476,'→',53,INK);c.symbol(1160,475,'K','Ic',51,GOLD)
        c.text(1290,490,'Rapid fracture',30,RED,True)
        gauge(c,927,623,800,.69+.19*phase(t,crit,5),critical=t>crit+5)
        c.lines(925,738,['Linear-elastic fracture mechanics', '+ valid plane-strain conditions'],28,MUTED,step=40)
        c.text(925,821,'Thickness constrains out-of-plane strain.',23,MUTED)
    else:
        c.text(922,405,'Before the final break',36,INK,True)
        c.symbol(922,490,'K','I, max',52,TEAL);c.text(1085,491,'<',52,INK);c.symbol(1160,490,'K','Ic',52,GOLD)
        c.lines(923,608,['Fatigue crack growth can still occur.', 'K_Ic is not a fatigue-growth threshold.'],32,RED,True,step=55)
    foot(c,'Schematic — not to scale   •   Geometry factor Y changes with configuration   •   UNSW Sydney / ASTM E399-24')

def recap(c,t):
    eng=Q['engineering']['start']
    if t<eng:
        labels=['Repeated loading','Crack initiation','Crack growth','Critical condition','Final fracture']
        durations=[0,2.1,4.0,6.5,8.0]
        for i,label in enumerate(labels):
            xx=87+i*356
            active=t-140>=durations[i]
            c.rr((xx,276,xx+325,354),TEAL if active and i<4 else (RED if active else WHITE),r=13)
            c.text(xx+162,300,label,25,WHITE if active else MUTED,True,anchor='ma')
            if i<4:c.arrow(xx+331,314,xx+350,314,MUTED,3,9)
        progress=phase(t,140,8);final=phase(t,148,.5)
        specimen(c,450,620,w=390,h=200,a=.05+.65*progress,load=.45+.4*math.sin(t*3)**2,split=final,dim=False,small=True)
        data=[('recap1',['Repeated loading','can cause fatigue damage.']),('recap2',['S–N curves connect','stress amplitude and fatigue life.']),('recap3',['Fracture toughness helps assess','when an existing crack is critical.'])]
        for i,(key,lines) in enumerate(data):
            if t>=Q[key]['start']:
                yy=432+i*132
                c.text(823,yy,f'0{i+1}',29,TEAL,True)
                c.lines(901,yy,lines,31,INK,step=42)
    else:
        c.text(96,277,'Reduce the risk',47,TEAL,True)
        cards=[(95,'Reduce stress concentrations','Use smoother transitions.'),(695,'Improve surface condition','Limit scratches and defects.'),(1295,'Inspect for cracks','Find damage before it grows.')]
        for i,(xx,title,sub) in enumerate(cards):
            c.rr((xx,365,xx+530,828),WHITE,r=25)
            if i==0:
                c.line([(xx+90,579),(xx+225,579),(xx+225,480),(xx+440,480)],RED,12)
                c.line([(xx+90,635),(xx+185,635)],TEAL,12)
                pts=[(xx+185+100*math.sin(a),635-100*(1-math.cos(a))) for a in np.linspace(0,math.pi/2,50)]
                c.line(pts,TEAL,12);c.line([(xx+285,535),(xx+440,535)],TEAL,12)
            elif i==1:
                c.line([(xx+80,530),(xx+200,530),(xx+223,555),(xx+245,530),(xx+455,530)],RED,10)
                c.line([(xx+80,620),(xx+455,620)],TEAL,11)
                c.arrow(xx+275,555,xx+275,599,TEAL,5,13)
            else:
                c.circle(xx+260,535,85,None,TEAL,11)
                c.line([(xx+320,600),(xx+410,690)],TEAL,17)
                c.line([(xx+198,550),(xx+240,530),(xx+270,558),(xx+309,512)],RED,7)
            c.text(xx+265,705,title,27,INK,True,anchor='ma')
            c.text(xx+265,754,sub,26,MUTED,anchor='ma')
    foot(c,'Repeated loading → initiation → growth → critical condition → fracture   •   Original teaching animation')

def credits(c,t):
    c.rr((85,261,942,875),WHITE,r=22);c.rr((976,261,1835,875),WHITE,r=22)
    c.text(118,285,'TEACHING REFERENCES',27,TEAL,True)
    c.lines(118,343,['UNSW Sydney', 'Fatigue failure · Fracture toughness', 'unsw.edu.au'],29,INK,step=43)
    c.lines(118,499,['SOLIDWORKS Help', 'Stress–Life Cycle (S–N) Curve', 'help.solidworks.com'],29,INK,step=43)
    c.lines(118,655,['ASTM E399-24', 'Linear-elastic plane-strain toughness', 'store.astm.org'],29,INK,step=43)
    c.text(1010,285,'REAL PHOTOGRAPH',27,TEAL,True)
    c.lines(1010,341,['Wang Hui-li & Qin Si-feng (2014)', 'High-Strength Bolt Corrosion Fatigue', 'Life Model and Application · Figure 2', 'doi:10.1155/2014/567318'],28,INK,step=43)
    c.lines(1010,535,['CC BY 3.0 · original article license', 'Resized; exact origin not annotated.', 'creativecommons.org/licenses/by/3.0/'],25,MUTED,step=39)
    c.text(1010,687,'PRODUCTION',27,TEAL,True)
    c.lines(1010,736,['Python · Pillow · FFmpeg', 'Kokoro-82M neural voice · af_heart'],27,INK,step=43)
    foot(c,'Complete source URLs, attribution, prompts, bilingual narration and runnable code are included in the companion files.')

DRAW=[intro,photo,crack,sn,toughness,recap,credits]

def frame(t):
    sc=next(i for i,(s,e,*_) in enumerate(SCENES) if s<=t<e)
    c=Canvas();header(c,sc,t);DRAW[sc](c,t);captions(c,t)
    return c.im

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stills',action='store_true');ap.add_argument('--silent',action='store_true');ap.add_argument('--output',default='Fatigue_Failure.mp4');args=ap.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.stills:
        dest=OUT/'qa_frames';dest.mkdir(exist_ok=True)
        for t in [3,12,21,32,39,48,56,62,69,79,86,94,102,109,118,123,129,136,139,145,154,162,168,177]:
            frame(t).save(dest/f'{t:03}.png')
        print('Saved QA frames');return
    output=OUT/args.output
    temp_output=output.with_name(output.stem+'.rendering.'+uuid.uuid4().hex[:8]+'.mp4')
    cmd=['ffmpeg','-y','-loglevel','warning','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-']
    if not args.silent:cmd+=['-i',str(ASSETS/'narration.wav')]
    cmd+=['-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','4']
    if not args.silent:cmd+=['-af','loudnorm=I=-16:TP=-1.5:LRA=7','-c:a','aac','-b:a','160k','-ar','48000']
    cmd+=['-t','180','-movflags','+faststart','-metadata','title=Fatigue Failure: From Small Cracks to Sudden Fracture',str(temp_output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    started=time.time()
    try:
        for n in range(180*FPS):
            im=frame(n/FPS);proc.stdin.write(im.tobytes())
            if n%(FPS*10)==0:print(f'Render {n/FPS:5.1f}/180 s · wall {time.time()-started:.1f}s',flush=True)
        proc.stdin.close()
        if proc.wait()!=0:raise RuntimeError('FFmpeg failed')
        temp_output.replace(output)
    except BaseException:
        proc.kill();raise
    print(output,flush=True)

if __name__=='__main__':main()
