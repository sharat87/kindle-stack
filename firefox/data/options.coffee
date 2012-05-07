jQuery ($) ->

  $('#save-btn').click (e) ->
    alert self.port
    self.port.emit 'save-options', {email: $('#email-input').val()}
