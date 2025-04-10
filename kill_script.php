<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Search for the Python process running domain_lookup.py
    exec('wmic process where "name=\'python.exe\' and commandline like \'%domain_lookup.py%\'" get ProcessId', $output);

    // Extract the PID(s) from the output
    $pids = [];
    foreach ($output as $line) {
        if (is_numeric(trim($line))) {
            $pids[] = trim($line);
        }
    }

    if (!empty($pids)) {
        // Kill each process
        foreach ($pids as $pid) {
            exec("taskkill /F /PID $pid");
        }
        echo "<p style='color: green;'>Script(s) terminated successfully.</p>";
    } else {
        echo "<p style='color: red;'>No running script found to terminate.</p>";
    }
}
?>