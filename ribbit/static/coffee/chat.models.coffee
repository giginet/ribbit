Ribbit.models = {}
class Ribbit.models.Message
  constructor : (json) ->
    @body = json['body']
    @author = new Ribbit.models.User(json['author'])

class Ribbit.models.User
  constructor : (json) ->
    @username = json['username']
    @screen_name = json['screen_name']
    @avatar = json['avatar']

class Ribbit.models.Room
  constructor : (json) ->
    @title = json['title']
    @description = json['description']
    @image = json['image']
    @scope = json['scope']