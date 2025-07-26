import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    token: null,
    userRole: null,
    isAuthenticated: false,
    quizzes: [],
    subjects: [] ,
    chapters: [],
    BASE_URL: 'http://127.0.1:5000/api'
  },
  mutations: {
    SET_LOGIN_DATA(state, payload) {
      state.user = payload.user;
      state.token = payload.token;
      state.userRole = payload.userRole;
      state.isAuthenticated = true;
    },
    CLEAR_LOGIN_DATA(state) {
      state.user = null;
      state.token = null;
      state.userRole = null;
      state.isAuthenticated = false;
    },

    
    SET_SUBJECTS(state, payload) {
      state.subjects = payload;
    },
    
    SET_CHAPTERS(state, payload) {
      state.chapters = payload;
    },
    
    SET_QUIZZES(state, quizzes) {
      state.quizzes = quizzes;
    },

    
  },
  getters: {
    isLoggedIn: state => state.isAuthenticated,
    getCurrentUser: state => state.user,
    getUserRole: state => state.userRole,
    getToken: state => state.token,
    getQuizzes: state => state.quizzes,

    // Optional: get all subjects
    getSubjects: state => state.subjects,
    getChapters: state => state.chapters,

    // Optional: get all chapters as a flat array
    // allChapters(state) {
    //   return state.subjects.flatMap(subject => subject.chapters || []);
    // }
  },
  actions: {

    loadAuthFromStorage({ commit }) {
      const token = sessionStorage.getItem('token')
      const user = sessionStorage.getItem('user')
      const userRole = sessionStorage.getItem('userRole') // Add this line
      
      if (token && user && userRole) { // Check userRole too
        try {
          const parsedUser = JSON.parse(user)
          commit('SET_LOGIN_DATA', { 
            user: parsedUser, 
            token: token,
            userRole: userRole // Add this line
          })
        } catch (error) {
          console.error('Error parsing user data from storage:', error)
          sessionStorage.removeItem('token')
          sessionStorage.removeItem('user')
          sessionStorage.removeItem('userRole') // Clear this too
        }
      }
    },
    logout({ commit }) {
      // Clear the store state
      commit('CLEAR_LOGIN_DATA')
      
      // Clear sessionStorage
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('user')
      sessionStorage.removeItem('userRole')
      sessionStorage.removeItem('isAuthenticated')
      
      // Or clear all sessionStorage
      // sessionStorage.clear()
    }
    
  }
})
