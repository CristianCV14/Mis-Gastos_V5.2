from pathlib import Path
import zipfile, shutil, re
base=Path('/mnt/data/mis_gastos_v5')
# preserve original styles and files already extracted
idx=base/'index.html'; js=base/'app.js'; css=base/'styles.css'
html=idx.read_text(encoding='utf-8')
# Add dashboard commitment card after category summary section
html=html.replace('<section class="section"><div class="section-title"><h2>¿En qué estás gastando?</h2></div><div id="categorySummary" class="category-summary"></div></section>', '''<section class="section"><div class="section-title"><h2>Compromisos del mes</h2><button class="link-btn" data-view="commitments">Ver todos</button></div><div id="commitmentSummary" class="commitment-summary"></div></section>
  <section class="section"><div class="section-title"><h2>¿En qué estás gastando?</h2></div><div id="categorySummary" class="category-summary"></div></section>''')
# Add commitments view before stats
marker='<section id="statsView" class="view">'
commit_view='''<section id="commitmentsView" class="view">
  <div class="section-title"><div><span class="eyebrow">PLANIFICACIÓN</span><h2>Compromisos</h2></div><button id="newCommitmentBtn" class="primary-small">＋ Agregar</button></div>
  <div class="commitment-tabs"><button class="commit-tab active" data-commit-tab="active">Activos</button><button class="commit-tab" data-commit-tab="history">Historial</button></div>
  <div id="activeCommitments"></div><div id="commitmentHistory" class="hidden"></div>
</section>

'''
html=html.replace(marker,commit_view+marker)
# Add commitment modal before expense modal
modal='''<div id="commitmentModal" class="modal hidden"><div class="modal-card">
<div class="modal-header"><div><span class="eyebrow">NUEVO COMPROMISO</span><h2 id="commitmentModalTitle">Agregar compromiso</h2></div><button id="closeCommitmentModal" class="round-btn">✕</button></div>
<form id="commitmentForm">
<input id="commitmentId" type="hidden">
<label>Tipo de compromiso<select id="commitmentType"><option value="fixed">🔄 Gasto fijo mensual</option><option value="installment">💳 Compra en cuotas</option></select></label>
<label>Nombre<input id="commitmentName" type="text" maxlength="80" required placeholder="Ej: Cuenta celular, Notebook"></label>
<label>Monto mensual / valor de cuota<input id="commitmentAmount" type="number" min="1" step="1" inputmode="numeric" required placeholder="25000"></label>
<label>Categoría<select id="commitmentCategory"></select></label>
<label>Medio de pago<select id="commitmentPayment"></select></label>
<label>Día de vencimiento<input id="commitmentDueDay" type="number" min="1" max="31" value="10"></label>
<div id="installmentFields" class="installment-fields hidden">
<label>Número total de cuotas<input id="totalInstallments" type="number" min="1" step="1" value="12"></label>
<label>Fecha de la primera cuota<input id="startDate" type="date"></label>
</div>
<div id="fixedFields"><label>Fecha de inicio<input id="fixedStartDate" type="date"></label></div>
<button class="primary-btn save-btn" type="submit">✓ Guardar compromiso</button>
</form></div></div>

<div id="commitmentDetailModal" class="modal hidden"><div class="modal-card">
<div class="modal-header"><div><span class="eyebrow">DETALLE</span><h2 id="detailTitle">Compromiso</h2></div><button id="closeDetailModal" class="round-btn">✕</button></div>
<div id="commitmentDetail"></div>
</div></div>

'''
html=html.replace('<div id="expenseModal"',modal+'<div id="expenseModal"')
idx.write_text(html,encoding='utf-8')

