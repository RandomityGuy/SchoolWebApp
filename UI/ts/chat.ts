const popup_details_name = document.querySelector("#popup-user-detail-name") as HTMLDivElement;
const popup_details_class = document.querySelector("#popup-user-detail-class") as HTMLDivElement;
const popup_details_id = document.querySelector("#popup-user-detail-id") as HTMLDivElement;
const popup_details_avatar = document.querySelector("#popup-user-detail-avatar") as HTMLDivElement;
const popup_details_dm = document.querySelector("#popup-user-detail-add") as HTMLDivElement;
const channel_header = document.querySelector("#main-panel-profile-name") as HTMLDivElement;
const panel_profile = document.querySelector("#main-panel-profile") as HTMLDivElement;
const popup_details_back = document.querySelector("#popup-user-detail-back") as HTMLButtonElement;
const main_panel_messages = document.querySelector("#main-panel-messages") as HTMLDivElement;
const channel_list = document.querySelector("#channels") as HTMLDivElement;
const add_channel = document.querySelector("#add-channel") as HTMLDivElement;
const popup_channel_back = document.querySelector("#popup-add-channel-back") as HTMLButtonElement;
const popup_channel_submit = document.querySelector("#channel-user-submit") as HTMLInputElement;
const popup_channel_input = document.querySelector("#channel-user-id") as HTMLInputElement;
const send_button = document.querySelector("#main-input-button") as HTMLInputElement;
const send_box = document.querySelector("#main-input-message") as HTMLInputElement;

class Channel {
    id: string;
    name: string;
    flags: number;

    constructor(id: string, name: string, flags: number) {
        this.id = id;
        this.name = name;
        this.flags = flags;
    }
}

class ChannelMember {
    id: string;
    avatarurl: string;
    name: string;

    constructor(id: string, name: string, avatarurl: string) {
        this.id = id;
        this.name = name;
        this.avatarurl = avatarurl;
    }
}

let channels: Channel[] = null;
let channel_members: ChannelMember[] = null;
let current_channel: number = null;

let token: string = null;
let id: string = null;
let lastmsgid: string = null;

token = localStorage.getItem('token');
id = localStorage.getItem('id');
setChannelSidebar();

panel_profile.addEventListener('click', (e) => {
    if (channels[current_channel].flags != 0) {
        toggleUserDetails();
    }
});

popup_details_back.addEventListener('click', (e) => {
    toggleUserDetails();
});

popup_details_dm.addEventListener('click', (e) => {
    createDM(popup_details_id.textContent, false);
    toggleUserDetails();
});

add_channel.addEventListener('click', (e) => toggleAddChannel());

popup_channel_back.addEventListener('click', (e) => toggleAddChannel());

popup_channel_submit.addEventListener('click', (e) => {
    createDM(popup_channel_input.value);
});

send_button.addEventListener('click', (e) => {
    sendChatMessage(send_box.value);
    send_box.value = "";
});

send_box.addEventListener('keydown', (e) => {
    if (e.key == "Enter") {
        e.preventDefault();
        sendChatMessage(send_box.value);
        send_box.value = "";
    }
})

function toggleUserDetails() {
    document.getElementById('container').classList.toggle('disable');
    document.getElementById('popup-user-detail').classList.toggle('hide');
}

function setChannel(channel_index: number) {
    current_channel = channel_index;
    setChannelData();
    getChat();
}

