const CourseEditPage = {
    params: null,

    async render(params) {
        this.params = params;
        const content = document.getElementById('content');

        let course;
        try {
            course = await Api.get(`/courses/${params.id}`);
        } catch (error) {
            content.innerHTML = emptyState(
                'Курс не найден.',
                '<a href="/dashboard" data-link class="btn btn-primary">К моим курсам</a>'
            );
            return;
        }

        const user = Auth.getUser();
        if (user.id !== course.teacher_id && !Auth.isAdmin()) {
            Toast.show('Управлять курсом может только его автор', 'error');
            Router.navigate('/dashboard', true);
            return;
        }

        content.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <a href="/dashboard" data-link class="text-indigo-600 hover:underline text-sm mb-6 inline-block">← Мои курсы</a>

                <div class="card mb-8">
                    <div class="flex flex-wrap justify-between items-start gap-3 mb-2">
                        <h1 class="text-2xl font-bold text-gray-900">${esc(course.title)}</h1>
                        ${statusBadge(course.status)}
                    </div>
                    <p class="text-gray-600 mb-6">${esc(course.description)}</p>
                    <div class="flex flex-wrap gap-3">
                        ${course.status === 'draft' ? '<button id="publish-btn" class="btn btn-primary">Опубликовать</button>' : ''}
                        <a href="/courses/${course.id}" data-link class="btn btn-secondary">Посмотреть как студент</a>
                        <button id="delete-course-btn" class="btn btn-danger">Удалить курс</button>
                    </div>
                </div>

                <div class="flex flex-wrap justify-between items-center gap-3 mb-4">
                    <h2 class="text-xl font-bold text-gray-900">Уроки</h2>
                    <button id="add-lesson-btn" class="btn btn-primary">+ Добавить урок</button>
                </div>
                <div id="lessons-admin-list"></div>
            </div>`;

        const publishBtn = document.getElementById('publish-btn');
        if (publishBtn) {
            publishBtn.onclick = async () => {
                publishBtn.disabled = true;
                try {
                    await Api.post(`/courses/${course.id}/publish`);
                    Toast.show('Курс опубликован и виден в каталоге');
                    await this.render(params);
                } catch (error) {
                    Toast.show(error.detail || 'Не удалось опубликовать', 'error');
                    publishBtn.disabled = false;
                }
            };
        }

        document.getElementById('delete-course-btn').onclick = () => {
            Modal.confirm(
                'Удалить курс?',
                'Вместе с курсом удалятся все уроки, записи студентов и прогресс. Действие необратимо.',
                async () => {
                    try {
                        await Api.delete(`/courses/${course.id}`);
                        Toast.show('Курс удалён');
                        Router.navigate('/dashboard');
                    } catch (error) {
                        Toast.show(error.detail || 'Не удалось удалить курс', 'error');
                    }
                }
            );
        };

        document.getElementById('add-lesson-btn').onclick = () => this.openLessonModal(course, null);

        await this.loadLessons(course);
    },

    async loadLessons(course) {
        const list = document.getElementById('lessons-admin-list');
        let lessons = [];
        try {
            lessons = await Api.get(`/courses/${course.id}/lessons?limit=100`);
        } catch (error) {
            list.innerHTML = emptyState('Не удалось загрузить уроки: ' + error.detail);
            return;
        }

        this.lessons = lessons;

        if (!lessons.length) {
            list.innerHTML = emptyState('В курсе нет уроков.');
            return;
        }

        list.innerHTML = lessons.map((l) => `
            <div class="card mb-3 flex flex-wrap items-center gap-4">
                <div class="w-9 h-9 shrink-0 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-semibold">${l.order}</div>
                <div class="flex-1 min-w-0">
                    <h4 class="font-medium text-gray-900 truncate">${esc(l.title)}</h4>
                    <p class="text-sm text-gray-500">${l.duration_minutes ? l.duration_minutes + ' мин' : 'длительность не указана'}</p>
                </div>
                <div class="flex gap-2">
                    <a href="/courses/${course.id}/lessons/${l.id}" data-link class="btn btn-secondary text-sm">Открыть</a>
                    <button class="btn btn-secondary text-sm" data-edit="${l.id}">Изменить</button>
                    <button class="btn btn-danger text-sm" data-delete="${l.id}">Удалить</button>
                </div>
            </div>`).join('');

        list.onclick = (e) => {
            const editBtn = e.target.closest('[data-edit]');
            const deleteBtn = e.target.closest('[data-delete]');

            if (editBtn) {
                const lesson = lessons.find((l) => l.id === Number(editBtn.getAttribute('data-edit')));
                this.openLessonModal(course, lesson);
            }

            if (deleteBtn) {
                const lessonId = Number(deleteBtn.getAttribute('data-delete'));
                Modal.confirm('Удалить урок?', 'Порядок остальных уроков будет пересчитан автоматически.', async () => {
                    try {
                        await Api.delete(`/courses/${course.id}/lessons/${lessonId}`);
                        Toast.show('Урок удалён');
                        await this.render(this.params);
                    } catch (error) {
                        Toast.show(error.detail || 'Не удалось удалить урок', 'error');
                    }
                });
            }
        };
    },

    // lesson === null → создание; иначе редактирование
    openLessonModal(course, lesson) {
        const lessons = this.lessons || [];
        const isEdit = !!lesson;
        const last = lessons[lessons.length - 1];

        const anchorOptions = lessons.map((l) =>
            `<option value="${l.id}" ${!isEdit && l.id === (last && last.id) ? 'selected' : ''}>
                После урока ${l.order}. ${esc(l.title)}
            </option>`).join('');

        const overlay = Modal.open(`
            <h3 class="text-lg font-semibold text-gray-900 mb-4">${isEdit ? 'Редактировать урок' : 'Новый урок'}</h3>
            <form id="lesson-form">
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Название</label>
                    <input name="title" class="input" maxlength="255" required value="${isEdit ? esc(lesson.title) : ''}" />
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Содержание</label>
                    <textarea name="content" class="input" style="min-height:140px" required>${isEdit ? esc(lesson.content) : ''}</textarea>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Ссылка на видео (необязательно)</label>
                    <input name="video_url" type="url" class="input" placeholder="https://youtube.com/watch?v=..." value="${isEdit && lesson.video_url ? esc(lesson.video_url) : ''}" />
                </div>
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Длительность, мин (необязательно)</label>
                    <input name="duration_minutes" type="number" min="0" class="input" value="${isEdit && lesson.duration_minutes ? lesson.duration_minutes : ''}" />
                </div>
                ${!isEdit ? `
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Позиция в программе</label>
                        <select name="after_lesson_id" class="input">${anchorOptions}</select>
                    </div>
                ` : ''}
                <div class="flex justify-end gap-3">
                    <button type="button" class="btn btn-secondary" data-cancel>Отмена</button>
                    <button type="submit" class="btn btn-primary">${isEdit ? 'Сохранить' : 'Добавить'}</button>
                </div>
            </form>`);

        overlay.querySelector('[data-cancel]').onclick = () => overlay.remove();

        overlay.querySelector('#lesson-form').onsubmit = async (e) => {
            e.preventDefault();
            const form = e.target;
            const button = form.querySelector('button[type=submit]');
            button.disabled = true;

            const durationRaw = form.duration_minutes.value.trim();

            try {
                if (isEdit) {
                    // PATCH частичный: шлём только заполненные поля
                    const payload = {
                        title: form.title.value.trim(),
                        content: form.content.value.trim(),
                    };
                    if (form.video_url.value.trim()) payload.video_url = form.video_url.value.trim();
                    if (durationRaw !== '') payload.duration_minutes = Number(durationRaw);

                    await Api.patch(`/courses/${course.id}/lessons/${lesson.id}`, payload);
                    Toast.show('Урок обновлён');
                } else {
                    await Api.post(`/courses/${course.id}/lessons`, {
                        title: form.title.value.trim(),
                        content: form.content.value.trim(),
                        video_url: form.video_url.value.trim() || null,
                        after_lesson_id: Number(form.after_lesson_id.value),
                    });
                    Toast.show('Урок добавлен, порядок пересчитан');
                }
                overlay.remove();
                await this.render(this.params);
            } catch (error) {
                Toast.show(error.detail || 'Не удалось сохранить урок', 'error');
                button.disabled = false;
            }
        };
    },
};