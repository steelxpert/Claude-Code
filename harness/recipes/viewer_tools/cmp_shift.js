// node cmp_shift.js old.tsv new.tsv [shift=0.15] [skipRegex]  -> house compare with old y shifted
const fs=require('fs');const sh=process.argv[4]===undefined?0.15:+process.argv[4];
const skip=new RegExp(process.argv[5]||'^(Soil screw|Ground floor|Floor panel|Cross bearer)');
const rd=f=>fs.readFileSync(f,'utf8').trim().split('\n').filter(Boolean).map(l=>l.split('\t').slice(1));
const key=(r,s)=>[r[0],r[1],(+r[2]+s).toFixed(4),r[3],r[4],(+r[5]+s).toFixed(4),r[6]].join('\t');
const keyn=r=>r.join('\t');
const a=rd(process.argv[2]),b=rd(process.argv[3]);
const sk=r=>skip.test(r[0]);
const A=a.filter(r=>!sk(r)).map(r=>key(r,sh)), B=b.filter(r=>!sk(r)).map(keyn);
const cnt=m=>{const c=new Map();m.forEach(k=>c.set(k,(c.get(k)||0)+1));return c};
const CA=cnt(A),CB=cnt(B);const only=(X,Y)=>[...X].flatMap(([k,n])=>Array(Math.max(0,n-(Y.get(k)||0))).fill(k));
const r=only(CA,CB),ad=only(CB,CA);
console.log('old',a.length,'new',b.length,'compared old',A.length,'new',B.length,'skipped old',a.length-A.length,'skipped new',b.length-B.length,'| mismatch old',r.length,'new',ad.length);
r.forEach(x=>console.log('OLD(shifted) '+x));ad.forEach(x=>console.log('NEW '+x));
