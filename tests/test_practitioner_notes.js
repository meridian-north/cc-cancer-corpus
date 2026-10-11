const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const script = fs.readFileSync(path.join(root, 'practitioner_notes.js'), 'utf8');
function fixture() {
  const ids = ['question','agents','timing','observations','confounders','review','sources','preview-note','download-note','clear-note','preview','preview-section','status'];
  const elements = Object.fromEntries(ids.map(id => [id, {value:'',textContent:'',hidden:true,handlers:{},addEventListener(type, fn){this.handlers[type]=fn;}}]));
  for(const node of Object.values(elements)) Object.defineProperty(node,'innerHTML',{set(){throw new Error('HTML injection sink');}});
  let downloaded, clicked = false, revoked = false;
  const context = {document:{getElementById(id){assert.ok(elements[id],id);return elements[id];},
    createElement(type){assert.equal(type,'a');return {click(){clicked=true;assert.equal(this.download,'private-practitioner-notes.txt');},remove(){}};},body:{appendChild(){}}},
    Blob, URL:{createObjectURL(blob){downloaded=blob;return 'blob:synthetic';},revokeObjectURL(url){assert.equal(url,'blob:synthetic');revoked=true;}},
    setTimeout(fn){fn();}, fetch(){throw new Error('network forbidden');}, XMLHttpRequest(){throw new Error('network forbidden');}, WebSocket(){throw new Error('network forbidden');}};
  for (const key of ['localStorage','sessionStorage','indexedDB','navigator','location']) Object.defineProperty(context,key,{get(){throw new Error(key+' forbidden');}});
  vm.runInNewContext(script,context);
  return {elements,click(id){elements[id].handlers.click();},download:()=>downloaded,clicked:()=>clicked,revoked:()=>revoked};
}
test('preview renders literal input, including markup, without network/storage access',()=>{
  const f=fixture();f.elements.question.value='<img src=x onerror=alert(1)> synthetic question';f.click('preview-note');
  assert.match(f.elements.preview.textContent,/<img src=x onerror=alert\(1\)>/);
  assert.equal(f.elements['preview-section'].hidden,false);
  assert.match(f.elements.preview.textContent,/Do not post to GitHub/);
});
test('download contains current fields and preserves unknown values without inference',async()=>{
  const f=fixture();f.elements.agents.value='Synthetic product; dose unknown';f.click('download-note');
  assert.equal(f.clicked(),true);assert.equal(f.revoked(),true);
  const text=await f.download().text();assert.match(text,/dose unknown/);assert.match(text,/Not recorded/);
  assert.match(text,/PRIVATE NOTES FOR MY LICENSED PRACTITIONER/);
});
test('clear removes all field and preview content',()=>{
  const f=fixture();f.elements.observations.value='synthetic observation';f.click('preview-note');f.click('clear-note');
  assert.equal(f.elements.observations.value,'');assert.equal(f.elements.preview.textContent,'');
  assert.equal(f.elements['preview-section'].hidden,true);
});
test('worksheet blocks connections and form submissions and has no external assets',()=>{
  const html=fs.readFileSync(path.join(root,'practitioner_notes.html'),'utf8');
  assert.match(html,/connect-src 'none'/);assert.match(html,/form-action 'none'/);
  assert.doesNotMatch(html,/<form\b|<input[^>]*type=["']?file|src=["']https?:/i);
  assert.match(html,/There is no submit button/);
  for(const match of html.matchAll(/<textarea[^>]*>/g)) {assert.match(match[0],/autocomplete="off"/);assert.match(match[0],/maxlength="6000"/);}
});
