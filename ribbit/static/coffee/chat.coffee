Ribbit = {}
class Chat
  constructor : (@slug='') ->
    @socket = new io.Socket()
    @socket.on('connect', @onConnected)
    @socket.on('disconnect', @onDisconnected)
    @socket.on('message', @onMessaged)

  start : () ->
    @socket.connect()

  onConnected : () ->
    @

  onDisconnected : () ->
    @

  onMessaged : () ->
    @


class ChatView
  constructor : (@chat) ->
    @$messageForm = $('#message')
    @$form = $('form')
    @$form.on('submit', ->
        value = $('#message').val()
        if value
          data =
            room : @chat.slug
            action : 'message'
            message : value
        @$messageForm.val('').focus()
    )

$ ->
  Ribbit.chat = new Chat()
  Ribbit.chat.start()
  Ribbit.view = new ChatView(Ribbit.chat)
