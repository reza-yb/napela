var chat = {
        init: function(ownerId) {
            this.ownerId = ownerId
            this.cacheDOM();
            this.bindEvents();
            this.render();
        },
        chatSocket: null,
        messageToSend: '',
        ownerId: null,
        cacheDOM: function() {
            this.$chatHistory = $('.chat-history');
            this.$button = $('button');
            this.$textarea = $('#message-to-send');
            this.$chatHistoryList = this.$chatHistory.find('ul');
        },
        bindEvents: function() {
            this.$button.on('click', this.addMessage.bind(this));
//            this.$textarea.on('keyup', this.addMessageEnter.bind(this));
        },
        render: function() {
            this.scrollToBottom();
            if (this.messageToSend.trim() !== '') {
                try {
                    var ownerId = this.ownerId;
                    var contactId = document.getElementById("chat_with_contact_id").value;
                    var toUserId = document.getElementById("chat_with_user_id").value;

                    var chatMessage = new ChatMessage(ownerId,contactId,false,this.messageToSend.trim(),null);
                    /// creating group code
                    userIds = [ownerId,toUserId];
                    userIds.sort(function(a, b) {
                        if (a == null || b == null){
                            return 1;
                        }
                        return a - b;
                    });
                    var channelRoom = userIds.join('-');
                    var socket_message = new SocketMessage(MessageType.newMessage, channelRoom ,chatMessage)
                    this.chatSocket.send(JSON.stringify(socket_message));
                    this.$textarea.val('');
                    this.messageToSend = '';
                }catch(err) {
                    console.log(err);
                }
            }
        },

        addMessage: function() {
            this.messageToSend = this.$textarea.val();
            console.log('Add message: ' + this.messageToSend);
            this.render();
        },
        addMessageEnter: function(event) {
            // enter was pressed
            if (event.keyCode === 13) {
                this.addMessage();
            }
        },
        scrollToBottom: function() {
            this.$chatHistory.scrollTop(this.$chatHistory[0].scrollHeight);
            //       if(this.$chatHistory[0]!= undefined){
            //              this.$chatHistory.scrollTop(this.$chatHistory[0].scrollHeight);
            //       }else{
            //              this.$chatHistory.scrollTop(0);
            //       }
        },
        getCurrentTime: function() {
            return new Date().toLocaleTimeString().
            replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3");
        },
        getRandomItem: function(arr) {
            return arr[Math.floor(Math.random() * arr.length)];
        }

};

function main(userId,toContactId,toUserId){
    $(document).ready(function() {
        load_prev_messages_and_contact_avatar(toContactId);
        start_socket_and_listen(userId,toUserId);
        chat_initialization(userId);
    });
}

function chat_initialization(user_id){
    chat.init(user_id);
}

function start_socket_and_listen(ownerId,toUserId) {

    // Create Websocket
    chat.chatSocket = new ReconnectingWebSocket(
        'ws://' + window.location.host +
        '/ws/chat');

    // Send message
    chat.chatSocket.onmessage = function(e) {
        console.log("on message");
        var message_type = JSON.parse(JSON.parse(e.data))['message_type'];
        console.log(message_type)
        if (message_type == "new_chat_message"){
            var socketMessage = SocketMessage.fromJson(JSON.parse(JSON.parse(e.data)));
            console.log(socketMessage.message_data);
            var currentContactId = document.getElementById("chat_with_contact_id").value;
            if(socketMessage.message_data.contact_id === currentContactId){
                if(socketMessage.message_data.owner_user_id === chat.ownerId){
                    var template = Handlebars.compile( $("#message-template").html());
                    var context = {
                      messageOutput: socketMessage.message_data.text,
                      time: socketMessage.message_data.created_date_time
                    };

                    chat.$chatHistoryList.append(template(context));
                    chat.scrollToBottom();
                }else{
                    var templateResponse = Handlebars.compile( $("#message-response-template").html());
                    var contextResponse = {
                      response: socketMessage.message_data.text,
                      time: socketMessage.message_data.created_date_time
                    };
                    this.$chatHistoryList.append(templateResponse(contextResponse));
                    this.scrollToBottom();
                }
            }
        }
    };

    chat.chatSocket.onopen = function() {
        userIds = [ownerId,toUserId];
        userIds.sort(function(a, b) {
            if (a == null || b == null){
                return 1;
            }
            return a - b;
        });
        var channelRoom = userIds.join('-');
        var socket_message = new SocketMessage(MessageType.setChannel, channelRoom ,"");
        chat.chatSocket.send(JSON.stringify(socket_message));
    };

    chat.chatSocket.onclose = function(e) {
        console.log('Socket closed:' + e.toString());
        console.log(e);
    }
    chat.chatSocket.onerror = function(e) {
        console.error("Error: " + e.toString());
    };
    // Sign off message
    window.unload = function(e) {
        console.log('page closed');
    };
}

function load_prev_messages_and_contact_avatar(to_contact_id){
            var dataForm = "";
            document.getElementsByClassName("chat-with")[0].innerText = "Loading ...";
            $.ajax({
                url: 'http://'+window.location.host+'/chat/prev_messages/'+String(to_contact_id)+"/",
                data: dataForm,
                dataType: 'json',
                type: 'POST',
                contentType: "application/json; charset=utf-8",
            }).done(function (response) {
                chat.$chatHistoryList.empty();
                chat.cacheDOM();
                /// load contact name in chat page
                var contact_name = response.contact_info.first_name + " " + response.contact_info.last_name;
                document.getElementsByClassName("chat-with")[0].innerText = contact_name;
                ///////////////////////////////////////
                /// setting user id to hidden input ///
                ///////////////////////////////////////
                document.getElementById("chat_with_contact_id").value = to_contact_id;
                document.getElementById("chat_with_user_id").value = response.contact_info.id;
                /// load contact old messages
                response.prev_messages.forEach(function (message_data) {
                    if(owner_user_id == message_data.owner.id){
                        // self
                        var template = Handlebars.compile($("#message-template").html());
                        var context = {
                            messageOutput: message_data.text,
                            messageOwner: message_data.owner.first_name+" "+message_data.owner.last_name,
                            time: message_data.created_datetime
                        };
                        chat.$chatHistoryList.append(template(context));
                    }else{
                        // user
                        var templateResponse = Handlebars.compile($("#message-response-template").html());
                        var contextResponse = {
                            response: message_data.text,
                            messageOwner: message_data.owner.first_name+" "+message_data.owner.last_name,
                            time: message_data.created_datetime
                        };
                        chat.$chatHistoryList.append(templateResponse(contextResponse));
                    }
                });
                chat.scrollToBottom();

            }).fail(function (xhr, status, errorThrown) {
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            });
}
