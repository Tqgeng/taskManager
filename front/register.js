async function registerUser(username, password, email) {
    const response = await fetch("/jwt/register", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password,
            email: email
        })
    });

    if (response.ok) {
        console.log("Регистрация успешна, выполняем вход...");
        await loginUser(username, password); 
    } else {
        const error = await response.json();
        console.error("Ошибка регистрации:", error.detail);
    }
}

async function loginUser(username, password) {
    const response = await fetch("/jwt/login/", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            username: username,
            password: password
        })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        console.log("Вход выполнен, токен сохранён.");
        window.location.href = "/front/index.html"; 
    } else {
        const error = await response.json();
        console.error("Ошибка входа:", error.detail);
    }
}


document.getElementById("registerForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const email = document.getElementById("email").value;

    await registerUser(username, password, email);
});


