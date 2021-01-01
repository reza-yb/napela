class MessageType{
    static newMessage = "new_chat_message";
    static setChannel = "set_channel";
}

class SocketMessage {
    constructor(message_type, channel_room, message_data) {
        this.message_type = message_type;
        this.channel_room = channel_room;
        this.message_data = message_data
    }

    static fromJson(json){
         console.log(json);
         console.log(json.message_type);
         var socketMessage = new SocketMessage();
         socketMessage.message_type = json.message_type;
         socketMessage.channel_room = json.channel_room;

         if (socketMessage.message_type == MessageType.newMessage){
            socketMessage.message_data = ChatMessage.from(json.message_data);
         }
           return socketMessage;
    }
}
class ChatMessage {
    constructor(owner_user_id, contact_id, seen, text, created_date_time) {
        this.owner_user_id = owner_user_id;
        this.contact_id = contact_id;
        this.seen = seen
        this.text = text
        this.created_date_time = created_date_time
    }
    static from(json){
        return Object.assign(new ChatMessage(), json);
    }
}