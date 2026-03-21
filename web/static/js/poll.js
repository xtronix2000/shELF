const taskId = document.getElementById("task-id").dataset.id;

setInterval(function() {
    fetch("/api/status/" + taskId)
        .then(r => r.json())
        .then(data => {
            if (data.status === "done" || data.status === "failed") {
                location.reload();
            }
        });
}, 3000);