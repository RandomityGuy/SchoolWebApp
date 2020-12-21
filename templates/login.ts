const login_button = document.querySelector("#login_button") as HTMLButtonElement;
const username_text = document.querySelector("#username_text") as HTMLInputElement;
const password_text = document.querySelector("#password_text") as HTMLInputElement;


login_button.addEventListener("click",(e) => {
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