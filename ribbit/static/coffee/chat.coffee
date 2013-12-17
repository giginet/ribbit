Ribbit = {}
class Chat
  constructor : (@slug='') ->
    @socket = new WebSocket("ws://localhost:9000/chat")
    @socket.onopen = @onConnected
    @socket.onclose = @onDisconnected
    @socket.onmessage = @onMessaged

  start : () ->
    @
    #@socket.connect()

  onConnected : () ->
    console.log("connected to #{@slug}")

  onDisconnected : () ->
    @

  onMessaged : (e) ->
    console.log e.data


class ChatView
  constructor : (@chat) ->
    @$messageForm = $('#message')
    @$form = $('form')
    @$button = $('#send')
    @$button.on('click', =>
        value = $('#message').val()
        if value
          data =
            room : @chat.slug
            action : 'message'
            message : value
          @chat.socket.send(value)
          @$messageForm.val('').focus()
          false
    )

$ ->
  slug = $('#room-slug').val()
  Ribbit.chat = new Chat(slug)
  Ribbit.chat.start()
  Ribbit.view = new ChatView(Ribbit.chat)
