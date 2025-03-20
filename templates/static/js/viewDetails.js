function selecionarErros(){
    const titulo = document.querySelector('.titulo')
    const prova = "{{prova}}"
    titulo.innerHTML =  `<h1 class="titulo">ANALISE PROVA DA ${prova}  - acertos</h1>`
    
}
function selecionarAcertos(){
    const titulo = document.querySelector('.titulo')
    const prova = document.getElementById('provaValue')

    titulo.innerHTML =  `<h1 class="titulo">ANALISE PROVA DA ${prova} - erros </h1>`
    
}