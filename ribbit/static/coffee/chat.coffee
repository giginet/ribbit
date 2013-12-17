Ribbit = {}
class Chat
  constructor : (@slug='') ->
    @socket = new WebSocket("ws://localhost:8060/ws?#{@slug}")
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
      console.log e.data
    if recieved['action'] is 'receive'
      message = new Message(recieved)
      Ribbit.view.$messageList.append(Ribbit.view.createView(message).fadeIn('fast'))
    else if recieved['action'] is 'error'
      alert(recieved['body'])

class ChatView
  constructor : (@chat) ->
    @$messageForm = $('#message-box')
    @$messageList = $('#message-list')
    @$messageTemplate = $('.message')
    @$messageTemplate.remove()
    @$form = $('#message-form')
    submit = (e) =>
      value = @$messageForm.val()
      if value
        data =
          room : @chat.slug
          action : 'post'
          user : @chat.user
          body : value
      @chat.socket.send(JSON.stringify(data))
      @$messageForm.val('').focus()
      false
    @$form.on('click', submit)
    @$form.on('keydown', (e) ->
      ENTER_KEY = 13
      if e.keyCode == ENTER_KEY
        submit(e)
    )

  createView : (message) ->
    $view = @$messageTemplate.clone()
    $view.show()
    $view.find(".author").text("#{message.author['screen_name']}(@#{message.author['username']})")
    $view.find(".body").text(message.body)
    $view.find(".avatar").css({'background-image': "url(#{message.author['avatar']})"})
    $view

$ ->
  slug = $('#room-slug').val()
  Ribbit.chat = new Chat(slug)
  Ribbit.chat.start()
  Ribbit.view = new ChatView(Ribbit.chat)

class Message
  constructor : (@data) ->
    @body = @data['body']
    @author = @data['author']


