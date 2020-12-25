const login_continue = document.querySelector('#login_continue') as HTMLButtonElement;
const login_back = document.querySelector('#back') as HTMLButtonElement;

const username_text = document.querySelector("#username_text") as HTMLInputElement;
const password_text = document.querySelector("#pass") as HTMLInputElement;

const sign_in_button = document.querySelector("#signIn") as HTMLButtonElement;

login_continue.addEventListener('click',(e) => {
    signIn()
    attemptAutoSignIn()
})

login_back.addEventListener('click', (e) => {
    notSignIn()
})

sign_in_button.addEventListener('click', (e) => {
    attemptSignIn()
})

function signIn() {
    document.getElementById('middleBox').classList.toggle('middle-box-anim');
    document.getElementById('logoId').classList.toggle('logo-anim');
    document.getElementById('animbox').style.opacity = "0";
    document.getElementById('form').style.opacity = "1";
    document.getElementById('form').style.transitionDelay = "1s";
    document.getElementById('animbox').style.transitionDelay = "0ms"; 
    document.getElementById('animbox').style.pointerEvents = "none";   
    document.getElementById('form').style.pointerEvents = "auto";   
    
}

function notSignIn() {
    document.getElementById('middleBox').classList.toggle('middle-box-anim');
    document.getElementById('logoId').classList.toggle('logo-anim');
    document.getElementById('animbox').style.opacity = "1";
    document.getElementById('form').style.opacity = "0";
    document.getElementById('form').style.transitionDelay = "0ms";
    document.getElementById('animbox').style.transitionDelay = "0.7s";  
    document.getElementById('form').style.pointerEvents = "none";
    document.getElementById('animbox').style.pointerEvents = "auto";   
}

function attemptAutoSignIn() {
    let tok = localStorage.getItem('token');
    let body = { token: tok };
    if (tok !== null) {
        fetch('./api/authorizetoken', {
            method: "POST",
            body: JSON.stringify(body),
            headers: { 'Content-Type': 'application/json' },
        }).then((e) => {
            if (e.status != 403) {
                onSignIn();
            }
        }, (f) => onError());
    }
}

function attemptSignIn() {
    let username = username_text.value;
    let password = password_text.value;

    let body = { username: username, pwd: password };

    fetch('./api/authorize', {
        method: "POST",
        body: JSON.stringify(body),
        headers: {'Content-Type': 'application/json'},
    }).then((e) => {
        if (e.status != 403) {
            e.json().then(resp => {
                localStorage.setItem('token', resp.token);
                onSignIn()
            });
        } else {
            onError();
        }
    }, (f) => onError());
}

function onSignIn() {
    window.location.href = 'home';
    // Do whatever you want here after sign in
}

function onError() {
    username_text.classList.add('redBorders');
    password_text.classList.add('redBorders');
    username_text.placeholder = "Invalid credentials";
    username_text.value = "";
    password_text.placeholder = "Invalid credentials";
    password_text.value = "";
    username_text.addEventListener('click', onErrorEnd);
    password_text.addEventListener('click', onErrorEnd);

}

function onErrorEnd() {
    username_text.classList.remove('redBorders');
    password_text.classList.remove('redBorders');
    username_text.placeholder = "Username";
    password_text.placeholder = "Password";
    username_text.removeEventListener('click', onErrorEnd);
    password_text.removeEventListener('click', onErrorEnd);

}