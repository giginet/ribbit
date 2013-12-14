(function() {
  var Chat, ChatView, Ribbit;

  Ribbit = {};

  Chat = (function() {
    function Chat(slug) {
      this.slug = slug != null ? slug : '';
      this.socket = new io.Socket();
      this.socket.on('connect', this.onConnected);
      this.socket.on('disconnect', this.onDisconnected);
      this.socket.on('message', this.onMessaged);
    }

    Chat.prototype.start = function() {
      return this.socket.connect();
    };

    Chat.prototype.onConnected = function() {
      return this;
    };

    Chat.prototype.onDisconnected = function() {
      return this;
    };

    Chat.prototype.onMessaged = function() {
      return this;
    };

    return Chat;

  })();

  ChatView = (function() {
    function ChatView(chat) {
      this.chat = chat;
      this.$messageForm = $('#message');
      this.$form = $('form');
      this.$form.on('submit', function() {
        var data, value;
        value = $('#message').val();
        if (value) {
          data = {
            room: this.chat.slug,
            action: 'message',
            message: value
          };
        }
        return this.$messageForm.val('').focus();
      });
    }

    return ChatView;

  })();

  $(function() {
    Ribbit.chat = new Chat();
    Ribbit.chat.start();
    return Ribbit.view = new ChatView(Ribbit.chat);
  });

}).call(this);
