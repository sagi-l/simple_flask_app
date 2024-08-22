function moveTask(taskId, direction) {
    const taskList = document.getElementById('task-list');
    const task = document.getElementById('task-' + taskId);
    if (direction === 'up' && task.previousElementSibling) {
        taskList.insertBefore(task, task.previousElementSibling);
    } else if (direction === 'down' && task.nextElementSibling) {
        taskList.insertBefore(task.nextElementSibling, task);
    }

    // Send the new order to the server (optional)
    const tasks = Array.from(taskList.children).map(li => li.id.replace('task-', ''));
    fetch('/update-task-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tasks }),
    });
}
