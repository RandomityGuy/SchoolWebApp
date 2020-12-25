(function () {
  'use strict';

  const popup_details_name = document.querySelector("#popup-user-detail-name");
  const popup_details_class = document.querySelector("#popup-user-detail-class");
  const popup_details_id = document.querySelector("#popup-user-detail-id");
  const popup_details_avatar = document.querySelector("#popup-user-detail-avatar");
  const channel_header = document.querySelector("#main-panel-profile-name");
  const panel_profile = document.querySelector("#main-panel-profile");
  const popup_details_back = document.querySelector("#popup-user-detail-back");
  const main_panel_messages = document.querySelector("#main-panel-messages");
  const channel_list = document.querySelector("#channels");
  const add_channel = document.querySelector("#add-channel");
  const popup_channel_back = document.querySelector("#popup-add-channel-back");
  const popup_channel_submit = document.querySelector("#channel-user-submit");
  const popup_channel_input = document.querySelector("#channel-user-id");
  const send_button = document.querySelector("#main-input-button");
  const send_box = document.querySelector("#main-input-message");
  class Channel {
      constructor(id, name, flags) {
          this.id = id;
          this.name = name;
          this.flags = flags;
      }
  }
  class ChannelMember {
      constructor(id, name, avatarurl) {
          this.id = id;
          this.name = name;
          this.avatarurl = avatarurl;
      }
  }
  let channels = null;
  let channel_members = null;
  let current_channel = null;
  let token = null;
  let id = null;
  let lastmsgid = null;
  token = localStorage.getItem('token');
  id = localStorage.getItem('id');
  set_channel_sidebar();
  panel_profile.addEventListener('click', (e) => {
      toggleUserDetails();
  });
  popup_details_back.addEventListener('click', (e) => {
      toggleUserDetails();
  });
  add_channel.addEventListener('click', (e) => toggleAddChannel());
  popup_channel_back.addEventListener('click', (e) => toggleAddChannel());
  popup_channel_submit.addEventListener('click', (e) => {
      create_dm(parseInt(popup_channel_input.value));
  });
  send_button.addEventListener('click', (e) => {
      send_chat_message(send_box.value);
      send_box.value = "";
  });
  send_box.addEventListener('keydown', (e) => {
      if (e.key == "Enter") {
          e.preventDefault();
          send_chat_message(send_box.value);
          send_box.value = "";
      }
  });
  function toggleUserDetails() {
      if (channels[current_channel].flags != 0) {
          document.getElementById('container').classList.toggle('disable');
          document.getElementById('popup-user-detail').classList.toggle('hide');
      }
  }
  function set_channel(channel_index) {
      current_channel = channel_index;
      set_channel_data();
      get_chat();
  }
  function set_channel_sidebar() {
      channel_list.innerHTML = "";
      fetch("/api/channels?" + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
          channels = [];
          let idx = 0;
          data.channels.forEach((element) => {
              channels.push(new Channel(element.id.toString(), element.name, element.flags));
              let channel_div = document.createElement('div');
              channel_div.className = "channel";
              channel_div.id = idx.toString();
              channel_div.dataset.id = element.id.toString();
              channel_div.addEventListener('mouseover', (e) => showBorder(channel_div));
              channel_div.addEventListener('mouseout', (e) => hideBorder(channel_div));
              channel_div.addEventListener('click', (e) => set_channel(parseInt(channel_div.id)));
              if ((element.flags & 1) == 1) {
                  fetch(`/api/channels/${element.id}/users?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
                      channel_members = [];
                      data.users.forEach((element) => {
                          channel_members.push(new ChannelMember(element.id.toString(), element.name, element.avatarurl));
                      });
                      let is_in_channel = channel_members.find((c) => c.id == id) !== undefined;
                      if (is_in_channel) {
                          let other_member = channel_members.find((c) => c.id != id);
                          channel_div.textContent = other_member.name;
                      }
                      else {
                          let one = channel_members[0].name;
                          let two = null;
                          if (channel_members.length > 1)
                              two = channel_members[1].name;
                          else
                              two = "Empty";
                          channel_div.textContent = `${one} - ${two}`;
                      }
                  });
              }
              else {
                  channel_div.textContent = element.name;
              }
              channel_list.appendChild(channel_div);
              idx++;
          });
          current_channel = 0;
          set_channel_data();
          get_chat();
      });
  }
  function set_channel_data() {
      let channel = channels[current_channel];
      fetch(`/api/channels/${channel.id}/users?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
          channel_members = [];
          data.users.forEach((element) => {
              channel_members.push(new ChannelMember(element.id.toString(), element.name, element.avatarurl));
          });
          if ((channel.flags & 1) == 1) {
              let other_member = channel_members.find((c) => c.id != id);
              popup_details_name.textContent = other_member.name;
              popup_details_id.textContent = other_member.id.toString();
              popup_details_avatar.style.backgroundImage = "url(" + other_member.avatarurl + ")";
              channel_header.textContent = other_member.name;
              fetch(`/api/users/${other_member.id}?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
                  popup_details_class.textContent = data.class;
              });
              // popup_details_class.textContent <-- Add fetch
          }
          else if (channel.flags == 0) {
              channel_header.textContent = channel.name;
          }
      });
  }
  function get_chat() {
      let channel = channels[current_channel];
      main_panel_messages.innerHTML = "";
      fetch(`/api/channels/${channel.id}/messages?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
          data.messages.forEach((element) => {
              let sender_name = element.author.name;
              let sender_id = element.author.id;
              let sender_avatar = element.author.avatarurl;
              let message_id = element.id;
              let message_content = element.messages[0].content;
              add_chat_message(sender_name, sender_id, sender_avatar, message_id, message_content);
          });
          lastmsgid = data.lastmessageid;
      });
  }
  function show_user_details(id) {
      fetch(`/api/users/${id}?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
          popup_details_id.textContent = data.id;
          popup_details_name.textContent = data.username;
          popup_details_avatar.style.backgroundImage = "url(" + data["avatar-url"] + ")";
          let perms = data.permissions;
          if (perms == 511) {
              popup_details_class.textContent = "PRINCIPAL | Staff";
          }
          else {
              popup_details_class.textContent = data.class;
          }
          toggleUserDetails();
      });
  }
  function create_dm(id) {
      fetch(`/api/users/${id}/DM?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
          let channel_id = parseInt(data.id);
          let channel_name = data.channel_name;
          let flags = parseInt(data.flags);
          let channel = new Channel(channel_id.toString(), channel_name, flags);
          channels.push(channel);
          set_channel_sidebar();
          toggleAddChannel();
      }, create_dm_error);
  }
  function create_dm_error() {
      popup_channel_input.classList.add("redBorders");
      popup_channel_input.value = "";
      popup_channel_input.placeholder = "Invalid User ID";
      popup_channel_input.addEventListener('click', create_dm_error_end);
  }
  function create_dm_error_end() {
      popup_channel_input.classList.remove("redBorders");
      popup_channel_input.placeholder = "User ID";
      popup_channel_input.removeEventListener('click', create_dm_error_end);
  }
  function add_chat_message(sender_name, sender_id, sender_avatar, message_id, message_content, scroll = false) {
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
      }
      else {
          div.id = "messages-sent";
      }
      main_panel_messages.appendChild(div);
      if (scroll) {
          main_panel_messages.scrollTop = main_panel_messages.scrollHeight;
      }
  }
  function send_chat_message(content) {
      let body = { message: content };
      fetch(`/api/channels/${channels[current_channel].id}/messages?` + new URLSearchParams({ token: token.toString() }), {
          method: "POST",
          body: JSON.stringify(body),
          headers: { 'Content-Type': 'application/json' },
      }).then(e => update_chat(true));
  }
  function showBorder(element) {
      element.classList.add('border');
  }
  function hideBorder(element) {
      element.classList.remove('border');
  }
  function snowflake_to_timestamp(_id) {
      _id = _id >> BigInt(22);
      _id += BigInt(1142974214000);
      _id = _id / BigInt(1000);
      return Number(_id);
  }
  function toggleAddChannel() {
      document.getElementById('container').classList.toggle('disable');
      document.getElementById('popup-add-channel').classList.toggle('hide');
  }
  function update_chat(scroll = false) {
      fetch(`/api/channels/${channels[current_channel].id}/messages?after=${lastmsgid}&` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
          data.messages.forEach((element) => {
              let sender_name = element.author.name;
              let sender_id = element.author.id;
              let sender_avatar = element.author.avatarurl;
              let message_id = element.id;
              let message_content = element.messages[0].content;
              add_chat_message(sender_name, sender_id, sender_avatar, message_id, message_content, scroll);
          });
          if (data.lastmessageid != -1) {
              lastmsgid = data.lastmessageid;
          }
      });
  }
  let update_interval = setInterval(update_chat, 3000);

}());
