


// ====================================================================
// Função que apaga a mensagem da tela 2,5 segunto depois
// ====================================================================
  setTimeout(function () {
    document.getElementById("erro").style.display = "none";
      }, 2500);
    function hide(){
      document.getElementById("erro").style.display = "none";
      }
// ====================================================================



  function sair_add(){
    const numberPaginas = window.history.length * -1 ;
    console.log("oi isso é um console log");
    alert(numberPaginas, 'Alguém clicou no botão!');
      history.go(numberPaginas);
    };


