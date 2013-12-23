Ribbit.models = {};

Ribbit.models.Message = (function() {
  function Message(json) {
    this.body = json['body'];
    this.author = new Ribbit.models.User(json['author']);
  }

  return Message;

})();

Ribbit.models.User = (function() {
  function User(json) {
    this.username = json['username'];
    this.screen_name = json['screen_name'];
    this.avatar = json['avatar'];
  }

  return User;

})();
