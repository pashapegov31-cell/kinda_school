const LoginPage = {
    async render() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="max-w-md mx-auto mt-16">
                <div class="card">
                    <h1 class="text-2xl font-bold text-gray-900 mb-6">Вход</h1>
                    <form id="login-form" novalidate>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                            <input type="email" name="email" class="input" placeholder="you@school.io" required />
                        </div>
                        <div class="mb-6">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Пароль</label>
                            <input type="password" name="password" class="input" placeholder="••••••••" required />
                        </div>
                        <button type="submit" class="btn btn-primary w-full">Войти</button>
                    </form>
                    <p class="mt-5 text-center text-sm text-gray-500">
                        Нет аккаунта?
                        <a href="/register" data-link class="text-indigo-600 hover:underline">Зарегистрироваться</a>
                    </p>
                </div>
            </div>`;

        document.getElementById('login-form').onsubmit = async (e) => {
            e.preventDefault();
            const form = e.target;
            const button = form.querySelector('button[type=submit]');
            button.disabled = true;
            try {
                const user = await Auth.login(form.email.value.trim(), form.password.value);
                Toast.show('С возвращением, ' + user.name + '!');
                Router.navigate(user.role === 'student' ? '/courses' : '/dashboard');
            } catch (error) {
                Toast.show(error.detail || 'Не удалось войти', 'error');
                button.disabled = false;
            }
        };
    },
};