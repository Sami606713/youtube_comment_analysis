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
    }
});
});

// Function to display comments and sentiments in a table
function displayCommentsInTable(predictions) {
  document.getElementById("Total").innerHTML = predictions.length;
  const commentSection = document.getElementById('commentSection');

  // Create a table element
  const table = document.createElement('table');
  table.border = '1'; // Add border for visibility
  const headerRow = table.insertRow();

  // Create table headers
  const headerCell1 = document.createElement('th');
  headerCell1.textContent = 'Comment';
  const headerCell2 = document.createElement('th');
  headerCell2.textContent = 'Sentiment';

  headerRow.appendChild(headerCell1);
  headerRow.appendChild(headerCell2);

  // Append headers to the table
  table.appendChild(headerRow);

  // Populate the table with comments and sentiments
  predictions.forEach(prediction => {
      const row = table.insertRow();
      const cell1 = row.insertCell(0);
      const cell2 = row.insertCell(1);

      cell1.textContent = prediction.comment; // Display the comment
      cell2.textContent = prediction.sentiment; // Display the sentiment
  });

  // Append the table to the comment section
  commentSection.innerHTML = ''; // Clear previous content
  commentSection.appendChild(table);

  // Update ratios based on predictions
  updateRatios(predictions); 
}

// Function to update ratios based on prediction data
function updateRatios(predictions) {
  const total = predictions.length;
  const positiveCount = predictions.filter(prediction => prediction.sentiment === 'Positive').length;
  const negativeCount = predictions.filter(prediction => prediction.sentiment === 'Negative').length;
  const neutralCount = predictions.filter(prediction => prediction.sentiment === 'Neutral').length;

  document.getElementById('positiveRatio').textContent = `${((positiveCount / total) * 100).toFixed(2)}%`;
  document.getElementById('negativeRatio').textContent = `${((negativeCount / total) * 100).toFixed(2)}%`;
  document.getElementById('neutralRatio').textContent = `${((neutralCount / total) * 100).toFixed(2)}%`;
}
