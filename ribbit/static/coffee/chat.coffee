Ribbit = {}
class Chat
  constructor : (@slug='') ->
    @socket = new WebSocket("ws://localhost:8060/ws")
    @socket.onopen = @onConnected
    @socket.onclose = @onDisconnected
    @socket.onmessage = @onMessaged

  start : () ->
    @

  onConnected : () =>
    @socket.send({room : @slug, action : 'start'})

  onDisconnected : () =>
    @

  onMessaged : (e) =>
    try
      recieved = JSON.parse(e.data)
    catch error
      recieved = {}
    if recieved['action'] is 'receive'
      message = new Message(recieved['body'], recieved['author'])
      Ribbit.view.$messageList.append(message.createView())

class ChatView
  constructor : (@chat) ->
    @$messageForm = $('#message')
    @$messageList = $('#message-list')
    @$button = $('#send')
    @$button.on('click', =>
        value = $('#message').val()
        if value
          data =
            room : @chat.slug
            action : 'post'
            user : @chat.user
            body : value
        @chat.socket.send(JSON.stringify(data))
        @$messageForm.val('').focus()
        false
    )

$ ->
  slug = $('#room-slug').val()
  Ribbit.chat = new Chat(slug)
  Ribbit.chat.start()
  Ribbit.view = new ChatView(Ribbit.chat)

class Message


  constructor : (@body, @author) ->
    @$template = $('.message')

  createView : () ->
    $view = @$template.clone()
    $view.show()
    $view.find(".author").text("#{@author['fields']['screen_name']}(@#{@author['fields']['username']})")
    $view.find(".body").text(@body)
    $view
