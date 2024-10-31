chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "fetchComments") {
        chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
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

            const fetchAllComments = async (pageToken = '') => {
                let apiUrl = `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&key=${apiKey}&maxResults=100`;
                if (pageToken) apiUrl += `&pageToken=${pageToken}`;

                console.log("YouTube API URL:", apiUrl);

                const response = await fetch(apiUrl);
                if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

                const data = await response.json();
                const comments = data.items.map(item => item.snippet.topLevelComment.snippet.textDisplay);

                if (data.nextPageToken) {
                    const moreComments = await fetchAllComments(data.nextPageToken);
                    return comments.concat(moreComments);
                } else {
                    return comments;
                }
            };

            try {
                const allComments = await fetchAllComments();

                // Send the comments for sentiment analysis
                const analysisResponse = await fetch('http://127.0.0.1:8000/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: allComments })
                });
                if (!analysisResponse.ok) throw new Error(`HTTP error! Status: ${analysisResponse.status}`);
                
                const analysisResults = await analysisResponse.json();
                chrome.storage.local.set({ comments: allComments, analysisResults });
                console.log('Sentiment analysis results:', analysisResults);

                // Generate the word cloud
                const response = await fetch('http://127.0.0.1:8000/generate_wordcloud/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: allComments.join(" ") })
                });
                if (response.ok) {
                    const blob = await response.blob();
        
                    // Use FileReader as a fallback for URL.createObjectURL
                    const reader = new FileReader();
                    reader.onload = function(event) {
                        // Store the Base64 string in Chrome storage
                        chrome.storage.local.set({ wordCloudImage: event.target.result, analysisResults: analysisResults }, () => {
                            console.log('Word cloud image and analysis results stored.');
                        });
                    };
                    reader.onerror = function() {
                        console.error("Failed to read the Blob data.");
                        alert("An error occurred while displaying the word cloud.");
                    };
                    reader.readAsDataURL(blob); // Convert blob to Base64 URL
                }else{
                    throw new Error(`HTTP error! Status: ${wordCloudResponse.status}`);
                } 

                // Get Summary
                get_summary(text=allComments.join(" "))
                // End of get summary

                // Send message to update the UI
                chrome.runtime.sendMessage({
                    action: "updateUI",
                    analysisResults
                });
                sendResponse({ success: true, analysisResults });
            } catch (error) {
                console.error('Error during fetching or generating word cloud:', error);
                sendResponse({ error: error.message });
            }
        });

        return true; // Indicates asynchronous response
    }
    return true;
});

// generate_summary function
async function get_summary(text) {
    const response = await fetch('http://127.0.0.1:8000/generate_summary/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    });

    if (response.ok) {
        const summary = await response.json();
        
        // set the summary in Chrome storage
        chrome.storage.local.set({ summary: summary.summary }, () => {
            console.log('Summary stored in Chrome storage:', summary.summary);
        });
    } else {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
}

// Function to extract video ID from the URL
function extractVideoId(url) {
    const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}
