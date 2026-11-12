const {chromium}=require('playwright');const fs=require('fs');const SP=process.env.SP;
const THREEJS=fs.readFileSync(SP+'/node_modules/three/build/three.min.js','utf8')+"\n;(function(){var R=THREE.WebGLRenderer;THREE.WebGLRenderer=function(o){o=o||{};o.preserveDrawingBuffer=true;var r=new R(o);window.__R=r;var rr=r.render.bind(r);r.render=function(s,c){window.__S=s;return rr(s,window.__ORTHO||c)};return r};THREE.WebGLRenderer.prototype=R.prototype;})();";
const ORB=fs.readFileSync(SP+'/node_modules/three/examples/js/controls/OrbitControls.js','utf8');
async function open(file,w=1400,h=900){const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
await p.route('**/three.min.js',r=>r.fulfill({body:THREEJS,contentType:'application/javascript'}));
await p.route('**/OrbitControls.js',r=>r.fulfill({body:ORB,contentType:'application/javascript'}));
p.on('pageerror',e=>console.log('PAGEERR',e.message));
await p.goto('file://'+file);await p.waitForTimeout(1500);return {b,p};}
module.exports={open};
