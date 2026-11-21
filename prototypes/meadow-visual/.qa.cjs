const { chromium } = require(process.env.MAGE_PLAYWRIGHT);
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const fs = require('node:fs');
const assert = require('node:assert/strict');

(async () => {
 const browser = await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--no-sandbox','--disable-gpu']});
 const page = await browser.newPage({viewport:{width:1440,height:960}});
 page.setDefaultTimeout(4500);
 const errors=[];
 page.on('pageerror', e=>errors.push(e.message));
 const target = path.join(__dirname,'mage-next-run-visual.html');
 const shots = path.join(__dirname,'.qa');
 fs.mkdirSync(shots,{recursive:true});
 await page.goto(pathToFileURL(target).href);
 assert.equal(await page.locator('.opening .primary').evaluate(e=>getComputedStyle(e).borderImageWidth),'18px 24px');
 const click = act=>page.locator('[data-act="'+act+'"]').click();
 const jump = scene=>page.locator('[data-scene="'+scene+'"]').click();
 const wait = scene=>page.waitForFunction(scene=>document.querySelector('[aria-current="step"]')?.dataset.scene===scene,scene);
 const drag = async (key,index)=>{
  const source=page.locator('[data-hand="'+key+'"]');
  const target=page.locator('[data-drop-slot="'+index+'"]');
  await source.scrollIntoViewIfNeeded();
  const a=await source.boundingBox(),b=await target.boundingBox();
  await page.mouse.move(a.x+a.width/2,a.y+a.height/2);
  await page.mouse.down();
  await page.mouse.move(a.x+a.width/2,a.y+a.height/2-22,{steps:4});
  await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:8});
  await page.mouse.up();
 };
 const screens=['title','intro','battle','reward','equip','later','trace','retreat','retry','clear','road'];
 for (const scene of screens){
  await jump(scene);
  await page.locator('#game').screenshot({path:path.join(shots,scene+'.png')});
 }
 await jump('battle');
 assert.equal(await page.locator('.shield-art').getAttribute('src'),await page.evaluate(()=>assets['ui-shield-normal']));
 await page.evaluate(()=>{state.hp=2;state.foes=[{x:28,y:72,hp:1},{x:85,y:70,hp:1}];tick()});
 assert.equal(await page.locator('.shield-art').getAttribute('src'),await page.evaluate(()=>assets['ui-shield-hit']));
 await page.waitForFunction(()=>document.querySelector('.shield-art').getAttribute('src')===assets['ui-shield-weak']);
 await jump('title');
 await click('intro');await wait('intro');
 await click('start');await wait('battle');
 for(let i=0;i<3;i++)await click('cast-fire');
 await wait('reward');
 await click('reward-burst');await wait('equip');
 assert.equal(await page.locator('[data-drop-slot]').count(),3);
 assert.equal(await page.locator('[data-hand]').count(),3);
 await drag('burst',0);
 assert.match(await page.locator('.equip-feedback').innerText(),/빈 슬롯/);
 assert.equal(await page.locator('[data-drop-slot="0"] strong').innerText(),'화염탄');
 await drag('burst',1);
 assert.match(await page.locator('.equip-feedback').innerText(),/장착 완료/);
 assert.equal(await page.locator('[data-drop-slot="1"] strong').innerText(),'마력 폭발');
 assert.equal(await page.locator('[data-hand]:disabled').count(),3);
 await click('next');await wait('later');
 await click('cast-burst');await wait('trace');
 const star=page.locator('#star');await star.focus();
 for(const key of ['1','2','3','4','5','1'])await star.press(key);
 await wait('later');
 await page.waitForFunction(()=>document.querySelector('.hud-box strong')?.textContent.includes('3 / 5'));
 await click('demo-retreat');await wait('retreat');
 await click('buy-ward');
 assert.match(await page.locator('.retreat-dock').innerText(),/잔재 7/);
 await click('retry');await wait('retry');
 assert.equal(await page.locator('.shield-count strong').innerText(),'6/6');
 assert.equal(await page.locator('.card.empty').count(),2);
 await jump('later');
 await click('demo-clear');await wait('clear');await click('road');await wait('road');await click('continue');
 assert.equal(await page.locator('.story h2').innerText(),'오솔길');
 await jump('later');
 for (let wave=2;wave<=5;wave++){
  await page.waitForFunction(wave=>document.querySelector('.hud-box strong')?.textContent.includes(wave+' / 5'),wave);
  await click('cast-burst');await wait('trace');
  const box=await star.boundingBox();
  const nodes=[[180,36],[226,185],[101,92],[259,92],[134,185],[180,36]];
  for (const [i,[x,y]] of nodes.entries()){
   await page.mouse.move(box.x+box.width*x/360,box.y+box.height*y/246,{steps:i===0?1:8});
   if(i===0)await page.mouse.down();
  }
  await page.mouse.up();
 }
 await wait('clear');
 await jump('equip');
 await drag('fire',0);
 assert.match(await page.locator('.equip-feedback').innerText(),/합치기 완료.*Lv. 2/);
 assert.equal(await page.locator('[data-drop-slot="0"] small').innerText(),'Lv. 2');
 await jump('equip');
 await page.locator('[data-hand="lightning"]').press('Enter');
 await page.locator('[data-drop-slot="2"]').press('Enter');
 assert.equal(await page.locator('[data-drop-slot="2"] strong').innerText(),'연쇄 번개');
 await page.setViewportSize({width:390,height:844});
 await jump('title');
 assert.equal(await page.locator('.opening .primary').evaluate(e=>getComputedStyle(e).borderImageWidth),'6px 8px');
 for(const scene of screens){
  await jump(scene);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),390,scene);
 }
 await jump('equip');
 await page.screenshot({path:path.join(shots,'mobile.png'),fullPage:true});
 const track=page.locator('.hand-track');
 const rect=await track.boundingBox();
 await page.mouse.move(rect.x+rect.width*.85,rect.y+rect.height*.5);
 await page.mouse.down();
 await page.mouse.move(rect.x+rect.width*.2,rect.y+rect.height*.5,{steps:12});
 await page.mouse.up();
 await page.waitForFunction(()=>document.querySelector('.hand-track').scrollLeft>30);
 assert.equal(await page.locator('[data-hand][aria-pressed="true"]').count(),0);
 const touchPage=await browser.newPage({viewport:{width:390,height:844},hasTouch:true,isMobile:true});
 await touchPage.goto(pathToFileURL(target).href);
 await touchPage.locator('[data-scene="equip"]').tap();
 await touchPage.locator('.equip-stack').scrollIntoViewIfNeeded();
 const touch=await touchPage.context().newCDPSession(touchPage);
 const swipeBox=await touchPage.locator('.hand-track').boundingBox();
 async function swipe(from,to){
  await touch.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:from.x,y:from.y}]});
  for(const f of [.15,.35,.6,.85,1])await touch.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:from.x+(to.x-from.x)*f,y:from.y+(to.y-from.y)*f}]});
  await touch.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 }
 await swipe({x:swipeBox.x+swipeBox.width*.85,y:swipeBox.y+swipeBox.height*.5},{x:swipeBox.x+swipeBox.width*.2,y:swipeBox.y+swipeBox.height*.5});
 await touchPage.waitForFunction(()=>document.querySelector('.hand-track').scrollLeft>30);
 const spell=await touchPage.locator('[data-hand="burst"]').boundingBox();
 const slot=await touchPage.locator('[data-drop-slot="1"]').boundingBox();
 const from={x:spell.x+spell.width/2,y:spell.y+spell.height/2};
 const to={x:slot.x+slot.width/2,y:slot.y+slot.height/2};
 await swipe(from,to);
 await touchPage.waitForFunction(()=>document.querySelector('[data-drop-slot="1"] strong').textContent==='마력 폭발');
 assert.deepEqual(errors,[]);
 console.log('11 screens rendered; drag equip, same-card merge, invalid drop, keyboard, mouse and touch swipe, touch equip, tracing and game-flow checks passed');
 await browser.close();
})().catch(error=>{console.error(error);process.exit(1)});

