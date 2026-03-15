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
                            background: '#FFFFFF',
                            primary: '#0097A7',
                            secondary: '#00BCD4',
                            accent: '#9575CD',
                            success: '#66BB6A',
                            info: '#2196F3',
                            warning: '#FF9800',
                            error: '#E86674',
                            orange: '#E65100',
                            golden: '#A68C59',
                            badge: '#F5528C',
                            customPrimary: '#085294',
                        },
                    },
                },
            },
            defaults: {
                VTextField: {
                    density: 'compact',
                    variant: 'outlined',
                    hideDetails: true,
                },
                VSelect: {
                    density: 'compact',
                    variant: 'outlined',
                    hideDetails: true,
                },
                VAutocomplete: {
                    density: 'compact',
                    variant: 'outlined',
                    hideDetails: true,
                },
                VTextarea: {
                    density: 'compact',
                    variant: 'outlined',
                    hideDetails: true,
                },
                VCheckbox: {
                    density: 'compact',
                    hideDetails: true,
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
