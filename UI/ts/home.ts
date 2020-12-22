const user_details_name = document.querySelector("#user-details-name-div") as HTMLDivElement;
const user_details_class = document.querySelector("#user-details-class-div") as HTMLDivElement;
const user_details_id = document.querySelector("#user-details-id-div") as HTMLDivElement;
const user_details_avatar = document.querySelector("#user-details-avatar") as HTMLDivElement;

window.addEventListener('load', (e) => {
    populate_user_details();
});

export function populate_user_details() {
    let tok = localStorage.getItem('token');

    fetch("/api/users/@me?" + new URLSearchParams({ token: tok.toString() })).then(response => response.json()).then(data => {
        user_details_id.textContent = "ID: " + data.id.toString();
        user_details_class.textContent = data.class;
        user_details_name.textContent = data.username;
        user_details_avatar.style.backgroundImage = "url(" + data["avatar-url"] + ")";

        let perms = data.permissions;
        if (perms == 511) {
            user_details_class.textContent = "PRINCIPAL | Staff"
        }
    });
}
