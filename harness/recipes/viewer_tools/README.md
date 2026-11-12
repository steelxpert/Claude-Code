# Viewer render + regression tools (FLIN-006)

For docs/pilot_house/concept_viewer.html. Setup in a scratchpad: `npm i three@0.128.0`, copy these files
next to node_modules, run with `SP=<scratchpad>` (lib.js serves three.min.js + OrbitControls from
node_modules via page.route and wraps the renderer: window.__R, window.__S, window.__ORTHO).

- `node shot.js <html> views.json` - owner sketch rules: orthographic iso, fat black outlines,
  sections as clipping-plane slabs. View: {mode,out,dir,tgt,half,clips:[[[nx,ny,nz],c]],ex,lw}.
- `node shot3.js <html> views.json` - same, canvas grab via toDataURL (use for mode 'house').
- `node dump.js <html> <mode|all>` - Box3 per member (tsv); `node cmp.js a.tsv b.tsv` - label+box
  multiset diff; `cmp_shift.js` - same with a y shift (used when FL moved).
