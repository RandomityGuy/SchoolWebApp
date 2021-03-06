
var token: string;
var id: string;
var permissions: number;

var toAnnounceClasses: string[] = [];

const class_selector = document.querySelector("#class-selector-select-class") as HTMLSelectElement;
const class_selector_form = document.querySelector("#class-selector-form") as HTMLFormElement;
const announcementsdiv = document.querySelector("#announcements") as HTMLDivElement;

const createBackButton = document.querySelector("#create-back") as HTMLButtonElement;
const createCreateButton = document.querySelector("#create-create") as HTMLButtonElement;

const create_ann_checks = document.querySelector("#create-ann-check") as HTMLDivElement;
const create_ann_input = document.querySelector("#create-ann-input") as HTMLInputElement;

window.addEventListener('load', (e) => {
    token = localStorage.getItem('token');
    id = localStorage.getItem('id');
    permissions = Number.parseInt(localStorage.getItem('permissions'));

    if ((permissions & 1) == 1) {
        buildClassList();
    } else {
        buildAnnouncementList();
    }

    createBackButton.onclick = (e) => {
        e.preventDefault();
        togglePopup();
    }
    createCreateButton.onclick = (e) => {
        doAnnouncements(create_ann_input.value);
    }
    // buildAnnouncementList(id);
});

function buildClassList() {
    fetch("/api/classes?" + new URLSearchParams({ token: token.toString() })).then(e => e.json()).then(data => {
        class_selector.innerHTML = ``;
        class_selector_form.hidden = false;
        create_ann_checks.innerHTML = ``;
        data.forEach(studentclass => {
            let studentclassopt = document.createElement('option');
            studentclassopt.value = studentclass;
            studentclassopt.text = studentclass;
            class_selector.appendChild(studentclassopt);

            let chckbox = document.createElement('input');
            chckbox.type = 'checkbox';
            chckbox.id = chckbox.name = chckbox.value = studentclass;
            let label = document.createElement('label');
            label.htmlFor = studentclass;
            label.textContent = studentclass;
            create_ann_checks.appendChild(chckbox);
            create_ann_checks.appendChild(label);
            create_ann_checks.appendChild(document.createElement('br'));

            chckbox.onchange = () => {
                let val = chckbox.checked;
                if (chckbox.checked) {
                    if (!toAnnounceClasses.includes(chckbox.name))
                        toAnnounceClasses.push(chckbox.name);
                } else {
                    if (toAnnounceClasses.includes(chckbox.name))
                        toAnnounceClasses.splice(toAnnounceClasses.indexOf(chckbox.name), 1);
                }
            }
        });
        class_selector.onchange = () => buildAnnouncementListByClass(class_selector.value);
        buildAnnouncementListByClass(class_selector.value)
    })
}

function buildAnnouncementListByClass(studentclass: string) {
    fetch("/api/announcements?" + new URLSearchParams({ token: token.toString(), class: studentclass })).then(e => e.json()).then(data => {
        announcementsdiv.innerHTML = ``;
        data.forEach(announcement => {
            let anndiv = document.createElement('div');
            anndiv.className = 'a';
            let metadata = document.createElement('metadata');
            metadata.textContent = announcement.creator;
            let timestamp = document.createElement('timestamp');
            let utc = snowflakeToTimestamp(BigInt(announcement.id));
            timestamp.textContent = new Date(utc * 1000).toString();
            metadata.appendChild(timestamp);
            anndiv.appendChild(metadata);
            anndiv.appendChild(document.createElement('br'));
            let content = document.createElement('content');
            content.textContent = announcement.content;
            anndiv.appendChild(content);

            if ((permissions & 1) == 1) {
                let deletebutton = document.createElement('close');
                deletebutton.className = "close-1";
                deletebutton.textContent = "X";
                deletebutton.hidden = true;
                deletebutton.onclick = () => {
                    deleteAnnouncement(announcement.id);
                    announcementsdiv.removeChild(anndiv);
                }

                anndiv.appendChild(deletebutton);

                anndiv.onmouseenter = () => deletebutton.hidden = false;
                anndiv.onmouseleave = () => deletebutton.hidden = true;
            }

            announcementsdiv.appendChild(anndiv);
        })
        if ((permissions & 1) == 1) {
            let creatorbutton = document.createElement('button');
            creatorbutton.id = 'create-but';
            creatorbutton.onclick = togglePopup;
            creatorbutton.textContent = "New";
            announcementsdiv.appendChild(creatorbutton);
        }
    })
}

function buildAnnouncementList() {
    fetch("/api/announcements?" + new URLSearchParams({ token: token.toString() })).then(e => e.json()).then(data => {
        announcementsdiv.innerHTML = ``;
        data.forEach(announcement => {
            let anndiv = document.createElement('div');
            anndiv.className = 'a';
            let metadata = document.createElement('metadata');
            metadata.textContent = announcement.creator;
            let timestamp = document.createElement('timestamp');
            let utc = snowflakeToTimestamp(BigInt(announcement.id));
            timestamp.textContent = new Date(utc * 1000).toString();
            metadata.appendChild(timestamp);
            anndiv.appendChild(metadata);
            anndiv.appendChild(document.createElement('br'));
            let content = document.createElement('content');
            content.textContent = announcement.content;
            anndiv.appendChild(content);

            if ((permissions & 1) == 1) {
                let deletebutton = document.createElement('close');
                deletebutton.className = "close-1";
                deletebutton.textContent = "X";
                deletebutton.hidden = true;
                deletebutton.onclick = () => {
                    deleteAnnouncement(announcement.id);
                    announcementsdiv.removeChild(anndiv);
                }

                anndiv.appendChild(deletebutton);

                anndiv.onmouseenter = () => deletebutton.hidden = false;
                anndiv.onmouseleave = () => deletebutton.hidden = true;
            }

            announcementsdiv.appendChild(anndiv);
        })
        if ((permissions & 1) == 1) {
            let creatorbutton = document.createElement('button');
            creatorbutton.id = 'create-but';
            creatorbutton.onclick = togglePopup;
            creatorbutton.textContent = "New";
            announcementsdiv.appendChild(creatorbutton);
        }
    })
}

function deleteAnnouncement(id: string) {
    let body = { id: id };
    fetch(`/api/announcements?` + new URLSearchParams({ token: token.toString() }), {
        method: "DELETE",
        body: JSON.stringify(body),
        headers: { 'Content-Type': 'application/json' },
    });
}

function doAnnouncements(content: string) {
    toAnnounceClasses.forEach(studentclass => {
        let body = { content: content, class: studentclass };
        fetch(`/api/announcements?` + new URLSearchParams({ token: token.toString() }), {
            method: "POST",
            body: JSON.stringify(body),
            headers: { 'Content-Type': 'application/json' },
        });
    })
    buildAnnouncementListByClass(class_selector.value);
}

function snowflakeToTimestamp(_id: bigint) {
    _id = _id >> BigInt(22);
    _id += BigInt(1142974214000);
    _id = _id / BigInt(1000);
    return Number(_id);
}

function togglePopup() {
  document.getElementById('wrapper').classList.toggle('hide');
  document.getElementById('create').classList.toggle('hide');
}
