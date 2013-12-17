(function() {
  var Chat, ChatView, Ribbit,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  Ribbit = {};

  Chat = (function() {
    function Chat(slug) {
      this.slug = slug != null ? slug : '';
      this.onMessaged = __bind(this.onMessaged, this);
      this.onDisconnected = __bind(this.onDisconnected, this);
      this.onConnected = __bind(this.onConnected, this);
      this.socket = new WebSocket("ws://localhost:8060/ws");
      this.socket.onopen = this.onConnected;
      this.socket.onclose = this.onDisconnected;
      this.socket.onmessage = this.onMessaged;
    }

    Chat.prototype.start = function() {
      return this;
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
      this.$button = $('send');
      this.$button.on('submit', function() {
        var data, value;
        value = $('#message').val();
        if (value) {
          data = {
            room: _this.chat.slug,
            action: 'message',
            message: value
          };
        }
        _this.$messageForm.val('').focus();
        return false;
      });
    }

    return ChatView;

  })();

  $(function() {
    var slug;
    slug = $('#room-slug').val();
    console.log(slug);
    Ribbit.chat = new Chat(slug);
    Ribbit.chat.start();
    return Ribbit.view = new ChatView(Ribbit.chat);
  });

}).call(this);
