import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView from '../views/HomeView.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import UserPage from '../views/user/UserPage.vue'
import UserProfile from '../views/user/UserProfile.vue'
import UserSummary from '../views/user/UserSummary.vue'
import QuizPage from '../views/user/QuizPage.vue'
import ScorePage from '../views/user/ScorePage.vue'
import QuizHistory from '../views/user/QuizHistory.vue'
import BrowseQuiz from '../views/user/BrowseQuiz.vue'


// Admin components
import AdminPage from '../views/admin/AdminPage.vue'
import AdminSummary from '../views/admin/AdminSummary.vue'
import QuizManagement from '../views/admin/QuizManagement.vue'
import ProfilePage from '../views/admin/ProfilePage.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },

  /* ------------------------------ User routes ------------------------------ */
  {
    path: '/user',
    name: 'user',
    component: UserPage,
    meta: {
      requiresAuth: true,
      roles: ['user']
    }
  },
  {
    path: '/user/quizzes',
    name: 'BrowseContent',
    component: BrowseQuiz,
    meta: {
      requiresAuth: true,
      roles: ['user']
    }
  },
  {
    path: '/user/profile',
    name: 'userProfile',
    component: UserProfile,
    meta: {
      requiresAuth: true,
      roles: ['user']
    }
  },
  {
    path: '/user/summary',
    name: 'userSummary',
    component: UserSummary,
    meta: {
      requiresAuth: true,
      roles: ['user']
    }
  },
  {
    path: '/user/quiz/:quizId',
    name: 'quizPage',
    component: QuizPage,
    meta: {
      requiresAuth: true,
      roles: ['user']
    },
    props: true
  },
  {
    path: '/user/quiz/:attemptId/score',
    name: 'quizScore',
    component: ScorePage,
    meta: {
      requiresAuth: true,
      roles: ['user']
    },
    props: true
  },
  {
    path: '/user/profile/history',
    name: 'userHistory',
    component: QuizHistory,
    meta: {
      requiresAuth: true,
      roles: ['user']
    }
  },

  /* ------------------------------ Admin routes ------------------------------ */
  {
    path: '/admin',
    name: 'admin',
    component: AdminPage,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/quizmanagement',
    name: 'quizmanagement',
    component: QuizManagement,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    } 
  },
  {
    path: '/summary',
    name: 'adminsummary',
    component: AdminSummary,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/adminuserpage',
    name: 'AdminUserPage',
    component: ProfilePage,
    meta: {
      requiresAuth: true,
      roles: ['admin']
    }
  }


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


// Router Guards using Vuex
router.beforeEach((to, from, next) => {
  // Load auth from storage if not already loaded
  // if (!store.state.isAuthenticated) {
  //   store.dispatch('loadAuthFromStorage')
  // }


  const isAuthenticated = store.state.isAuthenticated
  const userRole = store.getters.getUserRole

  // Check if route requires guest (not logged in)
  if (to.meta.requiresGuest && isAuthenticated) {
    if (userRole === 'admin') {
      return next('/admin')
    } else {
      return next('/user')
    }
  }

    // Check if route requires authentication
    if (to.meta.requiresAuth && !isAuthenticated) {
      return next('/login')
    }

  
  // Check role-based access
  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    if (userRole === 'admin') {
      return next('/admin')
    } else if (userRole === 'user' || userRole === 'student') {
      return next('/user')
    } else {
      return next('/login')
    }
  }

  next()
})


export default router
