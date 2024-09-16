jQuery(document).ready(function($) {
    $('#songSubmissionType').on('change', function() {
        const selectedValue = $(this).val();
        if (selectedValue === 'url') {
            $('#songUrlContainer').show();
            $('#songFileContainer').hide();
            $('#songFile').val('');  // Clear file input
        } else if (selectedValue === 'upload') {
            $('#songFileContainer').show();
            $('#songUrlContainer').hide();
            $('#songUrl').val('');  // Clear URL input
        }
    });

    $('.song-form').on('submit', function(e) {
        e.preventDefault();  // Prevent default form submission

        const songUrl = $('#songUrl').val().trim();
        const songFile = $('#songFile')[0].files[0];
        const songSubmissionType = $('#songSubmissionType').val();

        if (!songSubmissionType) {
            alert('Please select how you want to submit your song.');
            return;
        }

        if ((songSubmissionType === 'url' && !songUrl) || (songSubmissionType === 'upload' && !songFile)) {
            alert('Please provide the required song information.');
            return;
        }

        const form = $(this)[0];
        const formData = new FormData(form);  // Create FormData object for file uploads
        
        // Hide the download button while processing
        $('.download-btn').hide();

        const submitButton = $(this).find('button[type="submit"]');
        submitButton.css('background-color', '#c36');
        submitButton.css('transform', 'translateY(-2px)');

        $('.spinner').show();
        $('.results').remove();  // Remove previous results if any

        $.ajax({
            url: '/compare-professor-song',  // Use the API URL passed from PHP
            type: 'POST',
            processData: false,  // Important for file upload
            contentType: false,  // Important for file upload
            data: formData,  // Send the form data
            success: function(response) {
                $('.spinner').hide();
                submitButton.css('background-color', '#2ecc71');  // Reset button color

                if (response && Array.isArray(response)) {
                    let resultsHtml = '<div class="results"><h2>Comparison Results:</h2><table id="resultsTable"><thead><tr><th>Artist Song</th><th>Similarity</th></tr></thead><tbody>';
                    response.forEach(result => {
                        resultsHtml += `<tr><td>${result.artist_song}</td><td>${result.similarity.toFixed(2)}</td></tr>`;
                    });
                    resultsHtml += '</tbody></table></div>';
                    $('.song-form').after(resultsHtml);  // Display the results

                    // Show the download button
                    $('.download-btn').show().on('click', function() {
                        downloadCSV(response);
                    });
                } else {
                    alert('Unexpected response from the server.');
                }
            },
            error: function(e) {
                $('.spinner').hide();
                submitButton.css('background-color', '#2ecc71');  // Reset button color on error
                alert('An error occurred: ' + e.responseJSON.error);
            }
        });
    });

    function downloadCSV(results) {
        const songName = $('#songName').val() || "Your Song Name"; // Add your song name input or fallback value
        const dateSubmitted = new Date().toLocaleDateString(); // Current date
        const comparisonArtist = $('#singer').val(); // Get the comparison artist's name
    
        let csvContent = "data:text/csv;charset=utf-8,";
        csvContent += "Your Song," + songName + "\n";
        csvContent += "Date Submitted," + dateSubmitted + "\n";
        csvContent += "Comparison Artist:," + comparisonArtist + "\n\n";
        csvContent += "Comparison Artist Songs,Similarity\n";
    
        results.forEach(result => {
            csvContent += `${result.artist_song},${result.similarity.toFixed(2)}\n`;
        });
    
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', `${songName}.csv`);
        document.body.appendChild(link);   // Required for Firefox
        link.click();
        document.body.removeChild(link);
    }
});
