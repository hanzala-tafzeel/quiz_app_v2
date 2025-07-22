import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    token: null,
    userRole: null,
    isAuthenticated: false,
    quizzes: [],
    subjects: [] ,
    chapters: []
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
  actions: {}
})
