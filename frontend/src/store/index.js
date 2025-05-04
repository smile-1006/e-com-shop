import { createStore } from 'vuex';
import mostBoughtProducts from './mostBoughtProducts';

export default createStore({
  modules: {
    mostBoughtProducts,
  },
});
