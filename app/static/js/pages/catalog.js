const CatalogPage = {
    async render() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div>
                <div class="flex flex-wrap justify-between items-end gap-4 mb-8">
                    <div>
                        <h1 class="text-3xl font-bold text-gray-900">Каталог курсов</h1>
                        <p class="text-gray-500 mt-1">Опубликованные курсы платформы</p>
                    </div>
                </div>
                <div id="catalog-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
            </div>`;

        const grid = document.getElementById('catalog-grid');

        try {
            const courses = await Api.get('/courses?limit=100');

            if (!courses.length) {
                grid.className = '';
                grid.innerHTML = emptyState(
                    'Пока нет опубликованных курсов.',
                    Auth.isTeacher() || Auth.isAdmin()
                        ? '<a href="/dashboard" data-link class="btn btn-primary">Создать первый курс</a>'
                        : ''
                );
                return;
            }

            grid.innerHTML = courses.map((c) => CourseCard(c)).join('');
        } catch (error) {
            grid.className = '';
            grid.innerHTML = emptyState('Не удалось загрузить курсы: ' + error.detail);
        }
    },
};