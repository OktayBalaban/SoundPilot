import { init, register, getLocaleFromNavigator } from 'svelte-i18n';

register('en', () => import('./locales/en.json'));
register('tr', () => import('./locales/tr.json'));

init({
    fallbackLocale: 'en',
    initialLocale: getLocaleFromNavigator() || 'en',
});