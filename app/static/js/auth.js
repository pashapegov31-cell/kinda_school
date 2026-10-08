const Auth = {
    TOKEN_KEY: 'ks_token',
    USER_KEY: 'ks_user',
    user: null,

    setToken(token) { localStorage.setItem(this.TOKEN_KEY, token); },
    getToken() { return localStorage.getItem(this.TOKEN_KEY); },

    setUser(user) {
        this.user = user;
        localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    },

    getUser() {
        if (this.user) return this.user;
        const raw = localStorage.getItem(this.USER_KEY);
        if (!raw) return null;
        try { this.user = JSON.parse(raw); return this.user; }
        catch (e) { return null; }
    },

    isLoggedIn() { return !!this.getToken(); },

    clear() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_KEY);
        this.user = null;
    },

    logout() {
        this.clear();
        Router.navigate('/login');
    },

    async login(email, password) {
        const r = await Api.post('/login', { email, password });
        this.setToken(r.access_token);
        try {
            const user = await Api.get('/me');
            this.setUser(user);
            return user;
        } catch (e) {
            this.clear();
            throw e;
        }
    },

    async register(email, name, password) {
        const r = await Api.post('/register', { email, name, password });
        this.setToken(r.access_token);
        try {
            const user = await Api.get('/me');
            this.setUser(user);
            return user;
        } catch (e) {
            this.clear();
            throw e;
        }
    },

    // тихо подтянуть профиль при старте; без редиректов
    async loadUser() {
        if (!this.getToken()) return null;
        try {
            const user = await Api.get('/me');
            this.setUser(user);
            return user;
        } catch (e) {
            this.clear();
            return null;
        }
    },

    role() {
        const u = this.getUser();
        return u ? u.role : null;
    },
    isStudent() { return this.role() === 'student'; },
    isTeacher() { return this.role() === 'teacher'; },
    isAdmin() { return this.role() === 'admin'; },
};