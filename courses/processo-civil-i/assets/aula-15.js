(function(){
  var group=document.getElementById('a15-triage');
  if(!group)return;
  var result=document.getElementById('a15-triage-result');
  if(!result)return;
  group.querySelectorAll('input[name="a15-witness-question"]').forEach(function(input){
    input.addEventListener('change',function(){
      if(input.value==='text'){
        result.className='result lim';
        result.innerHTML='<strong>Limite do art. 443, I.</strong> A decisão já identifica a alegação no item 15; a testemunha repetiria o fato textual documentado.';
      }else{
        result.className='result dec';
        result.innerHTML='<strong>O inciso I, sozinho, não barra esta pergunta.</strong> As tentativas externas são outra proposição; a admissibilidade ainda depende dos demais filtros.';
      }
    });
  });
})();
