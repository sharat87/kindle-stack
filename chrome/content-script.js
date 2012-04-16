jQuery(function ($) {

    if(!$(document.body).is('.question-page')) {
        // Not a StackExchange question page.
        return;
    }

    $('<a href=#><img src="' +
      chrome.extension.getURL('res/kindle.png') +
      '"></a>')
        .appendTo('#question div.vote')
        .css({
            display: 'block',
            height: '20px',
            margin: '0 auto 4px',
            outline: 'medium none',
            width: '24px'
        })
        .click(function (e) {
            e.preventDefault();

            var th = $(this);

            if(th.is('.loading')) {
                return;
            }

            th.addClass('loading').find('img')
                .attr('src',
                      chrome.extension.getURL('res/loading.gif'));

            var restoreImage = function () {
                th.removeClass('loading').find('img')
                    .attr('src',
                          chrome.extension.getURL('res/kindle.png'));
            };

            var questionId = $('#question').data('questionid');

            chrome.extension.sendRequest('get-email', function (email) {
                if (!email) {
                    chrome.extension.sendRequest('open-options');
                    restoreImage();
                    return;
                }
                $.ajax({
                    url: 'http://kindle-stack.sharats.me/send',
                    type: 'POST',
                    data: {
                        site: location.host,
                        question: questionId,
                        email: email
                    },
                    success: function (response) {
                        if (!response.ok) {
                            alert(response.msg ||
                                'Ooops! Something went wrong. Try again later.');
                        } else {
                            alert('Done. Happy reading!');
                        }
                        restoreImage();
                    },
                    error: function () {
                        alert('Ooops! Something terrible happened.');
                        restoreImage();
                    }
                });
            });

        });

    });
