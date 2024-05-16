const {EditorServiceClient} = require('./editor_grpc_web_pb.js');
const {InsertRequest, DeleteRequest} = require('./editor_pb.js');

const client = new EditorServiceClient('http://localhost:8080', null, null);


// Websocket to handle real time updates of the textarea
const socket = io('http://localhost:5000');  

socket.on('connect', function() {
    console.log('Connected to WebSocket server');
});

socket.on('document_update', function(data) {
    document.getElementById('editor').value = data.text;
});


// Function to send text insertions to server
function insertText(text, position) {
    const request = new InsertRequest();
    request.setText(text);
    request.setPosition(position);
    client.insertText(request, {}, (err, response) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log('Text inserted successfully');
        
    });
}

// Function to handle text deletions
function deleteText(startPosition, endPosition) {
    const request = new DeleteRequest();
    request.setStartPosition(startPosition);
    request.setEndPosition(endPosition);
    client.deleteText(request, {}, (err, response) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log('Text deleted successfully');
        
    });
}

// Function to get latest version of document
function fetchDocument() {
    const request = new editor_pb.FetchRequest();
    client.fetchDocument(request, {}, (err, response) => {
        if (err) {
            console.error('Failed to fetch document:', err);
            return;
        }
        // Update the textarea with the fetched document text
        document.getElementById('editor').value = response.getText();
    });
}

// Debounce function to reduce spamming the server
function debounce(func, delay) {
    let timeoutId;

    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

const debouncedInsertText = debounce(insertText, 300);
const debouncedDeleteText = debounce(deleteText, 300);
const debouncedFetchDocument = debounce(fetchDocument, 300);

// Event listener for the editor focus
// Sets previous value of the text area when it gains focus
document.getElementById('editor').addEventListener('focus', function(event) {
    this.previousValue = event.target.value;
});


// Event listeners for the editor input
// Does not handle paste event
document.getElementById('editor').addEventListener('input', function(event) {
    const textarea = event.target;
    const currentValue = textarea.value;  

    // Keep track of area that user is editing
    const selectionStart = textarea.selectionStart;
    const selectionEnd = textarea.selectionEnd;

    const previousValue = this.previousValue || '';

    if (selectionStart === selectionEnd) {  // No text is selected (user is adding or deleting single letters)
        if (currentValue.length > previousValue.length) {  // Text was inserted
            const insertedText = currentValue.substring(selectionStart - 1, selectionStart);

            insertText(insertedText, selectionStart - 1);
        } else {  // Text was deleted
            // Calculate deleted range assuming single character deletion for simplicity
            const deletedRangeStart = previousValue.length > currentValue.length ? selectionStart : selectionStart + 1;
            // Call function to handle deletion
            deleteText(deletedRangeStart, deletedRangeStart + 1);
        }
    } 
    else {  // Text is selected, indicating deletion
        deleteText(selectionStart, selectionEnd);
    }

    // Update the previous value for the next event
    this.previousValue = currentValue;
});

// Event listener for the paste event
document.getElementById('editor').addEventListener('paste', function(event) {
    const pastedText = event.clipboardData.getData('text'); // Get the pasted text
    const textarea = event.target;
    const insertionPoint = textarea.selectionStart; // Get the insertion point

    // Prevent the default paste action to manually handle the text insertion
    event.preventDefault();


    insertText(pastedText, insertionPoint);

    // manually update the textarea value and the cursor position
    const currentValue = textarea.value;
    textarea.value = currentValue.slice(0, insertionPoint) + pastedText + currentValue.slice(textarea.selectionEnd);
    textarea.setSelectionRange(insertionPoint + pastedText.length, insertionPoint + pastedText.length);

    // Update the previous value for the next input event
    this.previousValue = textarea.value;
});


