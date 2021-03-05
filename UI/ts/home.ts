const user_details_name = document.querySelector("#user-details-name-div") as HTMLDivElement;
const user_details_class = document.querySelector("#user-details-class-div") as HTMLDivElement;
const user_details_id = document.querySelector("#user-details-id-div") as HTMLDivElement;
const user_details_avatar = document.querySelector("#user-details-avatar") as HTMLDivElement;
const logout_button = document.querySelector("#logout") as HTMLButtonElement;
const chat_button = document.querySelector('#chat-button') as HTMLButtonElement;
const announcements_button = document.querySelector("#announcements-button") as HTMLDivElement;

window.addEventListener('load', (e) => {
    populateUserDetails();
});

logout_button.addEventListener('click', (e) => {
    localStorage.removeItem('token');
    localStorage.removeItem('id');
    window.location.href = '/';
});

chat_button.addEventListener('click', (e) => {
    window.location.href = 'chat';
})

announcements_button.addEventListener('click', (e) => {
    window.location.href = 'announcements';
})

function populateUserDetails() {
    let tok = localStorage.getItem('token');

    fetch("/api/users/@me?" + new URLSearchParams({ token: tok.toString() })).then(response => response.json()).then(data => {
        user_details_id.textContent = "ID: " + data.id.toString();
        user_details_class.textContent = data.class;
        user_details_name.textContent = data.username;
        user_details_avatar.style.backgroundImage = "url(" + data["avatar-url"] + ")";

        localStorage.setItem('id', data.id.toString());

        let perms = data.permissions;
        if (perms == 511) {
            user_details_class.textContent = "PRINCIPAL | Staff"
        }
    });
}
