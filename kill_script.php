<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Execute the Python kill script
    $output = [];
    $returnVar = 0;

    // Path to Python executable and kill_script.py
    $pythonPath = 'C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
    $killScriptPath = 'kill_script.py';

    // Execute the Python script
    exec("$pythonPath $killScriptPath", $output, $returnVar);

    // Display the output
    echo "<pre>" . implode("\n", $output) . "</pre>";
    if ($returnVar === 0) {
        echo "<p style='color: green;'>Kill script executed successfully.</p>";
    } else {
        echo "<p style='color: red;'>Failed to execute the kill script.</p>";
    }
}
?>