(function() {
  var Chat, ChatView, Message, Ribbit,
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
      return this.socket.send({
        room: this.slug,
        action: 'start'
      });
    };

    Chat.prototype.onDisconnected = function() {
      return this;
    };

    Chat.prototype.onMessaged = function(e) {
      var error, message, recieved;
      try {
        recieved = JSON.parse(e.data);
      } catch (_error) {
        error = _error;
        recieved = {};
      }
      if (recieved['action'] === 'receive') {
        message = new Message(recieved['body'], recieved['author']);
        return Ribbit.view.$messageList.append(message.createView());
      }
    };

    return Chat;

  })();

  ChatView = (function() {
    function ChatView(chat) {
      var _this = this;
      this.chat = chat;
      this.$messageForm = $('#message');
      this.$messageList = $('#message-list');
      this.$button = $('#send');
      this.$button.on('click', function() {
        var data, value;
        value = $('#message').val();
        if (value) {
          data = {
            room: _this.chat.slug,
            action: 'post',
            user: _this.chat.user,
            body: value
          };
        }
        _this.chat.socket.send(JSON.stringify(data));
        _this.$messageForm.val('').focus();
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

  Message = (function() {
    function Message(body, author) {
      this.body = body;
      this.author = author;
      this.$template = $('.message');
    }

    Message.prototype.createView = function() {
      var $view;
      $view = this.$template.clone();
      $view.show();
      $view.find(".author").text("" + this.author['fields']['screen_name'] + "(@" + this.author['fields']['username'] + ")");
      $view.find(".body").text(this.body);
      return $view;
    };

    return Message;

  })();

}).call(this);
