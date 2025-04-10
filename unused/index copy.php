<!-- filepath: c:\wamp64\www\Python_domaincheck\index.php -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Domain Lookup</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-top: 20px;
        }

        form, .output, .kill-button {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }

        input[type="file"],
        input[type="number"],
        button {
            display: block;
            width: 100%;
            margin-bottom: 15px;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        .kill-button button {
            background-color: #dc3545;
        }

        .kill-button button:hover {
            background-color: #c82333;
        }

        .output pre {
            background: #f4f4f9;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>Domain Lookup</h1>

    <?php
set_time_limit(1200); // Allow the script to run for 20 minutes

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['kill_script'])) {
    // Kill the running script
    $pidFile = 'pid.txt';
    if (file_exists($pidFile)) {
        $previousPid = file_get_contents($pidFile);
        if (is_numeric($previousPid)) {
            // Check if the process is still running
            exec("tasklist /FI \"PID eq $previousPid\" 2>&1", $output);
            if (count($output) > 1) {
                exec("taskkill /F /PID $previousPid");
                echo "<p style='color: green;'>Script has been terminated.</p>";
            } else {
                echo "<p style='color: orange;'>No running process found for PID $previousPid. Cleaning up stale PID file.</p>";
            }
            unlink($pidFile); // Remove the PID file
        } else {
            echo "<p style='color: red;'>No valid PID found to terminate.</p>";
        }
    } else {
        echo "<p style='color: red;'>No running script found.</p>";
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    if ($_FILES['file']['error'] === UPLOAD_ERR_OK) {
        $uploadedFile = $_FILES['file']['tmp_name'];

        // Validate that the uploaded file is not empty
        if (filesize($uploadedFile) === 0) {
            echo "<p style='color: red;'>The uploaded file is empty. Please upload a valid file.</p>";
            exit;
        }

        $limit = isset($_POST['limit']) ? intval($_POST['limit']) : null;

        // Path to the Python script
        $pythonScript = 'C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Python\\Python313\\python.exe domain_lookup.py -f ' . escapeshellarg($uploadedFile) . ' -o output/output.txt';
        if ($limit) {
            $pythonScript .= ' -l ' . escapeshellarg($limit);
        }

        // Terminate any previously running script
        $pidFile = 'pid.txt';
        if (file_exists($pidFile)) {
            $previousPid = file_get_contents($pidFile);
            if (is_numeric($previousPid)) {
                exec("tasklist /FI \"PID eq $previousPid\" 2>&1", $output);
                if (count($output) > 1) {
                    exec("taskkill /F /PID $previousPid");
                }
                unlink($pidFile);
            }
        }

        // Start the new Python script and store its PID
        $command = "$pythonScript";
        exec($command . ' > /dev/null 2>&1 & echo $!', $output);
        $newPid = $output[0] ?? null;

        if ($newPid) {
            file_put_contents($pidFile, $newPid);
        }

        // Debugging: Log the command
        echo "<p>Executing command: $pythonScript</p>";

        // Debugging: Output the result
        echo "<pre>Output:\n" . implode("\n", $output) . "</pre>";
        if ($newPid) {
            file_put_contents($pidFile, $newPid);
            echo "<p>New PID: $newPid</p>";
        } else {
            echo "<p style='color: red;'>Failed to retrieve the PID of the Python script.</p>";
        }
    }
}
?>

    <form action="index.php" method="POST" enctype="multipart/form-data">
        <label for="file">Upload a file with domains:</label>
        <input type="file" name="file" id="file" required><br><br>
        
        <label for="limit">Limit the number of domains:</label>
        <input type="number" name="limit" id="limit" placeholder="e.g., 200"><br><br>
        
        <button type="submit">Process Domains</button>
    </form>

    <div class="kill-button">
        <form action="index.php" method="POST">
            <button type="submit" name="kill_script">Kill Running Script</button>
        </form>
    </div>

    <div id="results">
        <h2>Real-Time Results</h2>
        <pre id="output"></pre>
    </div>

    <div id="download" style="display: none;">
        <h2>Download Results</h2>
        <a href="output/output.txt" download>
            <button>Download Output</button>
        </a>
    </div>

    <script>
        function fetchResults() {
            const outputElement = document.getElementById('output');
            const downloadElement = document.getElementById('download');

            fetch('output/output.txt')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch results.');
                    }
                    return response.text();
                })
                .then(data => {
                    console.log('Fetched data:', data); // Debugging: Log the fetched data
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

        // Periodically fetch results every 5 seconds
        const fetchInterval = setInterval(fetchResults, 5000);
    </script>
</body>
</html>