function setChannelSidebar() {
    channel_list.innerHTML = "";
    fetch("/api/channels?" + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
        channels = [];
        let idx = 0;
        data.channels.forEach((element: { id: number; name: string; flags: number; }) => {
            channels.push(new Channel(element.id.toString(), element.name, element.flags));
            let channel_div = document.createElement('div');
            channel_div.className = "channel";
            channel_div.id = idx.toString();
            channel_div.dataset.id = element.id.toString();
            channel_div.addEventListener('mouseover', (e) => showBorder(channel_div));
            channel_div.addEventListener('mouseout', (e) => hideBorder(channel_div));
            channel_div.addEventListener('click', (e) => setChannel(parseInt(channel_div.id)));

            if ((element.flags & 1) == 1) {
                fetch(`/api/channels/${element.id}/users?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {

                    channel_members = [];
                    data.users.forEach((element: { id: number; name: string; avatarurl: string; }) => {
                        channel_members.push(new ChannelMember(element.id.toString(), element.name, element.avatarurl));
                    });
                    let is_in_channel = channel_members.find((c) => c.id == id) !== undefined;
                    if (is_in_channel) {
                        let other_member: ChannelMember = channel_members.find((c) => c.id != id);
                        channel_div.textContent = other_member.name;
                    } else {
                        let one = channel_members[0].name;
                        let two: string = null;
                        if (channel_members.length > 1) two = channel_members[1].name; else two = "Empty";
                        channel_div.textContent = `${one} - ${two}`;
                    }
                });
            } else {
                channel_div.textContent = element.name;
            }
            channel_list.appendChild(channel_div);
            idx++;

        });
        current_channel = 0;
        setChannelData();
        getChat();
    });
}

function setChannelData() {
    let channel = channels[current_channel];

    fetch(`/api/channels/${channel.id}/users?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {

        channel_members = [];
        data.users.forEach((element: { id: number; name: string; avatarurl: string; }) => {
            channel_members.push(new ChannelMember(element.id.toString(), element.name, element.avatarurl));
        });

        if ((channel.flags & 1) == 1) {
            let other_member: ChannelMember = channel_members.find((c) => c.id != id);
            popup_details_name.textContent = other_member.name;
            popup_details_id.textContent = other_member.id.toString();
            popup_details_avatar.style.backgroundImage = "url(" + other_member.avatarurl + ")";
            channel_header.textContent = other_member.name;

            fetch(`/api/users/${other_member.id}?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => { 
                popup_details_class.textContent = data.class; 
            });

            // popup_details_class.textContent <-- Add fetch
        } else if (channel.flags == 0) {
            channel_header.textContent = channel.name;
        }

     });
        
}

function getChat() {
    let channel = channels[current_channel];
    main_panel_messages.innerHTML = "";

    fetch(`/api/channels/${channel.id}/messages?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
        data.messages.forEach((element: { author: { name: any; id: any; avatarurl: any; }; id: any; messages: { content: any; }[]; }) => {
            let sender_name = element.author.name;
            let sender_id = element.author.id;
            let sender_avatar = element.author.avatarurl;
            let message_id = element.id;
            let message_content = element.messages[0].content;
            addChatMessage(sender_name, sender_id, sender_avatar, message_id, message_content);    
        });
        lastmsgid = data.lastmessageid;
    });
}

function showUserDetails(id: string) {
    fetch(`/api/users/${id}?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
        popup_details_id.textContent = data.id;
        popup_details_name.textContent = data.username;
        popup_details_avatar.style.backgroundImage = "url(" + data["avatar-url"] + ")";
        let perms = data.permissions;
        if (perms == 511) {
            popup_details_class.textContent = "PRINCIPAL | Staff"
        } else {
            popup_details_class.textContent = data.class;
        }
        toggleUserDetails();
    });
}

function createDM(id: string, doToggle: boolean = true) {
    fetch(`/api/users/${id}/DM?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
        let channel_id = parseInt(data.id);
        let channel_name = data.channel_name;
        let flags = parseInt(data.flags);

        let channel = new Channel(channel_id.toString(), channel_name, flags);
        channels.push(channel);

        setChannelSidebar();
        if (doToggle) toggleAddChannel();
    }, createDMError);
}

function createDMError() {
    popup_channel_input.classList.add("redBorders");
    popup_channel_input.value = "";
    popup_channel_input.placeholder = "Invalid User ID";
    popup_channel_input.addEventListener('click', createDMErrorEnd);
}

function createDMErrorEnd() {
    popup_channel_input.classList.remove("redBorders");
    popup_channel_input.placeholder = "User ID";
    popup_channel_input.removeEventListener('click', createDMErrorEnd);
}


function addChatMessage(sender_name: string, sender_id: string, sender_avatar: string, message_id: string, message_content: string, scroll: boolean = false) {
    let div = document.createElement('div');
    let metadata = document.createElement('metadata');
    let user = document.createElement('user');
    metadata.addEventListener('click', (e) => showUserDetails(sender_id));
    user.textContent = sender_name;
    let timestamp = document.createElement('timestamp');
    let utc = snowflakeToTimestamp(BigInt(message_id));
    timestamp.textContent = new Date(utc * 1000).toString();
    metadata.appendChild(user);
    metadata.appendChild(timestamp);
    div.appendChild(metadata);
    let msgdiv = document.createElement('div');
    msgdiv.id = "message";
    msgdiv.textContent = message_content;
    div.appendChild(msgdiv);
    
    if (sender_id != id) {
        div.id = "messages-recieved";
    } else {
        div.id = "messages-sent";
    }

    main_panel_messages.appendChild(div); 
    if (scroll) {
        main_panel_messages.scrollTop = main_panel_messages.scrollHeight;
    }
}

function sendChatMessage(content: string) {
    let body = { message: content };
    fetch(`/api/channels/${channels[current_channel].id}/messages?` + new URLSearchParams({ token: token.toString() }), {
        method: "POST",
        body: JSON.stringify(body),
        headers: { 'Content-Type': 'application/json' },
    }).then(e => updateChat(true));
}

function showBorder(element: HTMLDivElement) {
    element.classList.add('border');
}

function hideBorder(element: HTMLDivElement) {
  element.classList.remove('border');
}

function snowflakeToTimestamp(_id: bigint) {
    _id = _id >> BigInt(22);
    _id += BigInt(1142974214000);
    _id = _id / BigInt(1000);
    return Number(_id);
}

function toggleAddChannel() {
    document.getElementById('container').classList.toggle('disable');
    document.getElementById('popup-add-channel').classList.toggle('hide');
}

function updateChat(scroll: boolean = false) {
    fetch(`/api/channels/${channels[current_channel].id}/messages?after=${lastmsgid}&` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
        data.messages.forEach((element: { author: { name: any; id: any; avatarurl: any; }; id: any; messages: { content: any; }[]; }) => {
            let sender_name = element.author.name;
            let sender_id = element.author.id;
            let sender_avatar = element.author.avatarurl;
            let message_id = element.id;
            let message_content = element.messages[0].content;
            addChatMessage(sender_name, sender_id, sender_avatar, message_id, message_content, scroll);   
        });
        if (data.lastmessageid != -1) {
            lastmsgid = data.lastmessageid;
        }
    });
}

let update_interval = setInterval(updateChat, 3000);