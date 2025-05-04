import { fetchMostBoughtProducts } from '../api/index';

const state = {
  mostBoughtProducts: [],
};

const getters = {
  mostBoughtProducts: (state) => state.mostBoughtProducts,
};

const actions = {
  async loadMostBoughtProducts({ commit }) {
    try {
      const response = await fetchMostBoughtProducts();
      commit('setMostBoughtProducts', response.data);
    } catch (error) {
      console.error('Failed to load most bought products:', error);
    }
  },
};

const mutations = {
  setMostBoughtProducts(state, products) {
    state.mostBoughtProducts = products;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
