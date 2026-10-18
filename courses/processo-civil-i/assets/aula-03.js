(function(){
  var form=document.getElementById('a03-questions');
  if(!form)return;
  var result=document.getElementById('a03-result');
  var combinations={
    'necessaria-unitario':'Litisconsórcio necessário e unitário: todos devem participar, e o mérito deve ser uniforme.',
    'necessaria-simples':'Litisconsórcio necessário e simples: todos devem participar, e o mérito pode variar para cada um.',
    'facultativa-unitario':'Litisconsórcio facultativo e unitário: a reunião é opcional, mas o mérito deve ser uniforme.',
    'facultativa-simples':'Litisconsórcio facultativo e simples: a reunião é opcional, e o mérito pode variar para cada um.'
  };
  function update(){
    var data=new FormData(form);
    var participacao=data.get('participacao');
    var uniformidade=data.get('uniformidade');
    if(!participacao||!uniformidade){
      result.textContent='Selecione uma resposta para cada pergunta.';
      return;
    }
    var key=participacao+'-'+uniformidade;
    result.textContent=(key==='facultativa-simples'?'Gustavo: ':'')+combinations[key];
  }
  form.addEventListener('change',update);
  update();
})();
