"""python _src/shots.py 1440|390 -> zrzuty podstron (full page) do _src/sh"""
import sys, os
from playwright.sync_api import sync_playwright
w=int(sys.argv[1]);h=900 if w>800 else 844
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'sh');os.makedirs(OUT,exist_ok=True)
P=['','przejazdy/','lotnisko/','o-nas/','kontakt/']
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':w,'height':h},is_mobile=w<800,has_touch=w<800)
    pg=ctx.new_page();errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    for path in P:
        pg.goto('http://127.0.0.1:8125/taxi-sycow-prusiko/'+path+'?team=1',wait_until='networkidle')
        pg.wait_for_timeout(3500)
        pg.evaluate("document.querySelectorAll('.mapa').forEach(m=>m.scrollIntoView())");pg.wait_for_timeout(2600);pg.evaluate('scrollTo(0,0)');pg.wait_for_timeout(300)
        n=(path.strip('/') or 'home')
        pg.screenshot(path=f'{OUT}/{w}_{n}_top.png')
        pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))")
        pg.wait_for_timeout(900)
        pg.screenshot(path=f'{OUT}/{w}_{n}.png',full_page=True)
    print('ERR',errs)
