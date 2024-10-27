document.addEventListener('DOMContentLoaded', () => {
  chrome.runtime.sendMessage({ action: "fetchComments" }, (response) => {
      if (response.error) {
          alert(response.error); // Display error to user
          return;
      }
  }); // Corrected closing parenthesis here

  // Listen for the updateUI action from background script
//   chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//       if (request.action === "updateUI") {
//           chrome.storage.local.get(['comments'], (data) => {
//               if (data.comments) {
//                   displayComments(data.comments);
//               }
//           });
//       }
//   });
});


chrome.storage.local.get(['analysisResults'], (data) => {
  const analysisResults = data.analysisResults;
  
  // Check if analysisResults exist
  if (analysisResults && Array.isArray(analysisResults.predictions)) {
      displayCommentsInTable(analysisResults.predictions);
  } else {
      console.log('No analysis results found.');
  }
});

// Function to display comments and sentiments in a table
function displayCommentsInTable(predictions) {
  document.getElementById("Total").innerHTML=predictions.length;
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
  updateRatios(); 
}

// Function to update ratios (placeholder)
function updateRatios() {
  // Example implementation to update ratios
  document.getElementById('positiveRatio').textContent = "50%"; // Replace with actual calculation
  document.getElementById('negativeRatio').textContent = "30%"; // Replace with actual calculation
  document.getElementById('neutralRatio').textContent = "20%"; // Replace with actual calculation
}
