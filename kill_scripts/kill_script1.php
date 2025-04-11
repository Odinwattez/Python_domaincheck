<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Execute the Python kill script
    $output = [];
    $returnVar = 0;

    // Path to Python executable and kill_script.py
    $pythonPath = 'C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
    $killScriptPath = '../kill_scripts/kill_script1.py';

    // Execute the Python script to terminate the running process
    exec("$pythonPath $killScriptPath", $output, $returnVar);

    // Display the output of the kill script
    echo "<pre>" . implode("\n", $output) . "</pre>";
    if ($returnVar === 0) {
        echo "<p style='color: green;'>Kill script executed successfully.</p>";
    } else {
        echo "<p style='color: red;'>Failed to execute the kill script.</p>";
    }
}
?>