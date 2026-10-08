const DashboardPage = {
    async render() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div>
                <div class="flex flex-wrap justify-between items-end gap-4 mb-8">
                    <div>
                        <h1 class="text-3xl font-bold text-gray-900">Мои курсы</h1>
                        <p class="text-gray-500 mt-1">Создание, редактирование и публикация</p>
                    </div>
                    <button id="create-course-btn" class="btn btn-primary">+ Создать курс</button>
                </div>
                <div id="dash-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
            </div>`;

        document.getElementById('create-course-btn').onclick = () => this.openCreateModal();
        await this.load();
    },

    async load() {
        const grid = document.getElementById('dash-grid');
        try {
            const courses = await Api.get('/courses/mine?limit=100');

            if (!courses.length) {
                grid.className = '';
                grid.innerHTML = emptyState('У вас пока нет курсов. Создайте первый!');
                return;
            }

            grid.innerHTML = courses.map((c) => `
                <div class="card flex flex-col">
                    <div class="flex justify-between items-start gap-2 mb-3">
                        <h3 class="text-lg font-semibold text-gray-900">${esc(c.title)}</h3>
                        ${statusBadge(c.status)}
                    </div>
                    <p class="text-gray-600 text-sm mb-4 line-clamp-3 flex-1">${esc(c.description)}</p>
                    <div class="flex justify-between items-center mb-4">
                        <span class="text-xl font-bold text-indigo-600">${fmtPrice(c.price)}</span>
                        <span class="text-xs text-gray-400">${fmtDate(c.created_at)}</span>
                    </div>
                    <div class="flex gap-2">
                        <a href="/dashboard/courses/${c.id}" data-link class="btn btn-primary flex-1">Управлять</a>
                        <a href="/courses/${c.id}" data-link class="btn btn-secondary">Вид</a>
                    </div>
                </div>`).join('');
        } catch (error) {
            grid.className = '';
            grid.innerHTML = emptyState('Не удалось загрузить курсы: ' + error.detail);
        }
    },

    openCreateModal() {
        const overlay = Modal.open(`
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Новый курс</h3>
            <form id="create-course-form">
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Название</label>
                    <input name="title" class="input" maxlength="255" required />
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Описание</label>
                    <textarea name="description" class="input" required></textarea>
                </div>
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Цена, ₽</label>
                    <input name="price" type="number" min="0" step="0.01" class="input" required />
                </div>
                <div class="flex justify-end gap-3">
                    <button type="button" class="btn btn-secondary" data-cancel>Отмена</button>
                    <button type="submit" class="btn btn-primary">Создать</button>
                </div>
            </form>`);

        overlay.querySelector('[data-cancel]').onclick = () => overlay.remove();

        overlay.querySelector('#create-course-form').onsubmit = async (e) => {
            e.preventDefault();
            const form = e.target;
            const button = form.querySelector('button[type=submit]');
            button.disabled = true;
            try {
                const course = await Api.post('/courses', {
                    title: form.title.value.trim(),
                    description: form.description.value.trim(),
                    price: Number(form.price.value),
                });
                overlay.remove();
                Toast.show('Курс создан: черновик с базовым уроком');
                Router.navigate('/dashboard/courses/' + course.id);
            } catch (error) {
                Toast.show(error.detail || 'Не удалось создать курс', 'error');
                button.disabled = false;
            }
        };
    },
};