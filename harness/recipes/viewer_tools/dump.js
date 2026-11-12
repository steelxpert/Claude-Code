const {open}=require('./lib.js');(async()=>{const {b,p}=await open(process.argv[2]);
const out=await p.evaluate((k)=>{if(k!=='all')__dbg.showMode(k);__S.updateMatrixWorld(true);const vis=o=>{for(;o;o=o.parent)if(!o.visible)return false;return true};const res=[];
__members.forEach((m,i)=>{const bb=new THREE.Box3();let n=0;m.meshes.forEach(o=>{if(k!=='all'&&!vis(o))return;bb.expandByObject(o);n++});if(!n)return;const f=v=>v.toFixed(4);res.push([i,m.label,f(bb.min.x),f(bb.min.y),f(bb.min.z),f(bb.max.x),f(bb.max.y),f(bb.max.z)].join('\t'))});return res},process.argv[3]);
console.log(out.join('\n'));await b.close()})();
