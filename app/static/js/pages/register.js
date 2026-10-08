const RegisterPage = {
    async render() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="max-w-md mx-auto mt-16">
                <div class="card">
                    <h1 class="text-2xl font-bold text-gray-900 mb-6">Регистрация</h1>
                    <p class="text-sm text-gray-500 mb-4">Новые аккаунты создаются с ролью «student».</p>
                    <form id="register-form" novalidate>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Имя</label>
                            <input type="text" name="name" class="input" placeholder="Иван Петров" required />
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                            <input type="email" name="email" class="input" placeholder="you@school.io" required />
                        </div>
                        <div class="mb-6">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Пароль</label>
                            <input type="password" name="password" class="input" placeholder="Минимум 8 символов" minlength="8" required />
                        </div>
                        <button type="submit" class="btn btn-primary w-full">Создать аккаунт</button>
                    </form>
                    <p class="mt-5 text-center text-sm text-gray-500">
                        Уже есть аккаунт?
                        <a href="/login" data-link class="text-indigo-600 hover:underline">Войти</a>
                    </p>
                </div>
            </div>`;

        document.getElementById('register-form').onsubmit = async (e) => {
            e.preventDefault();
            const form = e.target;
            const button = form.querySelector('button[type=submit]');
            button.disabled = true;
            try {
                const user = await Auth.register(
                    form.email.value.trim(),
                    form.name.value.trim(),
                    form.password.value
                );
                Toast.show('Аккаунт создан. Добро пожаловать!');
                Router.navigate('/courses');
            } catch (error) {
                Toast.show(error.detail || 'Не удалось зарегистрироваться', 'error');
                button.disabled = false;
            }
        };
    },
};