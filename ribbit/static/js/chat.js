(function() {
  var Chat, ChatView, Ribbit;

  Ribbit = {};

  Chat = (function() {
    function Chat(slug) {
      this.slug = slug != null ? slug : '';
      this;
    }

    Chat.prototype.start = function() {
      return this.socket.connect();
    };

    Chat.prototype.onConnected = function() {
      console.log("connected to " + this.slug);
      return this.socket.send({
        room: this.slug,
        action: 'start'
      });
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
        this.$messageForm.val('').focus();
        return false;
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
