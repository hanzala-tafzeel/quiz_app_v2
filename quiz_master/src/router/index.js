import { createRouter, createWebHistory } from 'vue-router'
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
  {
    path: '/user',
    name: 'user',
    component: UserPage
  },
  {
    path: '/user/quizzes',
    name: 'BrowseContent',
    component: BrowseQuiz,
  },
  {
    path: '/user/profile',
    name: 'userProfile',
    component: UserProfile
  },
  {
    path: '/user/summary',
    name: 'userSummary',
    component: UserSummary
  },
  {
    path: '/user/quiz/:quizId',
    name: 'quizPage',
    component: QuizPage,
    props: true
  },
  {
    path: '/user/quiz/:attemptId/score',
    name: 'quizScore',
    component: ScorePage,
    props: true
  },
  {
    path: '/user/profile/history',
    name: 'userHistory',
    component: QuizHistory,
  },

  // Admin routes
  {
    path: '/admin',
    name: 'admin',
    component: AdminPage,
  },
  {
    path: '/quizmanagement',
    name: 'quizmanagement',
    component: QuizManagement
  },
  {
    path: '/summary',
    name: 'adminsummary',
    component: AdminSummary
  },
  {
    path: '/adminuserpage',
    name: 'AdminUserPage',
    component: ProfilePage
  }


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
