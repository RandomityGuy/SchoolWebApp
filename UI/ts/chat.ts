const popup_details_name = document.querySelector("#popup-user-detail-name") as HTMLDivElement;
const popup_details_class = document.querySelector("#popup-user-detail-class") as HTMLDivElement;
const popup_details_id = document.querySelector("#popup-user-detail-id") as HTMLDivElement;
const popup_details_avatar = document.querySelector("#popup-user-detail-avatar") as HTMLDivElement;
const channel_header = document.querySelector("#main-panel-profile-name") as HTMLDivElement;
const panel_profile = document.querySelector("#main-panel-profile") as HTMLDivElement;
const popup_details_back = document.querySelector("#popup-user-detail-back") as HTMLButtonElement;
const main_panel_messages = document.querySelector("#main-panel-messages") as HTMLDivElement;
const channel_list = document.querySelector("#channels") as HTMLDivElement;

class Channel {
    id: number;
    name: string;
    flags: number;

    constructor(id: number, name: string, flags: number) {
        this.id = id;
        this.name = name;
        this.flags = flags;
    }
}

class ChannelMember {
    id: number;
    avatarurl: string;
    name: string;

    constructor(id: number, name: string, avatarurl: string) {
        this.id = id;
        this.name = name;
        this.avatarurl = avatarurl;
    }
}

let channels: Channel[] = null;
let channel_members: ChannelMember[] = null;
let current_channel: number = null;

let token: string = null;
let id: number = null;

token = localStorage.getItem('token');
id = parseInt(localStorage.getItem('id'));
fetch("/api/channels?" + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
    channels = [];
    let idx = 0;
    data.channels.forEach((element: { id: number; name: string; flags: number; }) => {
        channels.push(new Channel(element.id, element.name, element.flags));
        let channel_div = document.createElement('div');
        channel_div.className = "channel";
        channel_div.id = idx.toString();
        channel_div.dataset.id = element.id.toString();
        channel_div.addEventListener('mouseover', (e) => showBorder(channel_div));
        channel_div.addEventListener('mouseout', (e) => hideBorder(channel_div));
        channel_div.addEventListener('click', (e) => set_channel(parseInt(channel_div.id)));

        channel_div.innerHTML = element.name;
        channel_list.appendChild(channel_div);
        idx++;

    });
    current_channel = 0;
    set_channel_data();
    get_chat();
});

panel_profile.addEventListener('click', (e) => {
    toggleUserDetails();
});

popup_details_back.addEventListener('click', (e) => {
    toggleUserDetails();
});

function toggleUserDetails() {
  document.getElementById('container').classList.toggle('disable');
  document.getElementById('popup-user-detail').classList.toggle('hide');
}

function set_channel(channel_index: number) {
    current_channel = channel_index;
    set_channel_data();
    get_chat();
}

function set_channel_data() {
    let channel = channels[current_channel];

    fetch(`/api/channels/${channel.id}/users?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {

        channel_members = [];
        data.users.forEach((element: { id: number; name: string; avatarurl: string; }) => {
            channel_members.push(new ChannelMember(element.id, element.name, element.avatarurl));
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

function get_chat() {
    let channel = channels[current_channel];
    main_panel_messages.innerHTML = "";

    fetch(`/api/channels/${channel.id}/messages?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
        data.messages.forEach((element: { author: { name: any; id: any; avatarurl: any; }; id: any; messages: { content: any; }[]; }) => {
            let sender_name = element.author.name;
            let sender_id = element.author.id;
            let sender_avatar = element.author.avatarurl;
            let message_id = element.id;
            let message_content = element.messages[0].content;

            let div = document.createElement('div');
            let metadata = document.createElement('metadata');
            let user = document.createElement('user');
            metadata.addEventListener('click', (e) => show_user_details(sender_id));
            user.textContent = sender_name;
            let timestamp = document.createElement('timestamp');
            let utc = snowflake_to_timestamp(BigInt(message_id));
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
        });
    });
}

function show_user_details(id: number) {
    fetch(`/api/users/${id}?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
        popup_details_id.textContent = data.id;
        popup_details_name.textContent = data.username;
        popup_details_avatar.style.backgroundImage = "url(" + data["avatar-url"] + ")";
        popup_details_class.textContent = data.class;
        toggleUserDetails();
    });
}

function showBorder(element: HTMLDivElement) {
    element.classList.add('border');
}

function hideBorder(element: HTMLDivElement) {
  element.classList.remove('border');
}

function snowflake_to_timestamp(_id: bigint) {
    _id = _id >> BigInt(22);
    _id += BigInt(1142974214000);
    _id = _id / BigInt(1000);
    return Number(_id);
}