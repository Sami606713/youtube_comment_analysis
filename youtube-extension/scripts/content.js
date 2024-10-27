// Extract the video ID from the URL
let urlParams = new URLSearchParams(window.location.search);
let videoId = urlParams.get('v');

// Send the video ID back to the background script
chrome.runtime.sendMessage({videoId: videoId}, function(response) {
    console.log('Video ID sent to background script');
});
