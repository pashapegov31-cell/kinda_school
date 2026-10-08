function esc(value) {
    if (value === null || value === undefined) return '';
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function fmtPrice(price) {
    return Number(price).toLocaleString('ru-RU', { minimumFractionDigits: 0, maximumFractionDigits: 2 }) + ' ₽';
}

function fmtDate(iso) {
    if (!iso) return '—';
    return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
}

function statusBadge(status) {
    const map = {
        draft: ['badge-draft', 'Черновик'],
        published: ['badge-published', 'Опубликован'],
        archived: ['badge-archived', 'Архив'],
    };
    const [cls, label] = map[status] || ['badge-draft', status];
    return `<span class="badge ${cls}">${label}</span>`;
}

function progressBar(percent) {
    const p = Math.max(0, Math.min(100, Math.round(percent)));
    return `
        <div class="flex items-center gap-3">
            <div class="progress-track flex-1"><div class="progress-fill" style="width:${p}%"></div></div>
            <span class="text-sm text-gray-500 w-10 text-right">${p}%</span>
        </div>`;
}

function emptyState(text, actionHtml = '') {
    return `
        <div class="card text-center py-16">
            <p class="text-gray-500 mb-4">${esc(text)}</p>
            ${actionHtml}
        </div>`;
}

const Toast = {
    show(message, type = 'success') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        toast.className = 'toast toast-' + type;
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    },
};

const NavBar = {
    render() {
        const navbar = document.getElementById('navbar');
        const user = Auth.getUser();

        if (!Auth.isLoggedIn() || !user) {
            navbar.className = 'bg-white border-b border-gray-200';
            navbar.innerHTML = `
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between items-center h-16">
                        <a href="/courses" data-link class="text-xl font-bold text-indigo-600">Kinda School</a>
                        <div class="flex items-center gap-3">
                            <a href="/courses" data-link class="text-gray-600 hover:text-gray-900">Каталог</a>
                            <a href="/login" data-link class="btn btn-secondary">Войти</a>
                            <a href="/register" data-link class="btn btn-primary">Регистрация</a>
                        </div>
                    </div>
                </div>`;
            return;
        }

        const links = [{ href: '/courses', label: 'Каталог' }];
        if (user.role === 'student') links.push({ href: '/my-courses', label: 'Мои курсы' });
        if (user.role === 'teacher' || user.role === 'admin') links.push({ href: '/dashboard', label: 'Мои курсы' });
        if (user.role === 'admin') links.push({ href: '/admin', label: 'Пользователи' });

        navbar.className = 'bg-white border-b border-gray-200';
        navbar.innerHTML = `
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center h-16 gap-4">
                    <div class="flex items-center gap-6 min-w-0">
                        <a href="/courses" data-link class="text-xl font-bold text-indigo-600 whitespace-nowrap">Kinda School</a>
                        <nav class="flex gap-5 overflow-x-auto">
                            ${links.map(l => `
                                <a href="${l.href}" data-link
                                   class="whitespace-nowrap ${window.location.pathname === l.href || window.location.pathname.startsWith(l.href + '/') ? 'text-indigo-600 font-medium' : 'text-gray-600 hover:text-gray-900'} transition">
                                    ${l.label}
                                </a>`).join('')}
                        </nav>
                    </div>
                    <div class="flex items-center gap-3 shrink-0">
                        <span class="text-sm text-gray-600 hidden sm:inline">
                            ${esc(user.name)} <span class="text-xs text-gray-400">· ${esc(user.role)}</span>
                        </span>
                        <button class="btn btn-secondary text-sm" onclick="Auth.logout()">Выйти</button>
                    </div>
                </div>
            </div>`;
    },
};

const Modal = {
    confirm(title, message, onConfirm, confirmLabel = 'Удалить') {
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.innerHTML = `
            <div class="modal" style="max-width:440px">
                <h3 class="text-lg font-semibold text-gray-900 mb-2">${esc(title)}</h3>
                <p class="text-gray-600 mb-6">${esc(message)}</p>
                <div class="flex gap-3 justify-end">
                    <button class="btn btn-secondary" data-cancel>Отмена</button>
                    <button class="btn btn-danger" data-confirm>${esc(confirmLabel)}</button>
                </div>
            </div>`;
        document.body.appendChild(overlay);

        overlay.querySelector('[data-cancel]').onclick = () => overlay.remove();
        overlay.querySelector('[data-confirm]').onclick = () => { overlay.remove(); onConfirm(); };
        overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
    },

    open(html, maxWidth = '560px') {
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.innerHTML = `<div class="modal" style="max-width:${maxWidth}">${html}</div>`;
        document.body.appendChild(overlay);
        overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
        return overlay;
    },
};

function CourseCard(course) {
    return `
        <a href="/courses/${course.id}" data-link class="card block hover:shadow-lg transition">
            <div class="flex justify-between items-start mb-3 gap-2">
                <h3 class="text-lg font-semibold text-gray-900">${esc(course.title)}</h3>
                ${statusBadge(course.status)}
            </div>
            <p class="text-gray-600 text-sm mb-6 line-clamp-3">${esc(course.description)}</p>
            <div class="flex justify-between items-center">
                <span class="text-xl font-bold text-indigo-600">${fmtPrice(course.price)}</span>
                <span class="text-xs text-gray-400">${fmtDate(course.created_at)}</span>
            </div>
        </a>`;
}