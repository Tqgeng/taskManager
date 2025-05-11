async function getTasks() {
    const token = localStorage.getItem('token'); 
    const response = await fetch("/tasks/", {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });
    if (response.ok === true) {
        const tasks = await response.json();
        console.log(tasks);
        const rows = document.querySelector("tbody");
        rows.innerHTML = '';
        tasks.forEach(task => rows.append(row(task)));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function getTask(id) {
    const token = localStorage.getItem('token');
    const response = await fetch(`/tasks/${id}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });
    if (response.ok === true) {
        const task = await response.json();
        document.getElementById("taskId").value = task.id;
        document.getElementById("taskName").value = task.title;
        document.getElementById("taskDescription").value = task.description;
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function createTask(taskName, taskDescription) {
    const token = localStorage.getItem('token');
    const response = await fetch("/tasks/", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            title: taskName,
            description: taskDescription
        })
    });
    if (response.ok === true) {
        const task = await response.json();
        document.querySelector("tbody").append(row(task));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function editTask(taskId, taskName, taskDescription) {
    const token = localStorage.getItem('token');
    const response = await fetch(`/tasks/${taskId}`, {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            id: taskId,
            title: taskName,
            description: taskDescription
        })
    });
    if (response.ok === true) {
        const task = await response.json();
        document.querySelector(`tr[data-rowid='${task.id}']`).replaceWith(row(task));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function deleteTask(id) {
    const token = localStorage.getItem('token');
    const response = await fetch(`/tasks/${id}`, {
        method: "DELETE",
        headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });
    if (response.ok === true) {
        const task = await response.json();
        document.querySelector(`tr[data-rowid='${task.id}']`).remove();
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function updateTaskStatus(taskId, completedStatus) {
    const token = localStorage.getItem('token');
    const response = await fetch(`/tasks/${taskId}/status`, {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            completed: completedStatus
        })
    });

    if (response.ok) {
        const updatedTask = await response.json();
        updateTaskRow(updatedTask);  // Обновляем строку без перезагрузки
    } else {
        console.error("Ошибка обновления статуса:", await response.json());
    }
}

function reset() {
    document.getElementById("taskId").value = 
    document.getElementById("taskName").value = 
    document.getElementById("taskDescription").value = "";
}

function row(task) {
    const tr = document.createElement("tr");
    tr.setAttribute("data-rowid", task.id);
    if (task.completed) tr.classList.add("completed");

    const nameTd = document.createElement("td");
    nameTd.append(task.title);
    tr.append(nameTd);

    const descriptionTd = document.createElement("td");
    descriptionTd.append(task.description || "Нет описания");
    tr.append(descriptionTd);

    const completedTd = document.createElement("td");
    completedTd.textContent = task.completed ? "✅ Выполнено" : "⏳ В процессе";
    tr.append(completedTd);

    const linksTd = document.createElement("td");

    const editLink = document.createElement("button"); 
    editLink.append("Изменить");
    editLink.addEventListener("click", async() => await getTask(task.id));
    linksTd.append(editLink);

    const completeBtn = document.createElement("button");
    completeBtn.textContent = task.completed ? "Возобновить" : "Завершить";
    completeBtn.addEventListener("click", async () => {
        await updateTaskStatus(task.id, !task.completed);
    });
    linksTd.append(completeBtn);

    const removeLink = document.createElement("button"); 
    removeLink.append("Удалить");
    removeLink.addEventListener("click", async () => await deleteTask(task.id));

    linksTd.append(removeLink);
    tr.appendChild(linksTd);


    return tr;
}


document.getElementById("resetButton").addEventListener("click", () => reset());

document.getElementById("saveButton").addEventListener("click", async () => {
    const id = document.getElementById("taskId").value;
    const name = document.getElementById("taskName").value;
    const description = document.getElementById("taskDescription").value;
    if (id === "")
        await createTask(name, description);
    else
        await editTask(id, name, description);
    reset();
});

function logoutUser() {
    localStorage.removeItem("token");
    console.log("Выход выполнен, токен удалён.");
    window.location.href = "/front/login.html";
}

document.getElementById("logoutButton")?.addEventListener("click", logoutUser);

getTasks();
