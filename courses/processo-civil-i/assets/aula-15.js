(function(){
  var group=document.getElementById('a15-triage');
  if(!group)return;
  var result=document.getElementById('a15-triage-result');
  if(!result)return;
  group.querySelectorAll('input[name="a15-witness-question"]').forEach(function(input){
    input.addEventListener('change',function(){
      if(input.value==='text'){
        result.className='result lim';
        result.innerHTML='<span class="runin">Limite do art. 443, I.</span> A decisão já identifica a alegação no item 15; a testemunha repetiria o fato textual documentado.';
      }else{
        result.className='result dec';
        result.innerHTML='<span class="runin">O inciso I, sozinho, não barra esta pergunta.</span> As tentativas externas são outra proposição; a admissibilidade ainda depende dos demais filtros.';
      }
    });
  });
})();
