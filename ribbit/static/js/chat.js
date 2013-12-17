(function() {
  var Chat, ChatView, Ribbit;

  Ribbit = {};

  Chat = (function() {
    function Chat(slug) {
      this.slug = slug != null ? slug : '';
      this.socket = new WebSocket("ws://localhost:9000/chat");
      this.socket.onopen = this.onConnected;
      this.socket.onclose = this.onDisconnected;
      this.socket.onmessage = this.onMessaged;
    }

    Chat.prototype.start = function() {
      return this;
    };

    Chat.prototype.onConnected = function() {
      return console.log("connected to " + this.slug);
    };

    Chat.prototype.onDisconnected = function() {
      return this;
    };

    Chat.prototype.onMessaged = function(e) {
      return console.log(e.data);
    };

    return Chat;

  })();

  ChatView = (function() {
    function ChatView(chat) {
      var _this = this;
      this.chat = chat;
      this.$messageForm = $('#message');
      this.$form = $('form');
      this.$button = $('#send');
      this.$button.on('click', function() {
        var data, value;
        value = $('#message').val();
        if (value) {
          data = {
            room: _this.chat.slug,
            action: 'message',
            message: value
          };
          _this.chat.socket.send(value);
          _this.$messageForm.val('').focus();
          return false;
        }
      });
    }

    return ChatView;

  })();

  $(function() {
    var slug;
    slug = $('#room-slug').val();
    Ribbit.chat = new Chat(slug);
    Ribbit.chat.start();
    return Ribbit.view = new ChatView(Ribbit.chat);
  });

}).call(this);
