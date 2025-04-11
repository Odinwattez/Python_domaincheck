<!-- filepath: c:\wamp64\www\Python_domaincheck\index.php -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">	
    <title>Domain Lookup</title>
</head>
<body>
    <h1 class="main-title">
        <a href="index.php" class="plain-link">Domain Lookup</a>
        <a href="indexcheck.php" class="plain-link">Domain Check</a>     
    </h1>
    <h1 class="main-title">Watch out this one is very slow...</h1>

    <?php
set_time_limit(1200); // Allow the script to run for 20 minutes
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
        $uploadedFile = $_FILES['file']['tmp_name'];

        // Validate that the uploaded file is not empty
        if (filesize($uploadedFile) === 0) {
            echo "<p style='color: red;'>The uploaded file is empty. Please upload a valid file.</p>";
            exit;
        }

        $limit = isset($_POST['limit']) ? intval($_POST['limit']) : null;

        // Path to the Python script
        $pythonScript = 'C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Python\\Python313\\python.exe domain_check.py -f ' . escapeshellarg($uploadedFile) . ' -o output/output1.txt';
        if ($limit) {
            $pythonScript .= ' -l ' . escapeshellarg($limit);
        }

        // Add verbose mode if selected
        $verbose = isset($_POST['verbose']) ? '-v' : '';
        $pythonScript .= " $verbose";

        // Debugging: Log the command
        echo "<p>Executing command: $pythonScript</p>";

        // Execute the Python script in the background using start /B
        $command = "start /B $pythonScript";
        exec($command . ' > NUL 2>&1', $output, $returnVar);

    } else {
        echo "<p style='color: red;'>Please upload a valid file.</p>";
    }
}
?>

<form class="upload-form" action="indexcheck.php" method="POST" enctype="multipart/form-data">
<label class="upload-label" for="file-upload">Upload een bestand:</label>
    
    <div class="file-upload-wrapper">
        <input id="file-upload" type="file" name="file">
        <label for="file-upload" class="custom-file-button">Bestand kiezen</label>
        <span id="file-name">Geen bestand gekozen</span>
    </div>
    
    <label class="limit-label" for="limit">Limit the number of domains:</label>
    <input class="limit-input" type="number" name="limit" id="limit" placeholder="e.g., 200"><br><br>

    <label for="verbose">Verbose Mode:</label>
    <input type="checkbox" name="verbose" id="verbose">
    
    <button class="process-button" type="submit" name="action" value="process">Process Domains</button>
</form>

<div class="kill-section">
    <div class="button-container">
        <form class="kill-form" action="kill_scripts/kill_script1.php" method="POST">
            <button class="kill-button" type="submit" name="action" value="kill">Kill Running Script</button>
        </form>
        <form class="output-form" action="delete_outputs/delete_output1.php" method="POST">
            <button class="delete-button" type="submit" name="action" value="Empty">Delete the output</button>
        </form>
    </div>
</div>

<div class="results-section">
    <h2 class="results-title">Real-Time Results</h2>
    <pre class="results-output" id="output"></pre>
</div>

<div class="download-section" id="download" style="display: none;">
    <h2 class="download-title">Download Results</h2>
    <a class="download-link" href="output/output1.txt" download>
        <button class="download-button">Download Output</button>
    </a>
</div>

    <script>
        document.getElementById("file-upload").addEventListener("change", function() {
        var fileName = this.files.length > 0 ? this.files[0].name : "Geen bestand gekozen";
        document.getElementById("file-name").textContent = fileName;
        });

        function fetchResults() {
            const outputElement = document.getElementById('output');
            const downloadElement = document.getElementById('download');

            fetch('output/output1.txt')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch results.');
                    }
                    return response.text();
                })
                .then(data => {
                    outputElement.textContent = data;

                    // Show the download button when processing is complete
                    if (data.includes('END_OF_RESULTS')) {
                        downloadElement.style.display = 'block';
                        clearInterval(fetchInterval); // Stop fetching updates
                    }
                })
                .catch(error => {
                    console.error('Error fetching results:', error);
                });
        }

        // Periodically fetch results every 2 seconds
        const fetchInterval = setInterval(fetchResults, 2000);
    </script>
</body>
</html>