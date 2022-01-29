function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.href = "/";
    });
}