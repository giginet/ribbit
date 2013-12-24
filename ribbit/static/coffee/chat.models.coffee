Ribbit.models = {}
class Ribbit.models.Message
  constructor : (json) ->
    @id = json['id']
    @body = json['body']
    @author = new Ribbit.models.User(json['author'])
    @room = new Ribbit.models.Room(json['room'])
    @created_at = new Date(Date.parse(json['created_at']))
    @updated_at = new Date(Date.parse(json['updated_at']))
    @domID = "message-#{@id}"

class Ribbit.models.User
  constructor : (json) ->
    @id = json['id']
    @username = json['username']
    @screen_name = json['screen_name']
    @avatar = json['avatar']

class Ribbit.models.Room
  constructor : (json) ->
    @id = json['id']
    @title = json['title']
    @description = json['description']
    @image = json['image']
    @scope = json['scope']
    @created_at = new Date(Date.parse(json['created_at']))
