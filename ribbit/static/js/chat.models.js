Ribbit.models = {};

Ribbit.models.Message = (function() {
  function Message(json) {
    this.id = json['id'];
    this.body = json['body'];
    this.author = new Ribbit.models.User(json['author']);
    this.room = new Ribbit.models.Room(json['room']);
    this.created_at = new Date(Date.parse(json['created_at']));
    this.updated_at = new Date(Date.parse(json['updated_at']));
    this.domID = "message-" + this.id;
  }

  return Message;

})();

Ribbit.models.User = (function() {
  function User(json) {
    this.id = json['id'];
    this.username = json['username'];
    this.screen_name = json['screen_name'];
    this.avatar = json['avatar'];
  }

  return User;

})();

Ribbit.models.Room = (function() {
  function Room(json) {
    this.id = json['id'];
    this.title = json['title'];
    this.description = json['description'];
    this.image = json['image'];
    this.scope = json['scope'];
    this.created_at = new Date(Date.parse(json['created_at']));
  }

  return Room;

})();
