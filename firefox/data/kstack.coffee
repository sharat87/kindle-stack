jQuery ($) ->

  # Check if this is a StackExchange question page.
  return unless $(document.body).is('.question-page')

  self.port.on 'init-data-response', (data) ->
    $('<a href=#><img src="' + data.kindleImage + '"></a>')
      .appendTo('#question div.vote')
      .css(
        display: 'block'
        height: '20px'
        margin: '0 auto 4px'
        outline: 'medium none'
        width: '24px'
      )
      .click (e) ->
        do e.preventDefault

        th = $ this

        self.port.emit 'show-options'
        return

        return if th.is('.loading')

        th.addClass('loading').find('img')
          .attr('src', data.loadingImage)

        restoreImage = ->
          th.removeClass('loading').find('img')
            .attr('src', data.kindleImage)

        questionId = $('#question').data('questionid')

        chrome.extension.sendRequest 'get-email', (email) ->

          unless email
            do restoreImage
            # chrome.extension.sendRequest 'open-options'
            alert 'go to options and set your email address'
            return

          $.ajax
            url: 'http://kindle-stack.sharats.me/send'
            type: 'POST'

            data:
              site: location.host,
              question: questionId,
              email: email

            success: (response) ->
              if not response.ok
                  alert(response.msg or
                      'Ooops! Something went wrong. Try again later.')
              else
                  alert 'Done. Happy reading!'
              do restoreImage

            error: ->
              alert 'Ooops! Something terrible happened.'
              do restoreImage

  self.port.emit 'init-data'
