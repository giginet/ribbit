Ribbit = {}
class Chat
  constructor : (@slug='') ->
    @
#    @socket = new WebSocket("")
#    @socket.on('connect', @onConnected)
#    @socket.on('disconnect', @onDisconnected)
#    @socket.on('message', @onMessaged)

  start : () ->
    @socket.connect()

  onConnected : () ->
    console.log("connected to #{@slug}")
    @socket.send({room : @slug, action : 'start'})

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
        return false
    )

$ ->
  slug = $('#room-slug').val()
  Ribbit.chat = new Chat(slug)
  Ribbit.chat.start()
  Ribbit.view = new ChatView(Ribbit.chat)
