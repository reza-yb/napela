function start_socket_and_listen(roomId) {

    // Declare variables
    var userName;

    // Create Websocket
    var chatSocket = new ReconnectingWebSocket(
        'ws://' + window.location.host +
        '/ws/chat');

    // Send message
    chatSocket.onmessage = function(e) {
        console.log('Got a message:' + e.data.toString());
    };

    chatSocket.onopen = function() {
        chatSocket.send(JSON.stringify({ 'message': 'i am connected now' }));
    };



    chatSocket.onclose = function(e) {
        console.log('Socket closed:' + e.toString());
        console.log(e);
    }

    chatSocket.onerror = function(e) {
        console.error("Error: " + e.toString());
    };

    // Sign off message
    window.unload = function(e) {
        console.log('page closed');
    };
}

$(document).ready(function() {
    start_socket_and_listen(120);
    var chat = {
        messageToSend: '',
        messageResponses: [
            'Why did the web developer leave the restaurant? Because of the table layout.',
            'How do you comfort a JavaScript bug? You console it.',
            'An SQL query enters a bar, approaches two tables and asks: "May I join you?"',
            'What is the most used language in programming? Profanity.',
            'What is the object-oriented way to become wealthy? Inheritance.',
            'An SEO expert walks into a bar, bars, pub, tavern, public house, Irish pub, drinks, beer, alcohol'
        ],
        init: function() {
            this.cacheDOM();
            this.bindEvents();
            this.render();
        },
        cacheDOM: function() {
            this.$chatHistory = $('.chat-history');
            this.$button = $('button');
            this.$textarea = $('#message-to-send');
            this.$chatHistoryList = this.$chatHistory.find('ul');
        },
        bindEvents: function() {
            this.$button.on('click', this.addMessage.bind(this));
            this.$textarea.on('keyup', this.addMessageEnter.bind(this));
        },
        render: function() {
            this.scrollToBottom();
            if (this.messageToSend.trim() !== '') {
                var template = Handlebars.compile($("#message-template").html());
                var context = {
                    messageOutput: this.messageToSend,
                    messageOwner: "Amir",
                    time: this.getCurrentTime()
                };
                console.log(template(context));
                this.$chatHistoryList.append(template(context));
                console.log(this.$chatHistoryList);

                this.scrollToBottom();
                this.$textarea.val('');

                // responses
                var templateResponse = Handlebars.compile($("#message-response-template").html());
                var contextResponse = {
                    response: this.getRandomItem(this.messageResponses),
                    messageOwner: "Tomas",
                    time: this.getCurrentTime()
                };

                setTimeout(function() {
                    this.$chatHistoryList.append(templateResponse(contextResponse));
                    this.scrollToBottom();
                }.bind(this), 1500);

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

    chat.init();

    //  var searchFilter = {
    //    options: { valueNames: ['name'] },
    //    init: function() {
    //      var userList = new List('people-list', this.options);
    //      var noItems = $('<li id="no-items-found">No items found</li>');
    //
    //      userList.on('updated', function(list) {
    //        if (list.matchingItems.length === 0) {
    //          $(list.list).append(noItems);
    //        } else {
    //          noItems.detach();
    //        }
    //      });
    //    }
    //  };
    //
    //  searchFilter.init();

});