# Append CSS
css_text=css.read_text(encoding='utf-8')
css_text += r'''
.primary-small{border:0;background:#0f172a;color:#fff;border-radius:12px;padding:10px 14px;font-weight:800;cursor:pointer}.commitment-summary{display:grid;gap:8px}.commitment-card{background:#fff;border:1px solid #e2e8f0;border-radius:17px;padding:13px;display:grid;grid-template-columns:1fr auto;gap:8px;box-shadow:0 3px 12px #0f172a08}.commitment-card .cc-main{min-width:0}.commitment-card .cc-title{font-weight:850;font-size:14px}.commitment-card .cc-meta{color:#64748b;font-size:11px;margin-top:4px}.commitment-card .cc-amount{font-weight:900;text-align:right}.cc-badge{display:inline-flex;align-items:center;margin-top:7px;padding:4px 7px;border-radius:999px;background:#eef2ff;color:#4338ca;font-size:10px;font-weight:800}.cc-actions{grid-column:1/-1;display:flex;gap:7px;flex-wrap:wrap}.cc-actions button{border:1px solid #e2e8f0;background:#f8fafc;border-radius:10px;padding:7px 9px;font-size:11px;font-weight:800;cursor:pointer}.cc-actions .danger{color:#b91c1c}.cc-progress{height:7px;background:#e2e8f0;border-radius:99px;overflow:hidden;margin-top:8px}.cc-progress i{display:block;height:100%;background:#4f46e5}.commitment-tabs{display:flex;background:#eef2f7;border-radius:13px;padding:4px;margin:12px 0 16px}.commit-tab{flex:1;border:0;background:transparent;border-radius:10px;padding:9px;font-weight:800;color:#64748b;cursor:pointer}.commit-tab.active{background:#fff;color:#0f172a;box-shadow:0 2px 7px #0f172a12}.commitment-list{display:grid;gap:10px}.history-card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:14px}.history-card h3{margin:0 0 5px}.history-card p{margin:4px 0;color:#64748b;font-size:12px}.history-status{font-size:10px;font-weight:900}.status-completed{color:#15803d}.status-cancelled{color:#b91c1c}.status-paused{color:#a16207}.commit-detail{display:grid;gap:10px}.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.detail-box{background:#f8fafc;border-radius:13px;padding:11px}.detail-box span{display:block;color:#64748b;font-size:10px}.detail-box strong{display:block;margin-top:3px;font-size:14px}.detail-actions{display:grid;gap:8px;margin-top:8px}.empty.small{padding:20px 12px}.form-card h3{margin-top:0}.hidden{display:none!important}
'''
css.write_text(css_text,encoding='utf-8')

