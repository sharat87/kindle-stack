pageMod = require 'page-mod'
{ data } = require 'self'
userstyles = require 'userstyles'
file = require 'file'
{ Cc, Ci } = require 'chrome'
{ Request } = require 'request'
{ Panel } = require 'panel'
{ storage } = require 'simple-storage'

showOptions = do ->
  optionsPane = Panel
    contentURL: data.url 'options.html'

  optionsPane.on 'save-options', (data) ->
    console.info 'save options'
    storage.email = data.email

  console.info 'options pane ready'
  return (-> do optionsPane.show)

exports.main = (options, callbacks) ->
  console.log options.loadReason

  pageMod.PageMod
    include: ['http://*', 'https://*']

    contentScriptWhen: 'end'
    contentScriptFile: [
      data.url 'jquery-1.7.2.min.js'
      data.url 'kstack.js'
    ]

    onAttach: (worker) ->

      userstyles.load data.url 'css/styles.css'

      worker.port.on 'init-data', ->
        worker.port.emit 'init-data-response', {
          kindleImage: data.url 'res/kindle.png'
          loadingImage: data.url 'res/loading.gif'
        }

      worker.port.on 'show-options', showOptions

      worker.port.on 'atch-open', (fname, href) ->
        console.info 'open file ' + fname
        fpath = '/home/sharat/Downloads/hd-attachments/' + fname

        fileToOpen = Cc["@mozilla.org/file/local;1"].createInstance(Ci.nsILocalFile)
        fileToOpen.initWithPath fpath

        open_file = ->
          worker.port.emit 'atch-open-response', fname, file.exists fpath
          do fileToOpen.launch if file.exists fpath

        do open_file

        unless file.exists fpath
          req = Request
            url: href
            onComplete: (response) ->
              console.info 'download finish ', response.status
              out_file = file.open fpath, 'w'
              out_file.write response.text
              do out_file.close
              worker.port.emit 'atch-download-complete', fname
              do open_file

          do req.get
