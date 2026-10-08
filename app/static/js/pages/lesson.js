const LessonPage = {
    // youtube watch/youtu.be → embed-адрес; для прочих url вернёт null
    youtubeEmbed(url) {
        if (!url) return null;
        const m = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([\w-]{11})/);
        return m ? 'https://www.youtube.com/embed/' + m[1] : null;
    },

    async render(params) {
        const content = document.getElementById('content');
        const { cid, lid } = params;

        let lesson;
        try {
            lesson = await Api.get(`/courses/${cid}/lessons/${lid}`);
        } catch (error) {
            if (error.status === 403) {
                content.innerHTML = emptyState(
                    'Урок доступен только записанным на курс студентам.',
                    `<a href="/courses/${cid}" data-link class="btn btn-primary">К странице курса</a>`
                );
            } else {
                content.innerHTML = emptyState(
                    'Урок не найден.',
                    `<a href="/courses/${cid}" data-link class="btn btn-primary">К странице курса</a>`
                );
            }
            return;
        }

        // соседние уроки для навигации
        let lessons = [];
        try {
            lessons = await Api.get(`/courses/${cid}/lessons?limit=100`);
        } catch (e) { /* навигация не критична */ }
        const idx = lessons.findIndex((l) => l.id === lesson.id);
        const prev = idx > 0 ? lessons[idx - 1] : null;
        const next = idx >= 0 && idx < lessons.length - 1 ? lessons[idx + 1] : null;

        const embed = this.youtubeEmbed(lesson.video_url);

        content.innerHTML = `
            <div class="max-w-3xl mx-auto">
                <a href="/courses/${cid}" data-link class="text-indigo-600 hover:underline text-sm mb-6 inline-block">← К курсу</a>

                <div class="card mb-6">
                    <div class="flex items-center gap-3 mb-3">
                        <span class="badge badge-draft">Урок ${lesson.order}</span>
                        ${lesson.duration_minutes ? `<span class="text-sm text-gray-500">${lesson.duration_minutes} мин</span>` : ''}
                    </div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-6">${esc(lesson.title)}</h1>

                    ${embed ? `
                        <div class="mb-6 aspect-video rounded-lg overflow-hidden bg-gray-900">
                            <iframe class="w-full h-full" src="${embed}" title="Видео урока"
                                    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                    allowfullscreen></iframe>
                        </div>
                    ` : lesson.video_url ? `
                        <a href="${esc(lesson.video_url)}" target="_blank" rel="noopener" class="btn btn-secondary mb-6">▶ Смотреть видео</a>
                    ` : ''}

                    <div class="lesson-content text-gray-700">${esc(lesson.content)}</div>

                    <div class="mt-8 pt-6 border-t border-gray-100 flex flex-wrap justify-between items-center gap-4">
                        <button id="mark-btn" class="btn btn-primary">Отметить пройденным</button>
                        <div class="flex gap-3">
                            ${prev ? `<a href="/courses/${cid}/lessons/${prev.id}" data-link class="btn btn-secondary">← ${esc(prev.title)}</a>` : ''}
                            ${next ? `<a href="/courses/${cid}/lessons/${next.id}" data-link class="btn btn-secondary">${esc(next.title)} →</a>` : ''}
                        </div>
                    </div>
                </div>
            </div>`;

        document.getElementById('mark-btn').onclick = async (e) => {
            const btn = e.target;
            btn.disabled = true;
            try {
                await Api.post(`/courses/${cid}/lessons/${lid}/lesson_progress`);
                Toast.show('Урок отмечен пройденным 🎉');
                btn.textContent = 'Пройдено ✓';
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-secondary');
            } catch (error) {
                Toast.show(error.detail || 'Не удалось отметить урок', 'error');
                btn.disabled = false;
            }
        };
    },
};