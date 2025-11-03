document.getElementById('extractor-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const url = document.getElementById('url').value.trim();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const headless = document.getElementById('headless').checked;

    const spinner = document.getElementById('spinner');
    const resultsContainer = document.getElementById('results-container');
    const resultMessage = document.getElementById('result-message');
    const results = document.getElementById('results');
    const downloadLink = document.getElementById('download-link');

    spinner.style.display = 'block';
    resultsContainer.style.display = 'none';
    downloadLink.style.display = 'none';

    try {
        // ✅ include username and password in payload
        const response = await fetch('/extract', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, username, password, headless })
        });

        const data = await response.json();

        if (response.ok) {
            resultMessage.textContent = `✅ Found ${data.links.length} header links:`;
            results.textContent = JSON.stringify(data.links, null, 2);
            resultsContainer.style.display = 'block';

            // Enable Zip download
            if (data.zip_file) {
                downloadLink.href = `/${data.zip_file}`;
                downloadLink.download = data.zip_file;
                downloadLink.textContent = `⬇️ Download ${data.zip_file}`;
                downloadLink.style.display = 'inline-block';
            }
        } else {
            resultMessage.textContent = `❌ Error: ${data.error}`;
            results.textContent = '';
            resultsContainer.style.display = 'block';
        }
    } catch (error) {
        resultMessage.textContent = `❌ Network Error: ${error.message}`;
        results.textContent = '';
        resultsContainer.style.display = 'block';
    } finally {
        spinner.style.display = 'none';
    }
});
