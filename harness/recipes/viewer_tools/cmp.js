// node cmp.js base.tsv new.tsv  -> lists members (label+box) only in base (removed/changed) and only in new (added/changed)
const fs=require('fs');const rd=f=>fs.readFileSync(f,'utf8').trim().split('\n').map(l=>l.split('\t').slice(1).join('\t'));
const a=rd(process.argv[2]),b=rd(process.argv[3]);const cnt=m=>{const c=new Map();m.forEach(k=>c.set(k,(c.get(k)||0)+1));return c};
const A=cnt(a),B=cnt(b);const only=(X,Y)=>[...X].flatMap(([k,n])=>Array(Math.max(0,n-(Y.get(k)||0))).fill(k));
const r=only(A,B),ad=only(B,A);console.log('base',a.length,'new',b.length,'| only-in-base',r.length,'| only-in-new',ad.length);
console.log('--- only in base\n'+r.join('\n'));console.log('--- only in new\n'+ad.join('\n'));
