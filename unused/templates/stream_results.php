<?php
set_time_limit(300); // Allow the script to run for 5 minutes
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
header('Access-Control-Allow-Origin: *');

// Check if a file was uploaded
if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    $uploadedFile = $_FILES['file']['tmp_name'];
    $limit = isset($_POST['limit']) ? intval($_POST['limit']) : null;

    // Debugging: Log the uploaded file and form data
    echo "data: Debug: Uploaded file: $uploadedFile\n\n";
    echo "data: Debug: Limit: $limit\n\n";
    ob_flush();
    flush();

    // Prepare the cURL request to the Flask backend
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://localhost:5000/check_domains");
    curl_setopt($ch, CURLOPT_POST, true);

    // Attach the file and other form data
    $postData = [
        'file' => new CURLFile($uploadedFile, $_FILES['file']['type'], $_FILES['file']['name']),
    ];
    if ($limit) {
        $postData['limit'] = $limit;
    }
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

    // Return the response incrementally
    curl_setopt($ch, CURLOPT_WRITEFUNCTION, function ($ch, $data) {
        echo "data: " . trim($data) . "\n\n";
        ob_flush();
        flush();
        return strlen($data);
    });

    // Execute the request
    if (!curl_exec($ch)) {
        $error = curl_error($ch);
        echo "data: Error: cURL error: $error\n\n";
        ob_flush();
        flush();
    }
    curl_close($ch);

    // Signal the end of the stream
    echo "data: END_OF_RESULTS\n\n";
    ob_flush();
    flush();
} else {
    echo "data: Error: No valid file uploaded.\n\n";
    ob_flush();
    flush();
}
?>