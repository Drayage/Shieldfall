const CACHE_NAME='shieldfall-v7';
const CARD_IDS=[
  'basic_attack','ambush','mid_attack','heavy_attack','mana_burst','shield_swap','rage_strike','backs_to_wall','finisher',
  'time_bomb','long_bomb1','long_bomb2','mid_bomb','big_bomb','persistent_shot','decay_persistent','growth_persistent','erosion_persistent','ultimate_persistent',
  'lowcost_guard','pre_guard','react_guard','react_guard_big','stance1','stance2','use_tax','delay_guard','persistent_attach','sac_attack','sac_guard',
  'dismantle','mass_dismantle','persistent_aura','delay_reflect','delay_reflect_all','mana_growth','mana_convert','mana_swift','last_shield','shield_mana','reboot','seal'
];
const CARD_ASSETS=CARD_IDS.map(id=>`./assets/cards/${id}.webp`);
const APP_SHELL=['./','./index.html','./manifest.webmanifest','./icon.svg','./icon-maskable.svg',...CARD_ASSETS];

self.addEventListener('install',event=>{
  event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate',event=>{
  event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==CACHE_NAME).map(key=>caches.delete(key)))));
  self.clients.claim();
});

self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;
  if(event.request.mode==='navigate'){
    event.respondWith(fetch(event.request).then(response=>{
      const copy=response.clone();
      caches.open(CACHE_NAME).then(cache=>cache.put('./index.html',copy));
      return response;
    }).catch(()=>caches.match('./index.html')));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request).then(response=>{
    if(response&&response.ok&&new URL(event.request.url).origin===self.location.origin){
      const copy=response.clone();
      caches.open(CACHE_NAME).then(cache=>cache.put(event.request,copy));
    }
    return response;
  })));
});
