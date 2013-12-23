var Chat, ChatView, Ribbit,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

Ribbit = {};

Chat = (function() {
  function Chat(slug) {
    this.slug = slug != null ? slug : '';
    this.onMessaged = __bind(this.onMessaged, this);
    this.onDisconnected = __bind(this.onDisconnected, this);
    this.onConnected = __bind(this.onConnected, this);
    this.socket = new WebSocket("ws://localhost:8060/ws?" + this.slug);
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
    console.log(e.data);
    recieved = JSON.parse(e.data);
    try {
      recieved = JSON.parse(e.data);
    } catch (_error) {
      error = _error;
      recieved = {};
    }
    if (recieved['action'] === 'receive') {
      message = new Ribbit.models.Message(recieved['message']);
      return Ribbit.view.$messageList.append(Ribbit.view.createView(message).fadeIn('fast'));
    } else if (recieved['action'] === 'error') {
      return alert(recieved['body']);
    }
  };

  return Chat;

})();

ChatView = (function() {
  function ChatView(chat) {
    var submit,
      _this = this;
    this.chat = chat;
    this.$messageForm = $('#message-box');
    this.$messageList = $('#message-list');
    this.$messageTemplate = $('.message');
    this.$messageTemplate.remove();
    this.$form = $('#message-form');
    submit = function(e) {
      var data, value;
      value = _this.$messageForm.val();
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
    };
    this.$form.on('click', submit);
    this.$form.on('keydown', function(e) {
      var ENTER_KEY;
      ENTER_KEY = 13;
      if (e.keyCode === ENTER_KEY) {
        return submit(e);
      }
    });
  }

  ChatView.prototype.createView = function(message) {
    var $view;
    $view = this.$messageTemplate.clone();
    $view.show();
    $view.find(".author").text("" + message.author['screen_name'] + "(@" + message.author['username'] + ")");
    $view.find(".body").text(message.body);
    $view.find(".avatar").css({
      'background-image': "url(" + message.author['avatar'] + ")"
    });
    return $view;
  };

  return ChatView;

})();

$(function() {
  var slug;
  slug = $('#room-slug').val();
  Ribbit.chat = new Chat(slug);
  Ribbit.chat.start();
  return Ribbit.view = new ChatView(Ribbit.chat);
});
