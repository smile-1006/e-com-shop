const state = () => ({
  mobile: null,
  full_name: null,
  isAuthenticated: false,
});

const getters = {
  isAuthenticated: (state) => state.isAuthenticated,
  mobile: (state) => state.mobile,
  full_name: (state) => state.full_name,
};

const mutations = {
  setUser(state, user) {
    state.mobile = user.mobile;
    state.full_name = user.full_name;
    state.isAuthenticated = true;
  },
  clearUser(state) {
    state.mobile = null;
    state.full_name = null;
    state.isAuthenticated = false;
  },
};

const actions = {
  login({ commit }, user) {
    commit('setUser', user);
  },
  logout({ commit }) {
    commit('clearUser');
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
