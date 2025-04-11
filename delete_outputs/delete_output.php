<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Clear the output file
    $outputFile = '../output/output.txt';
    if (file_exists($outputFile)) {
        file_put_contents($outputFile, ''); // Wipe the file clean
        echo "<p style='color: green;'>Output file has been cleared.</p>";
    } else {
        echo "<p style='color: red;'>Output file not found.</p>";
    }
}
?>