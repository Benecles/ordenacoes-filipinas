(function(){
  var hero=document.getElementById('a17-release42-hero');
  if(hero){
    var scale=hero.querySelector('.a17-scale');
    var outcome=hero.querySelector('#a17-hero-outcome');
    var doubt=hero.querySelector('.a17-doubt');
    var pans=hero.querySelectorAll('.a17-pan');
    var resetTimer;
    pans.forEach(function(button){
      button.addEventListener('click',function(){
        var claimant=button.dataset.side==='claimant';
        if(resetTimer) window.clearTimeout(resetTimer);
        scale.dataset.choice=claimant?'claimant':'defendant';
        pans.forEach(function(pan){pan.setAttribute('aria-pressed',String(pan===button));});
        var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if(claimant){
          doubt.style.transform='translate(-194px,100px)';
        }else if(reduced){
          delete scale.dataset.choice;
          doubt.style.transform='translate(0,0)';
        }else{
          doubt.style.transform='translate(194px,100px)';
          resetTimer=window.setTimeout(function(){
            if(scale.dataset.choice==='defendant'){
              delete scale.dataset.choice;
              doubt.style.transform='translate(0,0)';
            }
          },650);
        }
        outcome.textContent=claimant
          ? 'A dúvida sobre o fato constitutivo pesa contra quem pede.'
          : 'A dúvida sobre o fato constitutivo pesa contra quem pede, não contra quem se defende.';
        outcome.hidden=false;
      });
    });
  }
  var form=document.getElementById('a17-controls');
  if(!form)return;
  var result=document.getElementById('a17-result');
  var title=result.querySelector('.a17-result__title');
  var note=result.querySelector('.a17-result__text');
  function update(){
    var fact=form.elements.fato.value;
    var holder=fact==='constitutivo'?'autor':'réu';
    var basis=form.elements.hipotese.value;
    var reasoned=form.elements.fundamentada.checked;
    var opportunity=form.elements.oportunidade.checked;
    var feasible=form.elements.cumprivel.value;
    result.dataset.state='default';
    if(basis==='nenhuma'){
      title.textContent='Mantém-se a regra do caput';
      note.textContent='O ônus ordinário cabe ao '+holder+' para este fato.';
      return;
    }
    if(feasible==='nao'){
      result.dataset.state='blocked';
      title.textContent='Transferência vedada pelo § 2º';
      note.textContent='O encargo que a parte receberia seria impossível ou excessivamente difícil de cumprir.';
      return;
    }
    if(!reasoned||!opportunity){
      title.textContent='Mantém-se a regra do caput';
      note.textContent='O § 1º exige decisão fundamentada e oportunidade para a parte se desincumbir do encargo.';
      return;
    }
    result.dataset.state='redistributed';
    title.textContent='Redistribuição fundamentada com oportunidade';
    note.textContent='A nova atribuição depende da hipótese selecionada, da razão exposta e da chance de produzir a prova.';
  }
  form.addEventListener('change',update);
  update();
})();
