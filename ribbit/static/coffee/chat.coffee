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
    console.log("connected to #{@slug}")
    @socket.send({room : @slug, action : 'start'})

  onDisconnected : () =>
    @

  onMessaged : (e) =>
    console.log e.data

class ChatView
  constructor : (@chat) ->
    @$messageForm = $('#message')
    @$button = $('send')
    @$button.on('submit', =>
        value = $('#message').val()
        if value
          data =
            room : @chat.slug
            action : 'message'
            message : value
        @$messageForm.val('').focus()
        false
    )

$ ->
  slug = $('#room-slug').val()
  console.log slug
  Ribbit.chat = new Chat(slug)
  Ribbit.chat.start()
  Ribbit.view = new ChatView(Ribbit.chat)