# Rewrite JS with v5 logic
newjs=r'''const CATEGORIES=[['🍔','Comida'],['🚗','Transporte'],['🛒','Compras'],['🏠','Hogar'],['💊','Salud'],['🎮','Ocio'],['💳','Servicios'],['📦','Otros']];
const PAYMENTS=['💵 Efectivo','💳 Débito','💳 Crédito','🏦 Transferencia','❓ Otro'];
const KEY='mis_gastos_v5';const SETTINGS_KEY='mis_gastos_settings_v5';const OLD_KEY='mis_gastos_v3';const OLD_SETTINGS='mis_gastos_settings_v3';
let expenses=JSON.parse(localStorage.getItem(KEY)||'null');
let settings=JSON.parse(localStorage.getItem(SETTINGS_KEY)||'null');
let commitments=JSON.parse(localStorage.getItem('mis_gastos_commitments_v5')||'[]');
if(!expenses){expenses=JSON.parse(localStorage.getItem(OLD_KEY)||'[]');localStorage.setItem(KEY,JSON.stringify(expenses))}
if(!settings){settings=JSON.parse(localStorage.getItem(OLD_SETTINGS)||'{"budget":0}');localStorage.setItem(SETTINGS_KEY,JSON.stringify(settings))}
let quickCategory='';let commitmentTab='active';
const $=id=>document.getElementById(id),money=n=>new Intl.NumberFormat('es-CL',{style:'currency',currency:'CLP',maximumFractionDigits:0}).format(Number(n)||0),today=()=>new Date().toISOString().slice(0,10),monthKey=d=>String(d).slice(0,7),currentMonth=()=>today().slice(0,7),catIcon=n=>(CATEGORIES.find(x=>x[1]===n)||['📦'])[0];
const save=()=>localStorage.setItem(KEY,JSON.stringify(expenses)),saveSettings=()=>localStorage.setItem(SETTINGS_KEY,JSON.stringify(settings)),saveCommitments=()=>localStorage.setItem('mis_gastos_commitments_v5',JSON.stringify(commitments));
function toast(msg){const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1800)}
function esc(s){return String(s||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
function dateObj(s){const [y,m,d]=String(s).split('-').map(Number);return new Date(y,m-1,d)}
function monthDiff(a,b){return (b.getFullYear()-a.getFullYear())*12+b.getMonth()-a.getMonth()}
function installmentInfo(c,month=currentMonth()){
 const start=dateObj(c.startDate), target=dateObj(month+'-01');let elapsed=monthDiff(start,new Date(target.getFullYear(),target.getMonth(),1));
 const current=elapsed+1;const total=Number(c.totalInstallments)||1;return {current,remaining:Math.max(0,total-current),total,active:current>=1&&current<=total,completed:current>total}
}
function fixedActive(c){return c.status==='active'&&monthKey(c.startDate)<=currentMonth()}
function commitmentForMonth(c,month=currentMonth()){
 if(c.type==='fixed') return c.status==='active'&&monthKey(c.startDate)<=month?Number(c.amount):0;
 const info=installmentInfo(c,month);return c.status==='active'&&info.active?Number(c.amount):0;
}
function activeCommitments(){return commitments.filter(c=>c.status==='active'&& (c.type==='fixed'?fixedActive(c):installmentInfo(c).active))}
function commitmentState(c){if(c.type==='installment'){const i=installmentInfo(c);if(i.completed)return 'completed'}return c.status}
function commitmentLabel(c){if(c.type==='fixed')return '🔄 Gasto fijo mensual';const i=installmentInfo(c);return `💳 Cuota ${Math.min(Math.max(i.current,1),i.total)} de ${i.total}`}
function commitmentTotal(){return activeCommitments().reduce((s,c)=>s+commitmentForMonth(c),0)}
function populate(){
 $('categoryGrid').innerHTML=CATEGORIES.map(([i,n])=>`<button type="button" class="category-choice" data-cat="${n}"><span>${i}</span><small>${n}</small></button>`).join('');
 $('quickCategories').innerHTML=CATEGORIES.map(([i,n])=>`<button type="button" class="quick-cat" data-qcat="${n}"><span>${i}</span><small>${n}</small></button>`).join('');
 $('paymentGrid').innerHTML=PAYMENTS.map(x=>`<button type="button" class="payment-choice" data-pay="${x}">${x}</button>`).join('');
 $('categoryFilter').innerHTML='<option value="">Todas las categorías</option>'+CATEGORIES.map(([i,n])=>`<option value="${n}">${i} ${n}</option>`).join('');
 $('commitmentCategory').innerHTML=CATEGORIES.map(([i,n])=>`<option value="${n}">${i} ${n}</option>`).join('');
 $('commitmentPayment').innerHTML=PAYMENTS.map(x=>`<option value="${x}">${x}</option>`).join('');
}
function selectCategory(v){$('categoryInput').value=v;document.querySelectorAll('.category-choice').forEach(b=>b.classList.toggle('selected',b.dataset.cat===v))}
function selectPayment(v){$('paymentInput').value=v;document.querySelectorAll('.payment-choice').forEach(b=>b.classList.toggle('selected',b.dataset.pay===v))}
document.addEventListener('click',e=>{const c=e.target.closest('[data-cat]');if(c)selectCategory(c.dataset.cat);const p=e.target.closest('[data-pay]');if(p)selectPayment(p.dataset.pay);const qc=e.target.closest('[data-qcat]');if(qc){quickCategory=qc.dataset.qcat;document.querySelectorAll('.quick-cat').forEach(b=>b.classList.toggle('selected',b.dataset.qcat===quickCategory));updateQuickHint()}});
function updateQuickHint(){const amount=Number($('quickAmount').value)||0;$('quickHint').textContent=amount&&quickCategory?`Listo: ${money(amount)} en ${quickCategory}. Toca Guardar.`:'Ingresa un monto y selecciona una categoría.';$('quickHint').classList.toggle('ok',!!(amount&&quickCategory))}
$('quickAmount').addEventListener('input',updateQuickHint);
$('quickSaveBtn').onclick=()=>{const amount=Number($('quickAmount').value);if(!amount){$('quickAmount').focus();toast('Ingresa un monto');return}if(!quickCategory){toast('Selecciona una categoría');return}expenses.push({id:crypto.randomUUID(),amount,category:quickCategory,payment:'💵 Efectivo',description:'',date:today(),createdAt:Date.now()});save();$('quickAmount').value='';quickCategory='';document.querySelectorAll('.quick-cat').forEach(b=>b.classList.remove('selected'));updateQuickHint();render();toast('✓ Gasto registrado')};
function totals(){const m=expenses.filter(e=>monthKey(e.date)===currentMonth()),normal=m.reduce((s,e)=>s+e.amount,0),fixedAndInstallments=commitmentTotal(),committed=normal+fixedAndInstallments,tt=m.filter(e=>e.date===today()).reduce((s,e)=>s+e.amount,0),r=Math.max(0,(settings.budget||0)-committed);$('monthTotal').textContent=money(committed);$('todayTotal').textContent=money(tt);$('budgetTotal').textContent=money(settings.budget);$('remainingTotal').textContent=money(r);$('monthLabel').textContent=new Date().toLocaleDateString('es-CL',{month:'long',year:'numeric'})}
function item(e){return `<article class="expense-item"><div class="expense-icon">${catIcon(e.category)}</div><div class="expense-info"><strong>${esc(e.description||e.category)}</strong><small>${e.category} · ${e.payment.replace(/^[^ ]+ /,'')} · ${e.date}</small></div><div class="expense-amount">${money(e.amount)}</div><div class="item-actions"><button onclick="editExpense('${e.id}')">✏️</button><button onclick="deleteExpense('${e.id}')">🗑️</button></div></article>`}
function catData(list){const m={};list.forEach(e=>m[e.category]=(m[e.category]||0)+e.amount);const rows=Object.entries(m).sort((a,b)=>b[1]-a[1]),max=rows[0]?.[1]||1;return rows.map(([c,t])=>`<div class="cat-row"><div class="cat-top"><span>${catIcon(c)} ${c}</span><strong>${money(t)}</strong></div><div class="bar"><i style="width:${t/max*100}%"></i></div></div>`).join('')}
function commitmentCard(c){const value=commitmentForMonth(c),info=c.type==='installment'?installmentInfo(c):null;let meta=c.type==='fixed'?`$${money(value)} cada mes · Día ${c.dueDay||'—'}`:`${money(value)} este mes · ${commitmentLabel(c)} · Restan ${info.remaining} cuotas`;let progress=info?`<div class="cc-progress"><i style="width:${Math.min(100,info.current/info.total*100)}%"></i></div>`:'';return `<article class="commitment-card"><div class="cc-main"><div class="cc-title">${c.type==='fixed'?'🔄':'💳'} ${esc(c.name)}</div><div class="cc-meta">${esc(c.category)} · ${esc(c.payment)} · ${meta}</div><span class="cc-badge">${c.type==='fixed'?'Activo mensual':`Cuota ${info.current} de ${info.total}`}</span>${progress}</div><div class="cc-amount">${money(value)}</div><div class="cc-actions"><button onclick="showCommitmentDetail('${c.id}')">Ver detalle</button><button onclick="editCommitment('${c.id}')">✏️ Editar</button><button onclick="pauseCommitment('${c.id}')">⏸️ Pausar</button><button class="danger" onclick="cancelCommitment('${c.id}')">Cancelar</button></div></article>`}
function commitmentSummary(){const a=activeCommitments();$('commitmentSummary').innerHTML=a.length?a.slice(0,3).map(commitmentCard).join(''):`<div class="empty">No tienes compromisos activos. Agrega tus gastos fijos o compras en cuotas.</div>`}
function renderCommitments(){const active=activeCommitments();$('activeCommitments').innerHTML=active.length?`<div class="commitment-list">${active.map(commitmentCard).join('')}</div>`:'<div class="empty small">No tienes compromisos activos.</div>';const hist=commitments.filter(c=>commitmentState(c)!=='active'||(c.type==='installment'&&installmentInfo(c).completed)).sort((a,b)=>(b.updatedAt||b.createdAt)-(a.updatedAt||a.createdAt));$('commitmentHistory').innerHTML=hist.length?`<div class="commitment-list">${hist.map(historyCard).join('')}</div>`:'<div class="empty small">Aquí aparecerán los compromisos finalizados o cancelados.</div>'}
function historyCard(c){let status=commitmentState(c),label=status==='completed'?'Finalizado':status==='cancelled'?'Cancelado':'Pausado';let detail=c.type==='installment'?`${money(c.amount)} · ${c.totalInstallments} cuotas · Inicio ${c.startDate}`:`${money(c.amount)} al mes · Inicio ${c.startDate}`;return `<article class="history-card"><h3>${c.type==='fixed'?'🔄':'💳'} ${esc(c.name)}</h3><p>${detail}</p><p><span class="history-status ${status==='completed'?'status-completed':status==='cancelled'?'status-cancelled':'status-paused'}">${label}</span></p><div class="cc-actions"><button onclick="showCommitmentDetail('${c.id}')">Ver detalle</button></div></article>`}
function render(){totals();const m=expenses.filter(e=>monthKey(e.date)===currentMonth()).sort((a,b)=>b.createdAt-a.createdAt);$('recentList').innerHTML=m.length?m.slice(0,6).map(item).join(''):'<div class="empty">Todavía no tienes gastos registrados este mes.</div>';$('categorySummary').innerHTML=catData(m)||'<div class="empty">Aquí verás en qué categorías gastas más.</div>';commitmentSummary();renderHistory();renderCommitments();const total=m.reduce((s,e)=>s+e.amount,0);$('statCount').textContent=m.length;$('statAverage').textContent=money(m.length?total/m.length:0);$('statMax').textContent=money(Math.max(0,...m.map(e=>e.amount)));$('statDays').textContent=new Set(m.map(e=>e.date)).size;$('statsCategories').innerHTML=catData(m)||'<div class="empty">Registra gastos para ver estadísticas.</div>'}
function renderHistory(){const q=$('searchInput').value.toLowerCase().trim(),c=$('categoryFilter').value,d=$('dateFilter').value,l=expenses.filter(e=>(!q||`${e.description} ${e.category} ${e.payment}`.toLowerCase().includes(q))&&(!c||e.category===c)&&(!d||e.date===d)).sort((a,b)=>b.date.localeCompare(a.date)||b.createdAt-a.createdAt);$('historyList').innerHTML=l.length?l.map(item).join(''):'<div class="empty">No hay gastos que coincidan con los filtros.</div>'}
function openModal(id=null,preset=null){$('expenseForm').reset();$('expenseId').value=id||'';$('modalTitle').textContent=id?'Editar gasto':'Registrar gasto';selectCategory('');selectPayment('');$('dateInput').value=today();if(id){const e=expenses.find(x=>x.id===id);if(e){$('amountInput').value=e.amount;selectCategory(e.category);selectPayment(e.payment);$('descriptionInput').value=e.description||'';$('dateInput').value=e.date}}else if(preset)$('amountInput').value=preset;$('expenseModal').classList.remove('hidden');setTimeout(()=>$('amountInput').focus(),80)}
function closeModal(){$('expenseModal').classList.add('hidden')}
window.editExpense=id=>openModal(id);window.deleteExpense=id=>{if(confirm('¿Eliminar este gasto?')){expenses=expenses.filter(e=>e.id!==id);save();render();toast('Gasto eliminado')}};
$('expenseForm').onsubmit=e=>{e.preventDefault();if(!$('categoryInput').value||!$('paymentInput').value){toast('Selecciona categoría y medio de pago');return}const id=$('expenseId').value,d={amount:Number($('amountInput').value),category:$('categoryInput').value,payment:$('paymentInput').value,description:$('descriptionInput').value.trim(),date:$('dateInput').value};if(id){const i=expenses.findIndex(x=>x.id===id);expenses[i]={...expenses[i],...d}}else expenses.push({id:crypto.randomUUID(),...d,createdAt:Date.now()});save();closeModal();render();toast('✓ Gasto guardado')};
document.querySelectorAll('[data-amount]').forEach(b=>b.onclick=()=>{$('amountInput').value=b.dataset.amount});document.querySelectorAll('[data-quick]').forEach(b=>b.onclick=()=>{showView('dashboard');$('quickAmount').value=b.dataset.quick;updateQuickHint();$('quickAmount').focus()});$('quickAddBtn').onclick=()=>openModal();$('closeModal').onclick=closeModal;$('expenseModal').onclick=e=>{if(e.target===$('expenseModal'))closeModal()};
function showView(n){document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));$(`${n}View`).classList.add('active');document.querySelectorAll('.nav-btn').forEach(b=>b.classList.toggle('active',b.dataset.view===n));window.scrollTo({top:0,behavior:'smooth'})}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>showView(b.dataset.view));$('settingsBtn').onclick=()=>showView('settings');['searchInput','categoryFilter','dateFilter'].forEach(id=>$(id).addEventListener('input',renderHistory));$('clearFilters').onclick=()=>{$('searchInput').value='';$('categoryFilter').value='';$('dateFilter').value='';renderHistory()};
$('saveBudgetBtn').onclick=()=>{settings.budget=Number($('budgetInput').value)||0;saveSettings();render();toast('✓ Presupuesto guardado')};
$('exportBtn').onclick=()=>{const blob=new Blob([JSON.stringify({expenses,settings,commitments,exportedAt:new Date().toISOString()},null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`mis-gastos-${today()}.json`;a.click();URL.revokeObjectURL(a.href)};
$('importInput').onchange=async e=>{const f=e.target.files[0];if(!f)return;try{const d=JSON.parse(await f.text());if(!Array.isArray(d.expenses))throw 0;if(confirm('Esto reemplazará los datos actuales. ¿Continuar?')){expenses=d.expenses;settings=d.settings||settings;commitments=Array.isArray(d.commitments)?d.commitments:commitments;save();saveSettings();saveCommitments();render();toast('✓ Datos importados')}}catch{toast('Archivo no válido')}e.target.value=''};
$('deleteAllBtn').onclick=()=>{if((expenses.length||commitments.length)&&confirm('¿Eliminar TODOS los gastos y compromisos?')){expenses=[];commitments=[];save();saveCommitments();render();toast('Datos eliminados')}};
function toggleCommitmentFields(){const type=$('commitmentType').value;$('installmentFields').classList.toggle('hidden',type!=='installment');$('fixedFields').classList.toggle('hidden',type!=='fixed')}
function openCommitmentModal(id=null){$('commitmentForm').reset();$('commitmentId').value=id||'';$('commitmentModalTitle').textContent=id?'Editar compromiso':'Agregar compromiso';$('commitmentType').value='fixed';$('commitmentDueDay').value=10;$('fixedStartDate').value=today();$('startDate').value=today();toggleCommitmentFields();if(id){const c=commitments.find(x=>x.id===id);if(c){$('commitmentType').value=c.type;$('commitmentName').value=c.name;$('commitmentAmount').value=c.amount;$('commitmentCategory').value=c.category;$('commitmentPayment').value=c.payment;$('commitmentDueDay').value=c.dueDay||10;$('fixedStartDate').value=c.startDate;$('startDate').value=c.startDate;$('totalInstallments').value=c.totalInstallments||12;toggleCommitmentFields()}}$('commitmentModal').classList.remove('hidden')}
function closeCommitmentModal(){$('commitmentModal').classList.add('hidden')}
$('commitmentType').onchange=toggleCommitmentFields;$('newCommitmentBtn').onclick=()=>openCommitmentModal();$('closeCommitmentModal').onclick=closeCommitmentModal;$('commitmentModal').onclick=e=>{if(e.target===$('commitmentModal'))closeCommitmentModal()};
$('commitmentForm').onsubmit=e=>{e.preventDefault();const id=$('commitmentId').value,type=$('commitmentType').value,name=$('commitmentName').value.trim(),amount=Number($('commitmentAmount').value),category=$('commitmentCategory').value,payment=$('commitmentPayment').value,dueDay=Math.min(31,Math.max(1,Number($('commitmentDueDay').value)||1)),startDate=type==='fixed'?$('fixedStartDate').value:$('startDate').value;if(!name||!amount||!startDate){toast('Completa los datos del compromiso');return}const d={type,name,amount,category,payment,dueDay,startDate,status:'active',updatedAt:Date.now()};if(type==='installment')d.totalInstallments=Math.max(1,Number($('totalInstallments').value)||1);if(id){const i=commitments.findIndex(x=>x.id===id);commitments[i]={...commitments[i],...d}}else commitments.push({id:crypto.randomUUID(),...d,createdAt:Date.now()});saveCommitments();closeCommitmentModal();render();toast('✓ Compromiso guardado')};
window.editCommitment=id=>openCommitmentModal(id);window.pauseCommitment=id=>{const c=commitments.find(x=>x.id===id);if(c&&confirm(`¿Pausar “${c.name}”? Dejará de descontar del presupuesto hasta reactivarlo.`)){c.status='paused';c.updatedAt=Date.now();saveCommitments();render();toast('Compromiso pausado')}};window.cancelCommitment=id=>{const c=commitments.find(x=>x.id===id);if(c&&confirm(`¿Cancelar “${c.name}”? Pasará al historial y dejará de descontar del presupuesto.`)){c.status='cancelled';c.updatedAt=Date.now();saveCommitments();render();toast('Compromiso cancelado')}};
function showCommitmentDetail(id){const c=commitments.find(x=>x.id===id);if(!c)return;const info=c.type==='installment'?installmentInfo(c):null;$('detailTitle').textContent=c.name;$('commitmentDetail').innerHTML=`<div class="commit-detail"><div class="detail-grid"><div class="detail-box"><span>Tipo</span><strong>${c.type==='fixed'?'Gasto fijo mensual':'Compra en cuotas'}</strong></div><div class="detail-box"><span>Estado</span><strong>${commitmentState(c)==='completed'?'Finalizado':commitmentState(c)==='cancelled'?'Cancelado':commitmentState(c)==='paused'?'Pausado':'Activo'}</strong></div><div class="detail-box"><span>${c.type==='fixed'?'Monto mensual':'Valor de cuota'}</span><strong>${money(c.amount)}</strong></div><div class="detail-box"><span>Categoría</span><strong>${catIcon(c.category)} ${esc(c.category)}</strong></div>${info?`<div class="detail-box"><span>Progreso</span><strong>${Math.min(Math.max(info.current,1),info.total)} de ${info.total}</strong></div><div class="detail-box"><span>Cuotas restantes</span><strong>${info.remaining}</strong></div>`:`<div class="detail-box"><span>Vencimiento</span><strong>Día ${c.dueDay}</strong></div>`}<div class="detail-box"><span>Medio de pago</span><strong>${esc(c.payment)}</strong></div><div class="detail-box"><span>Inicio</span><strong>${c.startDate}</strong></div></div>${info?`<p class="muted">${info.completed?'Este compromiso terminó y ya no descuenta del presupuesto. Permanece en el historial.':`Este mes descuenta ${money(c.amount)} del presupuesto. Al finalizar la cuota ${info.total}, desaparecerá automáticamente de los compromisos activos y pasará al historial.`}</p>`:`<p class="muted">Este gasto se descuenta del presupuesto todos los meses mientras permanezca activo.</p>`}<div class="detail-actions">${commitmentState(c)==='active'?`<button class="secondary-btn" onclick="editCommitment('${c.id}');closeDetailModal()">✏️ Editar</button><button class="secondary-btn" onclick="pauseCommitment('${c.id}');closeDetailModal()">⏸️ Pausar</button><button class="danger-btn" onclick="cancelCommitment('${c.id}');closeDetailModal()">Cancelar compromiso</button>`:''}</div></div>`;$('commitmentDetailModal').classList.remove('hidden')}
window.showCommitmentDetail=showCommitmentDetail;function closeDetailModal(){$('commitmentDetailModal').classList.add('hidden')}$('closeDetailModal').onclick=closeDetailModal;$('commitmentDetailModal').onclick=e=>{if(e.target===$('commitmentDetailModal'))closeDetailModal()};
document.querySelectorAll('[data-commit-tab]').forEach(b=>b.onclick=()=>{commitmentTab=b.dataset.commitTab;document.querySelectorAll('[data-commit-tab]').forEach(x=>x.classList.toggle('active',x===b));$('activeCommitments').classList.toggle('hidden',commitmentTab!=='active');$('commitmentHistory').classList.toggle('hidden',commitmentTab!=='history')});
populate();render();if('serviceWorker'in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
'''
js.write_text(newjs,encoding='utf-8')
# update manifest and sw cache/version
manifest=base/'manifest.json'
if manifest.exists():
    m=manifest.read_text(encoding='utf-8').replace('Mis Gastos v3','Mis Gastos').replace('mis-gastos-v3','mis-gastos-v5')
    manifest.write_text(m,encoding='utf-8')
sw=base/'sw.js'
if sw.exists():
    s=sw.read_text(encoding='utf-8').replace('v3','v5')
    sw.write_text(s,encoding='utf-8')
(base/'README.txt').write_text('''MIS GASTOS V5\n\nNovedades:\n- Gastos fijos mensuales activos que descuentan del presupuesto.\n- Compras en cuotas con seguimiento automático de cuota actual y cuotas restantes.\n- Las cuotas finalizadas desaparecen de Compromisos activos y quedan en Historial.\n- Compromisos pausados o cancelados quedan registrados en Historial.\n- El presupuesto disponible considera gastos normales + compromisos activos del mes.\n- Exportación/importación incluye gastos, presupuesto y compromisos.\n\nImportante: los compromisos se calculan de forma lógica y no duplican gastos en el historial de gastos normales.\n''',encoding='utf-8')
# zip
out=Path('/mnt/data/mis_gastos_v5.zip')
if out.exists(): out.unlink()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in base.iterdir():
        if p.is_file(): z.write(p,p.name)
print(out, out.stat().st_size)
