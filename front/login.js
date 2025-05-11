document.addEventListener("click", (event) => {
    if (event.target && event.target.id === "registerBtn") {
        window.location.href = "/front/register.html";
    }
});


document.getElementById("loginButton").addEventListener("click", async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Пожалуйста, заполните все поля.");
        return;
    }

    // Создаем FormData объект для отправки данных как 'application/x-www-form-urlencoded'
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch("/jwt/login/", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        const token = data.access_token;

        // Сохранение токена в LocalStorage
        localStorage.setItem("token", token);

        // Перенаправление на страницу с задачами
        window.location.href = "/front/index.html";
    } else {
        // Показ ошибки
        const errorData = await response.json();
        console.log('Ошибка при авторизации:', errorData.detail || errorData.message);
        document.getElementById("error-message").style.display = "block";
    }
});

