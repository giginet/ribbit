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