function finalizaProva(){
    const itemsDesativar  = document.getElementsByClassName('nao-funciona-ao-finalizar')
    for (let i = 0; i < itemsDesativar.length; i++) {
        itemsDesativar.disabled = true
        itemsDesativar[i].classList.add('css-nao-funciona-ao-finalizar')
    }
}
function carregaSegundoSelect(select1ou2){
    const tipoAcertoErro = document.getElementById(`tipoAcertoErro${select1ou2}`)
    const certoErrado = document.getElementById(`certoErrado${select1ou2}`)
    const selectLetra = document.getElementById(`letraMarcada${select1ou2}`)

    tipoAcertoErro.style.display = 'block'
   
    while(tipoAcertoErro.children.length> 1){
        tipoAcertoErro.removeChild(tipoAcertoErro.lastChild)
        selectLetra.removeChild(selectLetra.lastChild)
    }
    if (certoErrado.value == 'true'){
        selectLetra.style.display = 'none'

        let listaTiposCerto = ['certeza', 'duvida', 'chute']
        let options = []
        for(let i = 0; i < (listaTiposCerto).length; i++){
            options[i] = document.createElement('option')
            options[i].value = listaTiposCerto[i]
            options[i].innerText = listaTiposCerto[i]
            tipoAcertoErro.appendChild(options[i])
        }
        
    }
    else if (certoErrado.value == 'false'){

        selectLetra.style.display = 'block'
        let listaTiposCerto = ['atencao', 'conteudo', 'tempo']
        let listaLetras = ['A', 'B', 'C', 'D', 'E']
        

        let options = []
        let optionsLetra = []

        for(let i = 0; i < (listaTiposCerto).length; i++){
            options[i] = document.createElement('option')
            options[i].value = listaTiposCerto[i]
            options[i].innerText = listaTiposCerto[i]

          

            tipoAcertoErro.appendChild(options[i])
            
        }
        
        for(let i = 0; i < listaLetras.length; i++){
            optionsLetra[i]  = document.createElement('option')
            optionsLetra[i].value = listaLetras[i]
            optionsLetra[i].innerText = listaLetras[i]
            selectLetra.appendChild(optionsLetra[i])
        }
    }
        
}

function aperteiVoltar(){
    localStorage.setItem('aperteiVoltar', true)
    // defina que apertei o botão voltar para quando eu entrar aparece a tela no começo e não a onde tava antes )
}
function enviarFormulario(event, materia) {

    let tipoAcertoInput = document.querySelector(`.tipoAcertoInput${materia}`)
    let select = document.querySelector(`.select${materia}`)
    let letraErrei = document.querySelector(`.letraErrei${materia}`)

    if (tipoAcertoInput.value == "nada" && (select.value == "default" || letraErrei.value == "default")) {
        event.preventDefault()
        alert('Escolha uma opção')
    }
    else {


        let btnAcertei = document.querySelector(`.btnAcertei${materia}`)
        let btnErrei = document.querySelector(`.btnErrei${materia}`)



        document.getElementById(`formulario${materia}`).submit()

    }
}

function verificaTipo(tipo, materia) {

    document.querySelector(`.tipoAcertoInput${materia}`).value = tipo

    document.querySelector(`.btnEnviar${materia}`).click()

}

function revelaBotao(parametro) {

    let tipoAcerto = document.getElementsByClassName('tipoAcerto' + parametro)
    for (let i = 0; i < tipoAcerto.length; i++) {
        tipoAcerto[i].classList.remove('d-none');

    }


    document.querySelector(`.btnErrei${parametro}`).style.display = '6vw'
    document.querySelector(`.btnErrei${parametro}`).style.marginRight = '10px'
    let btnsErrei = document.getElementsByClassName('btnErrei')
    for (let i = 0; i < btnsErrei.length; i++) {
        btnsErrei[i].disabled = true
    }
}



function removeD_none(materia) {
    let btnsAcertei = document.getElementsByClassName('btnAcertei')
    for (let i = 0; i < btnsAcertei.length; i++) {
        btnsAcertei[i].disabled = true
    }
    document.querySelector(`.select${materia}`).classList.remove('d-none')
    document.querySelector(`.letraErrei${materia}`).classList.remove('d-none')
    document.querySelector(`.inputNumber${materia}`).classList.remove('d-none')

    document.querySelector(`.inputNumber${materia}`).classList.remove('d-none')


    document.querySelector(`.btnAcertei${materia}`).style.display = '6vw'
    document.querySelector(`.btnAcertei${materia}`).style.marginRight = '10px'

}

// Função do GPT para ao recarregar a página voltar para onde tava antes:
document.addEventListener("DOMContentLoaded", () => {
   

    const scrollPosition = localStorage.getItem('scrollPosition');
    const aperteiVoltar = localStorage.getItem('aperteiVoltar');
    if (scrollPosition &&  aperteiVoltar == null) {
      window.scrollTo(0, parseInt(scrollPosition, 10));
      localStorage.removeItem('scrollPosition'); // Limpa após usar
    }
    localStorage.removeItem('aperteiVoltar')
  });

  // Salvar a posição de rolagem antes de recarregar
  window.addEventListener('beforeunload', () => {
   
    localStorage.setItem('scrollPosition', window.scrollY);
  });

  function saveScrollPosition() {
      localStorage.setItem('scrollPosition', window.scrollY);
    }



