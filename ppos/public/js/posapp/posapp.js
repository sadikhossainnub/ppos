import { createApp, h } from 'vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
// import 'vuetify/styles';
// import '@mdi/font/css/materialdesignicons.css';
import Home from './Home.vue';

frappe.provide('frappe.PosApp');

frappe.PosApp.posapp = class {
    constructor({ parent }) {
        this.$parent = $(document);
        this.page = parent.page;
        this.make_body();
    }
    make_body() {
        this.$el = this.$parent.find('.main-section');

        const vuetify = createVuetify({
            components,
            directives,
            theme: {
                defaultTheme: 'light',
                themes: {
                    light: {
                        colors: {
                            background: '#F8F9FA',
                            surface: '#FFFFFF',
                            primary: '#1A1A1A', // Modern deep black for primary actions
                            secondary: '#607D8B',
                            accent: '#2196F3',
                            success: '#4CAF50',
                            info: '#2196F3',
                            warning: '#FB8C00',
                            error: '#FF5252',
                        },
                    },
                },
            },
            defaults: {
                VCard: {
                    elevation: 0,
                    rounded: 'lg',
                    border: true,
                },
                VBtn: {
                    rounded: 'lg',
                    elevation: 0,
                    textTransform: 'none',
                    fontWeight: '600',
                },
                VTextField: {
                    density: 'compact',
                    variant: 'outlined',
                    rounded: 'lg',
                    bgColor: '#F1F3F4',
                    hideDetails: 'auto',
                },
                VSelect: {
                    density: 'compact',
                    variant: 'outlined',
                    rounded: 'lg',
                    bgColor: '#F1F3F4',
                    hideDetails: 'auto',
                },
                VAutocomplete: {
                    density: 'compact',
                    variant: 'outlined',
                    rounded: 'lg',
                    bgColor: '#F1F3F4',
                    hideDetails: 'auto',
                },
            },
        });

        const app = createApp({
            render: () => h(Home),
        });
        app.use(vuetify);
        app.config.globalProperties.__ = window.__;
        app.config.globalProperties.frappe = window.frappe;
        app.mount(this.$el[0]);
    }
    setup_header() {}
};
