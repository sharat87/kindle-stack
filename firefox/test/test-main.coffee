main = require 'main'

exports.test_test_run = (test) ->
  test.pass 'Unit test running!'

exports.test_id = (test) ->
  test.assert(require('self').id.length > 0)

exports.test_url = (test) ->
  require('request').Request({
    url: 'http://www.mozilla.org/'
    onComplete: (response) ->
      test.assertEqual(response.statusText, "OK")
      test.done()
  }).get()
  test.waitUntilDone 20000

exports.test_open_tab = (test) ->
  tabs = require 'tabs'
  tabs.open({
    url: 'http://www.mozilla.org/'
    onReady: (tab) ->
      test.assertEqual(tab.url, 'http://www.mozilla.org/')
      test.done()
  })
  test.waitUntilDone 20000
