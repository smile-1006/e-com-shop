import { createApp } from 'vue';
import App from './App.vue';
import { fetchProducts } from './firstpage';

createApp({
    components: { App },
    data() {
        return {
            products: []
        };
    },
    async created() {
        this.products = await fetchProducts();
    }
}).mount('#app');
