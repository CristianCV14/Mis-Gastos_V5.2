
/* MIS GASTOS V5.1 - PERIOD SELECTOR (ISOLATED)
   This module intentionally does not modify existing expense handlers.
*/
(function(){
  const KEY="mis_gastos_v51_selected_period";
  const today=new Date();
  const currentKey=()=>`${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,"0")}`;
  let period=localStorage.getItem(KEY)||currentKey();

  function parse(p){const [y,m]=p.split("-").map(Number);return new Date(y,m-1,1);}
  function key(d){return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`;}
  function shift(p,n){const d=parse(p);d.setMonth(d.getMonth()+n);return key(d);}
  function label(p){return parse(p).toLocaleDateString("es-ES",{month:"long",year:"numeric"}).replace(/^./,c=>c.toUpperCase());}
  function update(){
    const el=document.getElementById("v51PeriodLabel");
    if(el) el.textContent=label(period);
  }
  function set(p){
    period=p; localStorage.setItem(KEY,p); update();
    document.dispatchEvent(new CustomEvent("misgastos:periodchange",{detail:{period:p}}));
  }
  function init(){
    update();
    const prev=document.getElementById("v51PrevMonth");
    const next=document.getElementById("v51NextMonth");
    const now=document.getElementById("v51Today");
    if(prev)prev.addEventListener("click",()=>set(shift(period,-1)));
    if(next)next.addEventListener("click",()=>set(shift(period,1)));
    if(now)now.addEventListener("click",()=>set(currentKey()));
  }
  window.MisGastosPeriod={
    get:()=>period,
    set,
    previous:()=>set(shift(period,-1)),
    next:()=>set(shift(period,1))
  };
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});
  else init();
})();
