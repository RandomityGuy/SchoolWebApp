(function () {
    'use strict';

    const login_continue = document.querySelector('#login_continue');
    const login_back = document.querySelector('#back');
    const username_text = document.querySelector("#username_text");
    const password_text = document.querySelector("#pass");
    const sign_in_button = document.querySelector("#signIn");
    login_continue.addEventListener('click', (e) => {
        sign_in();
        attempt_auto_sign_in();
    });
    login_back.addEventListener('click', (e) => {
        not_sign_in();
    });
    sign_in_button.addEventListener('click', (e) => {
        attempt_sign_in();
    });
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
    function attempt_auto_sign_in() {
        let tok = localStorage.getItem('token');
        let body = { token: tok };
        if (tok !== null) {
            fetch('./api/authorizetoken', {
                method: "POST",
                body: JSON.stringify(body),
                headers: { 'Content-Type': 'application/json' },
            }).then((e) => {
                if (e.status != 403) {
                    on_sign_in();
                }
            }, (f) => on_error());
        }
    }
    function attempt_sign_in() {
        let username = username_text.value;
        let password = password_text.value;
        let body = { username: username, pwd: password };
        fetch('./api/authorize', {
            method: "POST",
            body: JSON.stringify(body),
            headers: { 'Content-Type': 'application/json' },
        }).then((e) => {
            if (e.status != 403) {
                e.json().then(resp => {
                    localStorage.setItem('token', resp.token);
                    on_sign_in();
                });
            }
            else {
                on_error();
            }
        }, (f) => on_error());
    }
    function on_sign_in() {
        window.location.href = 'home';
        // Do whatever you want here after sign in
    }
    function on_error() {
        username_text.classList.add('redBorders');
        password_text.classList.add('redBorders');
        username_text.placeholder = "Invalid credentials";
        username_text.value = "";
        password_text.placeholder = "Invalid credentials";
        password_text.value = "";
        username_text.addEventListener('click', on_error_end);
        password_text.addEventListener('click', on_error_end);
    }
    function on_error_end() {
        username_text.classList.remove('redBorders');
        password_text.classList.remove('redBorders');
        username_text.placeholder = "Username";
        password_text.placeholder = "Password";
        username_text.removeEventListener('click', on_error_end);
        password_text.removeEventListener('click', on_error_end);
    }

}());
