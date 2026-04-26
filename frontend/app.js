const token = localStorage.getItem('token');

// 🔐 если нет токена — назад на логин
if (!token) {
    window.location.href = 'login.html';
}

// 📋 загрузка задач
async function loadTasks() {
    const response = await fetch('http://127.0.0.1:8000/api/v1/tasks/', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });

    const data = await response.json();

    const list = document.getElementById('tasks');
    list.innerHTML = '';

    data.results.forEach(task => {
        const li = document.createElement('li');
        li.innerText = task.title + ' (' + task.status + ')';
        list.appendChild(li);
    });
}

// 🚪 выход
function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}