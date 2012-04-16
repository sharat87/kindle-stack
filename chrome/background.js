(function () {

    // Get the extension manifest.
    var xhr = new XMLHttpRequest();
    xhr.open('GET', chrome.extension.getURL('manifest.json'), false);
    xhr.send(null);
    var manifest = JSON.parse(xhr.responseText);

    // Put the version in localStorage
    localStorage.version = manifest.version;

    chrome.extension.onRequest.addListener(function (request, sender, send) {
        if (request == 'get-email') {
            send(localStorage.kindleEmail);
        } else if (request == 'open-options') {
            chrome.tabs.create({url: chrome.extension.getURL('options.html')});
        }
    });

}());
