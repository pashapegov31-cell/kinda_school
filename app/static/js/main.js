(async function bootstrap() {
    // если токен есть — подтягиваем профиль до первого рендера,
    // чтобы navbar и ролевые_guard'ы знали роль сразу
    await Auth.loadUser();
    Router.init();
})();