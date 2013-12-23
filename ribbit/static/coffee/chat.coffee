Ribbit = {}
class Chat
  constructor : (@slug='') ->
    @HOST = "localhost:8060"
    @socket = new WebSocket("ws://#{@HOST}/ws?#{@slug}")
    @socket.onopen = @onConnected
    @socket.onclose = @onDisconnected
    @socket.onmessage = @onMessaged

  start : () ->
    $.getJSON("http://#{@HOST}/api/messages.json?room=#{@slug}", (data) ->
      for messageJSON in data.reverse()
        message = new Ribbit.models.Message(messageJSON)
        Ribbit.view.addMessageView(message)
    )

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
      message = new Ribbit.models.Message(recieved['message'])
      Ribbit.view.addMessageView(message)
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

  addMessageView : (message) ->
    $view = @$messageTemplate.clone()
    $view.show()
    $view.find(".author").text("#{message.author['screen_name']}(@#{message.author['username']})")
    $view.find(".body").text(message.body)
#    $view.find(".avatar").css({'background-image': "url(#{message.author['avatar']})"})
    @$messageList.append($view.fadeIn('fast'))

$ ->
  slug = $('#room-slug').val()
  Ribbit.chat = new Chat(slug)
  Ribbit.view = new ChatView(Ribbit.chat)
  Ribbit.chat.start()

