const API_BASE = '/v1';

class ApiError extends Error {
    constructor(status, detail) {
        super(detail);
        this.status = status;
        this.detail = detail;
    }
}

async function apiRequest(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
    };

    const token = Auth.getToken();
    if (token) {
        headers['Authorization'] = 'Bearer ' + token;
    }

    let response;
    try {
        response = await fetch(API_BASE + endpoint, { ...options, headers });
    } catch (e) {
        throw new ApiError(0, 'Ошибка сети. Сервер недоступен.');
    }

    if (response.status === 204) return null;

    const text = await response.text();
    let data = null;
    try { data = text ? JSON.parse(text) : null; } catch (e) { data = null; }

    if (!response.ok) {
        // протухшая сессия: чистим и уходим на логин (кроме самих login/register)
        if (response.status === 401 && Auth.getToken() &&
            endpoint !== '/login' && endpoint !== '/register') {
            Auth.clear();
            if (window.Router && Router.ready) Router.navigate('/login', true);
        }
        const detail = (data && data.detail) || ('Ошибка сервера: ' + response.status);
        throw new ApiError(response.status, detail);
    }

    return data;
}

const Api = {
    get: (endpoint) => apiRequest(endpoint, { method: 'GET' }),
    post: (endpoint, body) => apiRequest(endpoint, { method: 'POST', body: JSON.stringify(body) }),
    patch: (endpoint, body) => apiRequest(endpoint, { method: 'PATCH', body: JSON.stringify(body || {}) }),
    delete: (endpoint) => apiRequest(endpoint, { method: 'DELETE' }),
};