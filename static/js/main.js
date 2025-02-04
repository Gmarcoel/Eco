function nextTurn(turns) {
    fetch('/next_turn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `turns=${turns}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();  // Reload the page to show updated data
        }
    });
}