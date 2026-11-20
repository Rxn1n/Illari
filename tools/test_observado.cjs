/* Run from the repository with: node --test tools/test_observado.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const scripts = Array.from(html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g), m => m[1]);
const app = scripts.find(script => script.includes('function detect(hz)'));
function section(start, end) {
  const from = app.indexOf(start);
  const to = app.indexOf(end, from + start.length);
  assert.ok(from >= 0 && to > from, 'Missing application section: ' + start);
  return app.slice(from, to);
}
// Exercise the functions from the shipped page without a network or a browser.
const definitions = [
  section('const nearestCell =', '/* ---------------------------------------------------------------- estado'),
  section('function boxMean(', '/* ---- escena de demostración'),
  section('function compat(', 'function pairForEvent('),
  section('function cellLL(', 'function sectorShare('),
  section('function compareIntervals(', 'async function viirsDaily(')
].join('\n');
const bbox = {n:1,s:0,w:0,e:1};
const dates = ['2026-10-07','2026-10-19'];
function context() {
  const S = {obs:{}, data:{}, multi:{}, cache:new Map(), hz:'fire'};
  const grid = new Float32Array(16);
  const acqs = dates.map((date,i) => ({
    date, prod:'GCOV', track:'112', dir:'D', frame:'090',
    pols:{HH:grid.map(() => i ? 0.001 : 1)}
  }));
  S.obs.flood = {source:'real', acqs, A:0, B:1, NX:4, NY:4, bbox, chg:3, pol:'HH', thrAuto:false, thrWater:-18};
  const noop = () => {};
  const api = {S, CITIES:{flood:{sectors:[]}}, KM_DEG:111.32, DEM_TILES:'tiles', DEM_COPERNICUS:'copernicus',
    NOW_EV:'now', TODAY:'2026-11-15', OPERA:{s1:'s1', hls:'hls'}, PAL_DSWX:[],
    evDate:()=>null, renderMulti:noop, renderObs:noop, sectorShare:()=>[],
    cellKm2:()=>1, loadCtx:async()=>null, exposure:()=>null, decodePal:rgba=>rgba,
    addDays:(d,n)=>new Date(Date.parse(d)+864e5*n).toISOString().slice(0,10)};
  vm.runInNewContext(definitions, api);
  return api;
}
test('both inline scripts compile', () => { for (const code of scripts) new vm.Script(code); });
test('a weather fallback cannot change the observed classification', () => {
  const api = context(), {S} = api, O = S.obs.flood;
  const classify = () => { api.detect('flood'); return [...O.res.cls]; };
  S.floodTerrain = {source:'tiles', NX:2, NY:1, bbox, z:[0,50]};
  const withDEM = classify();
  assert.equal(O.demMasked,8);
  S.data.flood = {mode:'demo', NX:1, NY:1, z:[1000]};
  assert.deepEqual(classify(), withDEM);
  delete S.floodTerrain;
  assert.ok(classify().every(code => code === 2));
  assert.equal(O.demSource,null);
  assert.match(O.res.warn.join(' '),/altitud omitido/);
  O.savedAt = '2026-11-15';
  O.terrain = {source:'demo', NX:1, NY:1, bbox, z:[1000]};
  assert.ok(classify().every(code => code === 2));
});
test('matches each OPERA endpoint and keeps day offsets', async () => {
  const api = context(), {S} = api;
  api.detect('flood');
  const calls = [];
  const allDates = ['2026-10-06','2026-10-18','2026-11-12'];
  api.scanDates = async (layer, box, start, end) => {
    calls.push([layer,start,end]);
    return layer === 's1' ? allDates.filter(d=>d >= start && d <= end).map(date=>({date})) : [];
  };
  api.gridOf = async (layer,date) => ({rgba:new Uint8Array(16).fill(date==='2026-10-18'?1:0), url:date});
  S.obs.flood.event = 'now';
  await api.loadMulti('flood');
  const M = S.multi.flood;
  assert.equal(M.status,'ok',M.err);
  assert.deepEqual(calls.filter(c=>c[0]==='s1'),[['s1','2026-10-01','2026-10-13'],['s1','2026-10-13','2026-10-25']]);
  assert.equal(M.timing.operaBefore,'2026-10-06'); assert.equal(M.timing.operaAfter,'2026-10-18');
  assert.equal(M.timing.beforeDays,-1); assert.equal(M.timing.afterDays,-1);
  assert.match(api.intervalLabel(M.timing), /exploratoria/);
  assert.match(api.intervalLabel(api.compareIntervals(...dates,...dates)), /mismas fechas/);
  api.scanDates = async () => [];
  await api.loadMulti('flood');
  assert.equal(S.multi.flood.status,'error');
});
