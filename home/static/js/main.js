let body = document.querySelector('body')
let fazzy = document.querySelector('.fazzy')
let icon = document.querySelector('.bi-moon-fill')

fazzy.addEventListener('click', ()=>{
    body.classList.toggle('dark')
    if(body.classList.contains('dark')){
        icon.classList.replace('bi-moon-fill', 'bi-sun-fill')
    }
    else{
        icon.classList.replace('bi-sun-fill', 'bi-moon-fill')
    }
})



