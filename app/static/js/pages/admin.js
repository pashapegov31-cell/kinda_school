const AdminPage = {
    async render() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div>
                <h1 class="text-3xl font-bold text-gray-900 mb-2">Пользователи</h1>
                <p class="text-gray-500 mb-8">Управление ролями платформы</p>
                <div class="card overflow-x-auto" style="padding:0">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-gray-50 text-gray-500">
                            <tr>
                                <th class="px-4 py-3 font-medium">ID</th>
                                <th class="px-4 py-3 font-medium">Имя</th>
                                <th class="px-4 py-3 font-medium">Email</th>
                                <th class="px-4 py-3 font-medium">Роль</th>
                                <th class="px-4 py-3 font-medium text-right">Действия</th>
                            </tr>
                        </thead>
                        <tbody id="users-tbody"></tbody>
                    </table>
                </div>
            </div>`;

        await this.load();
    },

    roleBadge(role) {
        const map = { admin: 'badge-archived', teacher: 'badge-published', student: 'badge-draft' };
        return `<span class="badge ${map[role] || 'badge-draft'}">${esc(role)}</span>`;
    },

    async load() {
        const tbody = document.getElementById('users-tbody');
        try {
            const users = await Api.get('/users?limit=100');
            const me = Auth.getUser();

            tbody.innerHTML = users.map((u) => `
                <tr class="border-t border-gray-100">
                    <td class="px-4 py-3 text-gray-400">#${u.id}</td>
                    <td class="px-4 py-3 font-medium text-gray-900">
                        ${esc(u.name)}${u.id === me.id ? ' <span class="text-xs text-gray-400">(это вы)</span>' : ''}
                    </td>
                    <td class="px-4 py-3 text-gray-600">${esc(u.email)}</td>
                    <td class="px-4 py-3">${this.roleBadge(u.role)}</td>
                    <td class="px-4 py-3 text-right">
                        ${u.id === me.id
                    ? '<span class="text-xs text-gray-400">—</span>'
                    : `<button class="btn btn-secondary text-xs" data-role="${u.id}" data-name="${esc(u.name)}">Сменить роль</button>`}
                    </td>
                </tr>`).join('');

            tbody.onclick = (e) => {
                const btn = e.target.closest('[data-role]');
                if (!btn) return;
                this.openRoleModal(Number(btn.getAttribute('data-role')), btn.getAttribute('data-name'));
            };
        } catch (error) {
            tbody.innerHTML = `<tr><td colspan="5" class="px-4 py-8 text-center text-gray-500">${esc(error.detail || 'Ошибка загрузки')}</td></tr>`;
        }
    },

    openRoleModal(userId, userName) {
        const overlay = Modal.open(`
            <h3 class="text-lg font-semibold text-gray-900 mb-1">Смена роли</h3>
            <p class="text-sm text-gray-500 mb-4">Пользователь: ${esc(userName)} (#${userId})</p>
            <form id="role-form">
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Новая роль</label>
                    <select name="role" class="input">
                        <option value="student">student — студент</option>
                        <option value="teacher">teacher — преподаватель</option>
                        <option value="admin">admin — администратор</option>
                    </select>
                </div>
                <div class="flex justify-end gap-3">
                    <button type="button" class="btn btn-secondary" data-cancel>Отмена</button>
                    <button type="submit" class="btn btn-primary">Сохранить</button>
                </div>
            </form>`);

        overlay.querySelector('[data-cancel]').onclick = () => overlay.remove();

        overlay.querySelector('#role-form').onsubmit = async (e) => {
            e.preventDefault();
            const role = e.target.role.value;
            try {
                await Api.post('/change/role', { user_id: userId, new_role: role });
                overlay.remove();
                Toast.show('Роль обновлена');
                await this.load();
            } catch (error) {
                Toast.show(error.detail || 'Не удалось сменить роль', 'error');
            }
        };
    },
};