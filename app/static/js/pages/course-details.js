const CourseDetailsPage = {
    async render(params) {
        const content = document.getElementById('content');

        let course;
        try {
            course = await Api.get(`/courses/${params.id}`);
        } catch (error) {
            content.innerHTML = emptyState(
                'Курс не найден или был удалён.',
                '<a href="/courses" data-link class="btn btn-primary">Вернуться в каталог</a>'
            );
            return;
        }

        const user = Auth.getUser();
        const isOwner = !!user && user.id === course.teacher_id;
        const canManage = isOwner || Auth.isAdmin();

        // запись студента на этот курс (если он студент)
        let enrollment = null;
        if (user && user.role === 'student') {
            try {
                const mine = await Api.get('/enrollments/me');
                enrollment = mine.find((e) => e.course_id === course.id) || null;
            } catch (e) { /* не критично */ }
        }

        // уроки: доступны залогиненным; у draft для посторонних будет 404
        let lessons = [];
        let lessonsBlocked = false;
        if (Auth.isLoggedIn()) {
            try {
                lessons = await Api.get(`/courses/${course.id}/lessons?limit=100`);
            } catch (e) {
                lessonsBlocked = true;
            }
        } else {
            lessonsBlocked = true;
        }

        const canOpenLessons = canManage || !!enrollment;

        content.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <a href="/courses" data-link class="text-indigo-600 hover:underline text-sm mb-6 inline-block">← В каталог</a>

                <div class="card mb-6">
                    <div class="flex flex-wrap justify-between items-start gap-3 mb-4">
                        <h1 class="text-3xl font-bold text-gray-900">${esc(course.title)}</h1>
                        ${statusBadge(course.status)}
                    </div>
                    <p class="text-gray-700 leading-relaxed mb-6">${esc(course.description)}</p>
                    <div class="flex flex-wrap justify-between items-center gap-4 pt-4 border-t border-gray-100">
                        <span class="text-3xl font-bold text-indigo-600">${fmtPrice(course.price)}</span>
                        <div class="flex gap-3">
                            ${canManage ? `
                                <a href="/dashboard/courses/${course.id}" data-link class="btn btn-secondary">Управлять курсом</a>
                            ` : ''}
                            ${user && user.role === 'student' && course.status === 'published' ? `
                                ${enrollment ? `
                                    <button class="btn btn-secondary" disabled>Вы записаны</button>
                                ` : `
                                    <button id="enroll-btn" class="btn btn-primary">Записаться на курс</button>
                                `}
                            ` : ''}
                        </div>
                    </div>
                </div>

                <h2 class="text-xl font-bold text-gray-900 mb-4">Программа курса</h2>
                <div id="lessons-block"></div>
            </div>`;

        const block = document.getElementById('lessons-block');

        if (lessonsBlocked && !canManage) {
            block.innerHTML = emptyState(
                Auth.isLoggedIn()
                    ? 'Уроки скрыты до публикации курса.'
                    : 'Войдите, чтобы увидеть программу курса.'
            );
        } else if (!lessons.length) {
            block.innerHTML = emptyState('В курсе пока нет уроков.');
        } else {
            block.innerHTML = lessons.map((lesson) => `
                ${canOpenLessons ? `
                    <a href="/courses/${course.id}/lessons/${lesson.id}" data-link
                       class="card mb-3 flex items-center gap-4 hover:shadow-md transition">
                        <div class="w-10 h-10 shrink-0 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-semibold">${lesson.order}</div>
                        <div class="flex-1 min-w-0">
                            <h4 class="font-medium text-gray-900 truncate">${esc(lesson.title)}</h4>
                            <p class="text-sm text-gray-500">${lesson.duration_minutes ? lesson.duration_minutes + ' мин' : 'длительность не указана'}</p>
                        </div>
                        <span class="text-gray-400">→</span>
                    </a>
                ` : `
                    <div class="card mb-3 flex items-center gap-4 opacity-70">
                        <div class="w-10 h-10 shrink-0 rounded-full bg-gray-100 text-gray-500 flex items-center justify-center font-semibold">${lesson.order}</div>
                        <div class="flex-1 min-w-0">
                            <h4 class="font-medium text-gray-700 truncate">${esc(lesson.title)}</h4>
                            <p class="text-sm text-gray-500">${lesson.duration_minutes ? lesson.duration_minutes + ' мин' : 'длительность не указана'}</p>
                        </div>
                        <span title="Доступно после записи" class="text-gray-400">🔒</span>
                    </div>
                `}
            `).join('');
        }

        const enrollBtn = document.getElementById('enroll-btn');
        if (enrollBtn) {
            enrollBtn.onclick = async () => {
                enrollBtn.disabled = true;
                try {
                    await Api.post(`/courses/${course.id}/enroll`);
                    Toast.show('Вы записаны на курс!');
                    await this.render(params);
                } catch (error) {
                    Toast.show(error.detail || 'Не удалось записаться', 'error');
                    enrollBtn.disabled = false;
                }
            };
        }
    },
};