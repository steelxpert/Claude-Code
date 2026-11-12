// Standing rules (owner 2026-11-12): thin-but-visible black profile outlines (fat lines), orthographic ISO views only, sections shown in iso.
// usage: node shot.js html views.json ; view = {mode,out,dir:[x,y,z],tgt:[..],half:m,clips:[[[nx,ny,nz],c],..],ex,lw}
const {open}=require('./lib.js');const fs=require('fs');const SP=process.env.SP;(async()=>{const {b,p}=await open(process.argv[2],1200,900);
for(const f of ['LineSegmentsGeometry','LineMaterial','LineSegments2'])await p.addScriptTag({content:fs.readFileSync(SP+'/node_modules/three/examples/js/lines/'+f+'.js','utf8')});
await p.evaluate(()=>{window.requestAnimationFrame=function(){return 0}});
const views=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
await p.evaluate(()=>{const sz=__R.getDrawingBufferSize(new THREE.Vector2());window.__LM=new THREE.LineMaterial({color:0x000000,linewidth:3,resolution:sz});
const L=[];__S.traverse(o=>{if(o.isMesh&&o.geometry&&!o.userData.__e)L.push(o)});
L.forEach(o=>{o.userData.__e=1;const g=new THREE.LineSegmentsGeometry().fromEdgesGeometry(new THREE.EdgesGeometry(o.geometry,25));const e=new THREE.LineSegments2(g,__LM);e.raycast=()=>{};o.add(e)});});
for(const v of views){await p.evaluate(v=>{__dbg.showMode(v.mode);(typeof v.ex==="number"?__dbg.setExplode(v.ex):__dbg.applyExplode(!!v.ex));__LM.linewidth=v.lw||3;if(window.__TMP){__S.remove(__TMP);window.__TMP=null}if(v.add){window.__TMP=new THREE.Group();(new Function("G",v.add))(__TMP);__S.add(__TMP)}
const el=__R.domElement,asp=el.clientWidth/el.clientHeight,h=v.half||0.5;const c=new THREE.OrthographicCamera(-h*asp,h*asp,h,-h,-50,50);
const t=new THREE.Vector3(...v.tgt),d=new THREE.Vector3(...v.dir).normalize();c.position.copy(t).addScaledVector(d,10);c.up.set(...(v.up||[0,1,0]));c.lookAt(t);c.updateProjectionMatrix();window.__ORTHO=c;
__R.clippingPlanes=(v.clips||[]).map(q=>new THREE.Plane(new THREE.Vector3(...q[0]),q[1]));__R.render(__S,c)},v);
await p.waitForTimeout(300);const du=await p.evaluate(()=>{__R.render(__S,__ORTHO);return __R.domElement.toDataURL('image/png')});fs.writeFileSync(v.out,Buffer.from(du.split(',')[1],'base64'));console.log('ok',v.out)}
await b.close()})();
