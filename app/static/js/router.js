const Router = {
    params: {},
    ready: false,

    routes: [
        { pattern: '/login', page: () => LoginPage, guestOnly: true },
        { pattern: '/register', page: () => RegisterPage, guestOnly: true },
        { pattern: '/', page: () => CatalogPage },
        { pattern: '/courses', page: () => CatalogPage },
        { pattern: '/courses/:id', page: () => CourseDetailsPage },
        { pattern: '/my-courses', page: () => MyCoursesPage, auth: true, roles: ['student'] },
        { pattern: '/courses/:cid/lessons/:lid', page: () => LessonPage, auth: true },
        { pattern: '/dashboard', page: () => DashboardPage, auth: true, roles: ['teacher', 'admin'] },
        { pattern: '/dashboard/courses/:id', page: () => CourseEditPage, auth: true, roles: ['teacher', 'admin'] },
        { pattern: '/admin', page: () => AdminPage, auth: true, roles: ['admin'] },
    ],

    navigate(path, replace = false) {
        if (replace) history.replaceState(null, '', path);
        else history.pushState(null, '', path);
        this.handleRoute();
    },

    matchRoute(pattern, path) {
        const pp = pattern.split('/');
        const cp = path.split('/');
        if (pp.length !== cp.length) return null;
        const params = {};
        for (let i = 0; i < pp.length; i++) {
            if (pp[i].startsWith(':')) params[pp[i].slice(1)] = decodeURIComponent(cp[i]);
            else if (pp[i] !== cp[i]) return null;
        }
        return params;
    },

    async handleRoute() {
        const path = window.location.pathname;

        for (const route of this.routes) {
            const params = this.matchRoute(route.pattern, path);
            if (!params) continue;

            if (route.guestOnly && Auth.isLoggedIn()) {
                this.navigate('/courses', true);
                return;
            }

            if (route.auth && !Auth.isLoggedIn()) {
                this.navigate('/login', true);
                return;
            }

            if (route.auth && route.roles) {
                const role = Auth.role();
                if (!route.roles.includes(role)) {
                    Toast.show('Раздел недоступен для вашей роли', 'error');
                    this.navigate('/', true);
                    return;
                }
            }

            this.params = params;
            const content = document.getElementById('content');
            content.innerHTML = '<div class="text-center py-20 text-gray-400">Загрузка…</div>';

            try {
                await route.page().render(params);
            } catch (error) {
                console.error(error);
                if (error instanceof ApiError) Toast.show(error.detail, 'error');
            }

            NavBar.render();
            window.scrollTo(0, 0);
            this.ready = true;
            return;
        }

        document.getElementById('content').innerHTML = `
            <div class="text-center py-24">
                <h1 class="text-5xl font-bold text-gray-900 mb-4">404</h1>
                <p class="text-gray-500 mb-8">Такой страницы нет</p>
                <a href="/courses" data-link class="btn btn-primary">В каталог</a>
            </div>`;
        NavBar.render();
        this.ready = true;
    },

    init() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[data-link]');
            if (!link) return;
            e.preventDefault();
            this.navigate(link.getAttribute('href'));
        });

        window.addEventListener('popstate', () => this.handleRoute());
        this.handleRoute();
    },
};