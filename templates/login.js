(function () {
    'use strict';

    const login_button = document.querySelector("#login_button");
    const username_text = document.querySelector("#username_text");
    const password_text = document.querySelector("#password_text");
    login_button.addEventListener("click", (e) => {
        let username = username_text.value;
        let password = password_text.value;
        let body = { usernname: username, pwd: password };
        fetch('./api/authorize', {
            method: "POST",
            body: JSON.stringify(body)
        }).then((e) => {
            if (e.status != 403) {
                e.json().then(resp => {
                    localStorage.setItem('token', resp.token);
                });
            }
        });
    });

}());
