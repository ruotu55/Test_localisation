document.addEventListener('DOMContentLoaded', () => {
    const subjectInput = document.getElementById('subjectInput');
    const searchButton = document.getElementById('searchButton');
    const videoResultsUl = document.getElementById('videoResults');
    const processedVideosUl = document.getElementById('processedVideos');
    const clearProcessedButton = document.getElementById('clearProcessed');

    // --- Simulated "Processed Videos" Storage ---
    // In a real application, this would be stored in a database, Google Sheets, etc.
    // For this demo, we'll use Local Storage to persist across browser sessions.
    let processedVideoUrls = new Set(JSON.parse(localStorage.getItem('processedVideoUrls') || '[]'));

    // Function to render processed videos list
    function renderProcessedVideos() {
        processedVideosUl.innerHTML = ''; // Clear existing list
        if (processedVideoUrls.size === 0) {
            processedVideosUl.innerHTML = '<li>No videos processed yet.</li>';
            return;
        }
        processedVideoUrls.forEach(url => {
            const li = document.createElement('li');
            li.classList.add('processed-item'); // Add class for styling
            li.innerHTML = `<a href="${url}" target="_blank">${url}</a>`;
            processedVideosUl.appendChild(li);
        });
    }

    // Function to add a video to processed list
    function addVideoToProcessed(url) {
        if (!processedVideoUrls.has(url)) {
            processedVideoUrls.add(url);
            localStorage.setItem('processedVideoUrls', JSON.stringify(Array.from(processedVideoUrls)));
            renderProcessedVideos();
            console.log(`Video added to processed list: ${url}`);
        } else {
            console.log(`Video already in processed list: ${url}`);
        }
    }

    // Function to handle the "Process" button click (simulated)
    function handleProcessClick(url, buttonElement) {
        if (!processedVideoUrls.has(url)) {
            addVideoToProcessed(url);
            buttonElement.textContent = 'Processed!';
            buttonElement.disabled = true; // Disable button after processing
            buttonElement.style.backgroundColor = '#28a745'; // Green color for processed
            buttonElement.style.cursor = 'default';
        }
    }

    // --- Simulated Search Function ---
    // IMPORTANT: In a real web application, directly calling external APIs
    // from client-side JavaScript is often not allowed due to CORS policies,
    // API key security, and rate limits. You would typically have a BACKEND SERVER
    // that makes the actual API call (e.g., to YouTube Data API or a custom scraper)
    // and then sends the results to your frontend.

    async function performSimulatedSearch(subject) {
        videoResultsUl.innerHTML = '<li>Searching...</li>'; // Show loading message

        // This is where I, as your AI assistant, would perform the search using my tools.
        // For the purpose of this interactive demo in your browser, we'll simulate results.
        // If you were running this on a server, you'd replace this with actual API calls.

        // Simulating a delay to mimic network request
        await new Promise(resolve => setTimeout(resolve, 1500));

        let simulatedResults = [];

        // Generate some dummy URLs based on the subject
        if (subject.toLowerCase().includes('pranks')) {
            simulatedResults = [
                { title: 'Top 10 Viral Pranks of 2024', url: 'https://www.youtube.com/watch?v=viral_prank_1' },
                { title: 'Best Public Prank Compilations', url: 'https://www.youtube.com/watch?v=public_prank_2' },
                { title: 'Funny Office Pranks Gone Wrong', url: 'https://www.youtube.com/watch?v=office_prank_3' },
                { title: 'New Pranks for Your Friends', url: 'https://www.youtube.com/watch?v=friends_prank_4' }
            ];
        } else if (subject.toLowerCase().includes('cooking')) {
            simulatedResults = [
                { title: 'Easy Dinner Recipes for Weeknights', url: 'https://www.youtube.com/watch?v=easy_cooking_1' },
                { title: 'Mastering Italian Cuisine', url: 'https://www.youtube.com/watch?v=italian_cooking_2' },
                { title: 'Baking Desserts 101', url: 'https://www.youtube.com/watch?v=baking_desserts_3' }
            ];
        } else {
            simulatedResults = [
                { title: `General Video about ${subject} 1`, url: `https://www.youtube.com/watch?v=general_${subject}_1` },
                { title: `General Video about ${subject} 2`, url: `https://www.youtube.com/watch?v=general_${subject}_2` }
            ];
        }
        
        displaySearchResults(simulatedResults);
    }

    // Function to display search results
    function displaySearchResults(results) {
        videoResultsUl.innerHTML = ''; // Clear previous results

        if (results.length === 0) {
            videoResultsUl.innerHTML = '<li>No videos found for this subject.</li>';
            return;
        }

        results.forEach(video => {
            const li = document.createElement('li');
            const isProcessed = processedVideoUrls.has(video.url);

            li.innerHTML = `
                <a href="${video.url}" target="_blank">${video.title}</a>
                <button class="process-btn" data-url="${video.url}" ${isProcessed ? 'disabled style="background-color: #28a745; cursor: default;"' : ''}>
                    ${isProcessed ? 'Processed!' : 'Mark as Processed'}
                </button>
            `;
            videoResultsUl.appendChild(li);

            // Add event listener to the newly created button
            const processButton = li.querySelector('.process-btn');
            if (!isProcessed) { // Only add listener if not already processed
                processButton.addEventListener('click', () => handleProcessClick(video.url, processButton));
            }
        });
    }

    // --- Event Listeners ---
    searchButton.addEventListener('click', () => {
        const subject = subjectInput.value.trim();
        if (subject) {
            performSimulatedSearch(subject);
        } else {
            alert('Please enter a subject to search for!');
        }
    });

    // Allow searching by pressing Enter key
    subjectInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            searchButton.click();
        }
    });

    clearProcessedButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear the processed videos list?')) {
            processedVideoUrls.clear();
            localStorage.removeItem('processedVideoUrls'); // Clear from local storage
            renderProcessedVideos();
            // Re-render search results if any, to reflect cleared status
            // This would require storing current search results or re-running search
            // For simplicity, we won't re-run search here, but in a real app you might.
        }
    });

    // Initial render of processed videos when page loads
    renderProcessedVideos();
});
