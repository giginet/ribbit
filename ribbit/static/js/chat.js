var Chat, ChatView, Ribbit,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

Ribbit = {};

Chat = (function() {
  function Chat(slug) {
    this.slug = slug != null ? slug : '';
    this.onMessaged = __bind(this.onMessaged, this);
    this.onDisconnected = __bind(this.onDisconnected, this);
    this.onConnected = __bind(this.onConnected, this);
    this.HOST = "localhost:8060";
    this.socket = new WebSocket("ws://" + this.HOST + "/ws?" + this.slug);
    this.socket.onopen = this.onConnected;
    this.socket.onclose = this.onDisconnected;
    this.socket.onmessage = this.onMessaged;
  }

  Chat.prototype.start = function() {
    return $.getJSON("http://" + this.HOST + "/api/messages.json?room=" + this.slug, function(data) {
      var message, messageJSON, _i, _len, _ref;
      _ref = data.reverse();
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        messageJSON = _ref[_i];
        message = new Ribbit.models.Message(messageJSON);
        Ribbit.view.addMessageView(message);
      }
      return Ribbit.view.scrollToMessage(message);
    });
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
      message = new Ribbit.models.Message(recieved['message']);
      Ribbit.view.addMessageView(message);
      return Ribbit.view.scrollToMessage(message);
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

  ChatView.prototype.addMessageView = function(message) {
    var $view;
    $view = this.$messageTemplate.clone();
    $view.show();
    $view.find(".author").text("" + message.author['screen_name'] + "(@" + message.author['username'] + ")");
    $view.find(".body").text(message.body);
    $view.attr('id', message.domID);
    return this.$messageList.append($view.fadeIn('fast'));
  };

  ChatView.prototype.scrollToMessage = function(message) {
    var $list, $target, position, speed;
    speed = 500;
    $target = $("#" + message.domID);
    $list = $("#message-list");
    position = $target.position().top + $list.scrollTop();
    return $list.animate({
      scrollTop: position
    }, speed, "swing");
  };

  return ChatView;

})();

$(function() {
  var slug;
  slug = $('#room-slug').val();
  Ribbit.chat = new Chat(slug);
  Ribbit.view = new ChatView(Ribbit.chat);
  return Ribbit.chat.start();
});
