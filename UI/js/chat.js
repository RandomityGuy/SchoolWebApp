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
  token = localStorage.getItem('token');
  id = parseInt(localStorage.getItem('id'));
  fetch("/api/channels?" + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
      channels = [];
      let idx = 0;
      data.channels.forEach(element => {
          channels.push(new Channel(element.id, element.name, element.flags));
          let channel_div = document.createElement('div');
          channel_div.className = "channel";
          channel_div.id = idx.toString();
          channel_div.dataset.id = element.id;
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
  function set_channel(channel_index) {
      current_channel = channel_index;
      set_channel_data();
      get_chat();
  }
  function set_channel_data() {
      let channel = channels[current_channel];
      fetch(`/api/channels/${channel.id}/users?` + new URLSearchParams({ token: token.toString() })).then(response => response.json()).then(data => {
          channel_members = [];
          data.users.forEach(element => {
              channel_members.push(new ChannelMember(element.id, element.name, element.avatarurl));
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
          data.messages.forEach(element => {
              let sender_name = element.author.name;
              let sender_id = element.author.id;
              let sender_avatar = element.author.avatarurl;
              let message_id = element.id;
              let message_content = element.messages[0].content;
              let div = document.createElement('div');
              div.innerHTML = `<metadata>
                    <user>${sender_name}</user>
                    <timestamp>${sender_id}</timestamp>
                 </metadata>
                 <div id="message">
                    ${message_content}
                 </div>`;
              if (sender_id != id) {
                  div.id = "messages-recieved";
              }
              else {
                  div.id = "messages-sent";
              }
              main_panel_messages.appendChild(div);
          });
      });
  }
  function showBorder(element) {
      element.classList.add('border');
  }
  function hideBorder(element) {
      element.classList.remove('border');
  }

}());
