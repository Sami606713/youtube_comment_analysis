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
                    // Send the comments for sentiment analysis
                    fetch('http://127.0.0.1:8000/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: allComments })
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(analysisResults => {
                        // Store the analysis results
                        chrome.storage.local.set({ comments: allComments, analysisResults: analysisResults });
                        console.log('Sentiment analysis results:', analysisResults);

                        // Now, generate the word cloud using the same comments
                        return fetch('http://127.0.0.1:8000/generate_wordcloud/', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ text: allComments.join(" ") })
                        })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`HTTP error! Status: ${response.status}`);
                            }
                            return response.blob(); // Fetch the word cloud image as a Blob
                        })
                        .then(blob => {
                            const imageUrl = URL.createObjectURL(blob); // Create a temporary URL for the image

                            // Store the image URL along with the analysis results
                            chrome.storage.local.set({ wordcloudImageUrl: imageUrl });
                            console.log('Word cloud generated and stored:', imageUrl);

                            // Update the UI
                            chrome.runtime.sendMessage({
                                action: "updateUI",
                                imageUrl: imageUrl,
                                analysisResults: analysisResults
                            });
                            sendResponse({ success: true, imageUrl: imageUrl, analysisResults: analysisResults });
                        });
                    })
                    .catch(error => {
                        console.error('Error during fetching or generating word cloud:', error);
                        sendResponse({ error: error.message });
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
