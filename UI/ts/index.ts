const login_continue = document.querySelector('#login_continue') as HTMLButtonElement;
const login_back = document.querySelector('#back') as HTMLButtonElement;

login_continue.addEventListener('click',(e) => {
    sign_in()
})

login_back.addEventListener('click', (e) => {
    not_sign_in()
})


function sign_in() {
    document.getElementById('middleBox').classList.toggle('middle-box-anim');
    document.getElementById('logoId').classList.toggle('logo-anim');
    document.getElementById('animbox').style.opacity = "0";
    document.getElementById('form').style.opacity = "1";
    document.getElementById('form').style.transitionDelay = "1s";
    document.getElementById('animbox').style.transitionDelay = "0ms"; 
    document.getElementById('animbox').style.pointerEvents = "none";   
    document.getElementById('form').style.pointerEvents = "auto";   
    
}

function not_sign_in() {
    document.getElementById('middleBox').classList.toggle('middle-box-anim');
    document.getElementById('logoId').classList.toggle('logo-anim');
    document.getElementById('animbox').style.opacity = "1";
    document.getElementById('form').style.opacity = "0";
    document.getElementById('form').style.transitionDelay = "0ms";
    document.getElementById('animbox').style.transitionDelay = "0.7s";  
    document.getElementById('form').style.pointerEvents = "none";
    document.getElementById('animbox').style.pointerEvents = "auto";   
}