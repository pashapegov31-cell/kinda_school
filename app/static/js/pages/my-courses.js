const MyCoursesPage = {
    // progress в API приходит float; защищаемся от обеих трактовок (0..1 и 0..100)
    percent(value) {
        const v = Number(value) || 0;
        return v <= 1 ? v * 100 : v;
    },

    async render() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div>
                <h1 class="text-3xl font-bold text-gray-900 mb-8">Мои курсы</h1>
                <div id="my-list" class="space-y-4"></div>
            </div>`;

        const list = document.getElementById('my-list');

        let enrollments;
        try {
            enrollments = await Api.get('/enrollments/me');
        } catch (error) {
            list.innerHTML = emptyState('Не удалось загрузить записи: ' + error.detail);
            return;
        }

        if (!enrollments.length) {
            list.innerHTML = emptyState(
                'Вы ещё не записаны ни на один курс.',
                '<a href="/courses" data-link class="btn btn-primary">Выбрать курс</a>'
            );
            return;
        }

        // добираем данные курсов параллельно
        const rows = await Promise.all(
            enrollments.map(async (en) => {
                try {
                    return { en, course: await Api.get(`/courses/${en.course_id}`) };
                } catch (e) {
                    return { en, course: null };
                }
            })
        );

        list.innerHTML = rows.map(({ en, course }) => {
            if (!course) {
                return `<div class="card text-gray-500">Курс #${en.course_id} больше не доступен</div>`;
            }
            return `
                <div class="card">
                    <div class="flex flex-wrap justify-between items-start gap-3 mb-3">
                        <div class="min-w-0">
                            <h3 class="text-xl font-semibold text-gray-900">${esc(course.title)}</h3>
                            <p class="text-sm text-gray-500 mt-1">Запись от ${fmtDate(en.enrolled_at)}</p>
                        </div>
                        <div class="flex items-center gap-2">
                            ${en.completed ? '<span class="badge badge-published">Завершён</span>' : statusBadge(course.status)}
                        </div>
                    </div>
                    <div class="mb-4">${progressBar(this.percent(en.progress))}</div>
                    <div class="flex flex-wrap gap-3">
                        <a href="/courses/${course.id}" data-link class="btn btn-primary">Продолжить обучение</a>
                        <button class="btn btn-secondary" data-unenroll="${course.id}">Отписаться</button>
                    </div>
                </div>`;
        }).join('');

        list.addEventListener('click', (e) => {
            const btn = e.target.closest('[data-unenroll]');
            if (!btn) return;
            const courseId = btn.getAttribute('data-unenroll');
            Modal.confirm(
                'Отписаться от курса?',
                'Прогресс по урокам будет потерян.',
                async () => {
                    try {
                        await Api.delete(`/courses/${courseId}/enroll`);
                        Toast.show('Вы отписались от курса');
                        await this.render();
                    } catch (error) {
                        Toast.show(error.detail || 'Не удалось отписаться', 'error');
                    }
                },
                'Отписаться'
            );
        });
    },
};