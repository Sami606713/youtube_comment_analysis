document.addEventListener('DOMContentLoaded', () => {
  // Send message to background script to fetch comments
  chrome.runtime.sendMessage({ action: "fetchComments" }, (response) => {
      if (response?.error) { // Check if response exists and has an error
          alert(response.error); // Display error to user
          return;
      }
  });

  // Listen for the updateUI action from background script
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "updateUI") {
        // Retrieve analysis results from chrome storage
        chrome.storage.local.get(['analysisResults'], (data) => {
            const predictions = data.analysisResults?.predictions; // Access predictions array directly
            
            if (Array.isArray(predictions)) {
                displayCommentsInTable(predictions); // Pass predictions array to display function
            } else {
                console.log('No analysis results found or data format mismatch.');
            }
        }); 
        // Word Cloud
        chrome.storage.local.get("wordCloudImage", (result) => {
          const wordCloudImage = document.getElementById('wordCloudImage');
          if (wordCloudImage && result.wordCloudImage) {
              wordCloudImage.src = result.wordCloudImage; // Set the Base64 image as src
              wordCloudImage.alt = 'Generated Word Cloud';
          }
      });
      // end Word Cloud

      // Retrieve and display summary
      chrome.storage.local.get('summary', (result) => {
        const summaryElement = document.getElementById('comm_summary');
        if (summaryElement && result.summary) {
            summaryElement.innerText = result.summary;
        } else {
            console.error('No summary found in Chrome storage');
        }
      });
    // End Summary

    }
});
});

// Function to display comments and sentiments in a table
function displayCommentsInTable(predictions) {
  document.getElementById("totalComments").innerHTML = predictions.length;

  // // Update ratios based on predictions
  updateRatios(predictions); 
}

// Function to update ratios based on prediction data
function updateRatios(predictions) {
  const total = predictions.length;
  const positiveCount = predictions.filter(prediction => prediction.sentiment === 'Positive').length;
  const negativeCount = predictions.filter(prediction => prediction.sentiment === 'Negative').length;
  const neutralCount = predictions.filter(prediction => prediction.sentiment === 'Neutral').length;

  const positiveRatio = ((positiveCount / total) * 100).toFixed(2);
  const negativeRatio = ((negativeCount / total) * 100).toFixed(2);
  const neutralRatio = ((neutralCount / total) * 100).toFixed(2);

  // Set text and color for each ratio
  document.getElementById('positiveRatio').textContent = `${positiveRatio}% 👍`;
  document.getElementById('negativeRatio').textContent = `${negativeRatio}% 👎`;
  document.getElementById('neutralRatio').textContent = `${neutralRatio}% 🤷`;
}
