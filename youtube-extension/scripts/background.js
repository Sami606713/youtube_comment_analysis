chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "fetchComments") {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            const url = tabs[0].url;
            const videoId = extractVideoId(url);
            const apiKey = 'AIzaSyCPQE_tFHOtVyOlMhIGAywLC-3R1ZfdnAo'; // Use your actual API key here

            const youtubeUrlRegex = /^[a-zA-Z0-9_-]{11}$/;
            if (!youtubeUrlRegex.test(videoId)) {
                console.log("Not a valid YouTube URL");
                sendResponse({ error: "Not a valid YouTube URL" });
                return;
            }

            console.log('Fetching comments for video ID:', videoId);

            const fetchAllComments = (pageToken = '') => {
                let apiUrl = `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&key=${apiKey}&maxResults=100`;
                if (pageToken) {
                    apiUrl += `&pageToken=${pageToken}`;
                }

                console.log("YouTube API URL:", apiUrl);

                return fetch(apiUrl)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        const comments = data.items.map(item => item.snippet.topLevelComment.snippet.textDisplay);
                        if (data.nextPageToken) {
                            return fetchAllComments(data.nextPageToken).then(moreComments => comments.concat(moreComments));
                        } else {
                            return comments;
                        }
                    });
            };

            fetchAllComments()
                .then(allComments => {
                    return fetch('http://127.0.0.1:8000/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: allComments })
                    }).then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    }).then(analysisResults => {
                        chrome.storage.local.set({ comments: allComments, analysisResults: analysisResults});
                        console.log('Sentiment analysis results:', analysisResults);

                        chrome.runtime.sendMessage({ action: "updateUI" });
                        sendResponse({ success: true });
                    });
                })
                .catch(error => {
                    console.error('Error during fetching or analyzing comments:', error);
                    sendResponse({ error: error.message });
                });

            return true; // Indicates asynchronous response
        });
    }
    return true; // Ensure listener also returns true for asynchronous handling
});

// Function to extract video ID from the URL
function extractVideoId(url) {
    const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}
