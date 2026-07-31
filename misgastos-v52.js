
/* MIS GASTOS V5.2 - PERIOD COMMITMENTS ENGINE */
(function(){
  const PERIOD_KEY="mis_gastos_v51_selected_period";
  const STATUS={ACTIVE:"active",PAUSED:"paused",FINISHED:"finished",CANCELLED:"cancelled"};

  function period(){
    return localStorage.getItem(PERIOD_KEY)||new Date().toISOString().slice(0,7);
  }
  function parts(p){const [y,m]=p.split("-").map(Number);return {y,m};}
  function monthIndex(p){const x=parts(p);return x.y*12+x.m;}
  function monthDiff(a,b){return monthIndex(b)-monthIndex(a);}
  function normalizeType(c){
    const t=String(c.type||c.kind||c.category||"").toLowerCase();
    if(t.includes("fixed")||t.includes("fijo")||t.includes("recurrent"))return "fixed";
    if(t.includes("install")||t.includes("cuot"))return "installment";
    return t;
  }
  function status(c){
    const s=String(c.status||c.state||"active").toLowerCase();
    if(["paused","pausado","pause"].includes(s))return STATUS.PAUSED;
    if(["cancelled","canceled","cancelado"].includes(s))return STATUS.CANCELLED;
    if(["finished","completed","finalizado","completado"].includes(s))return STATUS.FINISHED;
    return STATUS.ACTIVE;
  }
  function startPeriod(c){
    const raw=c.startDate||c.start||c.date||c.createdAt;
    if(!raw)return null;
    const m=String(raw).match(/^(\d{4})-(\d{2})/);
    return m?`${m[1]}-${m[2]}`:null;
  }
  function totalInstallments(c){
    return Number(c.installments||c.term||c.months||c.totalInstallments||0);
  }
  function installmentAmount(c,total){
    return Number(c.installmentAmount||c.monthlyAmount||c.amountPerInstallment||c.cuota||((Number(c.totalAmount||c.total||c.amount)||0)/(total||1))||0);
  }
  function getCommitments(){
    const candidates=["commitments","mis_gastos_commitments","gastosFijos","fixedExpenses","installments"];
    let all=[];
    for(const k of candidates){
      try{
        const v=JSON.parse(localStorage.getItem(k)||"null");
        if(Array.isArray(v)) all=all.concat(v.map(x=>({...x,_source:k})));
      }catch(e){}
    }
    // Deduplicate by stable id if available.
    const seen=new Set();
    return all.filter(c=>{
      const id=c.id||c._id;
      if(!id)return true;
      if(seen.has(String(id)))return false;
      seen.add(String(id)); return true;
    });
  }
  function getInstallmentInfo(c,p){
    const s=startPeriod(c), total=totalInstallments(c);
    if(!s||!total)return null;
    const d=monthDiff(s,p);
    // A paused commitment does not advance while paused. If pause/resume dates exist, calculate only active months.
    let effectiveIndex=d+1;
    if(c.pausedAt && c.resumedAt){
      const pauseP=String(c.pausedAt).slice(0,7), resumeP=String(c.resumedAt).slice(0,7);
      if(p>=pauseP && p<resumeP)return {paused:true};
      if(p>=resumeP)effectiveIndex=Math.max(1,effectiveIndex-Math.max(0,monthDiff(pauseP,resumeP)));
    } else if(status(c)===STATUS.PAUSED){
      return {paused:true};
    }
    if(effectiveIndex<1)return null;
    if(effectiveIndex>total)return {finished:true,total,amount:installmentAmount(c,total)};
    return {index:effectiveIndex,total,remaining:total-effectiveIndex,amount:installmentAmount(c,total)};
  }
  function activeForPeriod(c,p){
    const st=status(c), type=normalizeType(c);
    if(st===STATUS.CANCELLED||st===STATUS.FINISHED)return null;
    if(st===STATUS.PAUSED)return null;
    if(type==="fixed"){
      const s=startPeriod(c);
      const end=c.endDate?String(c.endDate).slice(0,7):null;
      if(s&&p<s)return null;
      if(end&&p>end)return null;
      return {type:"fixed",amount:Number(c.amount||c.monthlyAmount||c.value||0)};
    }
    if(type==="installment"){
      const info=getInstallmentInfo(c,p);
      if(!info||info.paused||info.finished)return null;
      return {type:"installment",...info};
    }
    return null;
  }
  function escape(s){return String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));}
  function money(n){return new Intl.NumberFormat("es-ES",{style:"currency",currency:"EUR",maximumFractionDigits:0}).format(Number(n)||0);}

  function render(){
    const p=period(), activeEl=document.getElementById("v52ActiveCommitments"), pausedEl=document.getElementById("v52PausedList"), totalEl=document.getElementById("v52CommitmentsTotal");
    if(!activeEl||!pausedEl)return;
    const cs=getCommitments(), active=[], paused=[];
    cs.forEach(c=>{
      const st=status(c), type=normalizeType(c);
      if(st===STATUS.PAUSED){paused.push(c);return;}
      const info=activeForPeriod(c,p);
      if(info)active.push({c,info});
    });
    let total=0;
    activeEl.innerHTML=active.length?active.map(({c,info})=>{
      total+=Number(info.amount)||0;
      const name=escape(c.name||c.title||c.description||"Compromiso");
      const id=escape(c.id||c._id||"");
      const detail=info.type==="installment"?`Cuota ${info.index} de ${info.total} · ${info.remaining} restantes`:`Gasto fijo mensual`;
      return `<div class="v52-card"><strong>${name}</strong><div class="v52-meta">${detail} · ${money(info.amount)}</div><div class="v52-actions"><button type="button" data-v52-pause="${id}">⏸️ Pausar</button><button type="button" data-v52-cancel="${id}">🔴 Cancelar</button></div></div>`;
    }).join(""):"<div class='v52-meta'>No hay compromisos activos para este período.</div>";
    pausedEl.innerHTML=paused.length?paused.map(c=>{
      const name=escape(c.name||c.title||c.description||"Compromiso"),id=escape(c.id||c._id||"");
      return `<div class="v52-card"><strong>${name}</strong><div class="v52-meta">⏸️ Pausado · no descuenta del presupuesto</div><div class="v52-actions"><button type="button" data-v52-resume="${id}">▶️ Reactivar</button><button type="button" data-v52-cancel="${id}">🔴 Cancelar</button></div></div>`;
    }).join(""):"<div class='v52-meta'>No hay compromisos pausados.</div>";
    if(totalEl)totalEl.textContent=money(total);
  }

  function findCommitment(id){
    return getCommitments().find(c=>String(c.id||c._id||"")===String(id));
  }
  function updateCommitment(c,patch){
    const keys=["commitments","mis_gastos_commitments","gastosFijos","fixedExpenses","installments"];
    for(const k of keys){
      try{
        const arr=JSON.parse(localStorage.getItem(k)||"null");
        if(!Array.isArray(arr))continue;
        let changed=false;
        const next=arr.map(x=>{
          if(String(x.id||x._id||"")===String(c.id||c._id||"")){changed=true;return {...x,...patch};}
          return x;
        });
        if(changed){localStorage.setItem(k,JSON.stringify(next));return true;}
      }catch(e){}
    }
    return false;
  }
  document.addEventListener("misgastos:periodchange",render);
  document.addEventListener("click",e=>{
    const pause=e.target.closest("[data-v52-pause]"), resume=e.target.closest("[data-v52-resume]"), cancel=e.target.closest("[data-v52-cancel]");
    if(pause||resume||cancel){
      const id=(pause||resume||cancel).dataset.v52Pause||(pause||resume||cancel).dataset.v52Resume||(pause||resume||cancel).dataset.v52Cancel;
      const c=findCommitment(id); if(!c)return;
      if(pause)updateCommitment(c,{status:STATUS.PAUSED,pausedAt:new Date().toISOString()});
      if(resume)updateCommitment(c,{status:STATUS.ACTIVE,resumedAt:new Date().toISOString()});
      if(cancel)updateCommitment(c,{status:STATUS.CANCELLED,cancelledAt:new Date().toISOString()});
      render();
    }
  });
  window.MisGastosV52={render,getCommitments,activeForPeriod,getInstallmentInfo};
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",render,{once:true});else render();
})();
