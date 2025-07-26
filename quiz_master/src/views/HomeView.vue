<template>
  <div class="landing-page">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container">
        <router-link class="navbar-brand fw-bold" to="/">QuizMaster</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-md mx-auto gap-2">
            <li class="nav-item rounded">
              <router-link class="nav-link active" aria-current="page" to="/">
                <i class="bi bi-house-fill me-2"></i>Home
              </router-link>
            </li>
            <li class="nav-item rounded">
              <router-link class="nav-link" to="/login">
                <i class="bi bi-box-arrow-in-right me-2"></i>Login
              </router-link>
            </li>
            <li class="nav-item rounded">
              <router-link class="nav-link" to="/register">
                <i class="bi bi-clipboard2-check-fill me-2"></i>Signup
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="container-fluid bg-dark text-white py-5 rounded">
      <div class="container py-4">
        <div class="row align-items-center">
          <div class="col-lg-6 mb-4 mb-lg-0">
            <h1>Test Your Knowledge</h1>
            <p class="lead mb-4">
              Challenge yourself with our extensive collection of quizzes across various categories and topics.
            </p>
            <div class="d-flex gap-3">
              <router-link to="/register" class="btn btn-light btn-lg px-4">
                <i class="bi bi-person-plus-fill me-2"></i>Get Started
              </router-link>
              <a href="#features" class="btn btn-outline-light btn-lg px-4">
                <i class="bi bi-info-circle-fill me-2"></i>Learn More
              </a>
            </div>
          </div>
          <div class="col-lg-6 text-center">
            <img 
              src="./../assets/quiz_logo.png" 
              width="350" 
              alt="Quiz App Illustration" 
              class="img-fluid rounded-3 shadow"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Categories Section -->
    <div class="container py-5">
      <h2 class="text-center mb-5">Popular Quiz Categories</h2>
      <div class="row g-4">
        <div 
          v-for="category in categories" 
          :key="category.name" 
          class="col-md-6 col-lg-3"
        >
          <div class="card border-0 shadow-sm rounded-3 text-center hover-effect">
            <div class="card-body p-4">
              <div 
                class="bg-dark text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" 
                style="width: 60px; height: 60px;"
              >
                <i :class="`bi ${category.icon}`" style="font-size: 1.5rem;"></i>
              </div>
              <h4>{{ category.name }}</h4>
              <p class="text-muted">{{ category.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="container-fluid bg-light py-5 rounded">
      <div class="container py-4">
        <h2 class="text-center mb-5">Why Choose Our Quiz App?</h2>
        <div class="row g-4">
          <div 
            v-for="feature in features" 
            :key="feature.title" 
            class="col-md-4"
          >
            <div class="card h-100 border-0 shadow-sm rounded-3">
              <div class="card-body p-4 text-center">
                <div 
                  class="bg-dark text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" 
                  style="width: 60px; height: 60px;"
                >
                  <i :class="`bi ${feature.icon}`" style="font-size: 1.5rem;"></i>
                </div>
                <h4>{{ feature.title }}</h4>
                <p class="text-muted">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Call to Action -->
    <div class="container-fluid bg-dark text-white py-5 mt-5 rounded">
      <div class="container py-4 text-center">
        <h2 class="mb-4">Ready to Test Your Knowledge?</h2>
        <p class="lead mb-4">Join thousands of users who challenge themselves daily with our quizzes.</p>
        <div class="d-flex justify-content-center gap-3">
          <router-link to="/register" class="btn btn-light btn-lg px-4">
            <i class="bi bi-person-plus-fill me-2"></i>Sign Up Now
          </router-link>
          <router-link to="/login" class="btn btn-outline-light btn-lg px-4">
            <i class="bi bi-box-arrow-in-right me-2"></i>Login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import NavBar from '@/components/NavBar.vue';
import FootPage from '@/components/FootPage.vue';
export default {
  name: 'HomeView',
  components: {
    NavBar,
    FootPage
  },
  data() {
    return {
      categories: [
        {
          name: 'Science',
          icon: 'bi-lightbulb-fill',
          description: 'Test your knowledge in Science with our challenging quizzes.'
        },
        {
          name: 'History',
          icon: 'bi-book-fill',
          description: 'Explore historical events and test your knowledge of the past.'
        },
        {
          name: 'Sports',
          icon: 'bi-trophy-fill',
          description: 'Challenge yourself with sports trivia and athletic knowledge.'
        },
        {
          name: 'Entertainment',
          icon: 'bi-film',
          description: 'Test your knowledge of movies, music, and pop culture.'
        }
      ],
      features: [
        {
          title: 'Challenging Questions',
          icon: 'bi-lightning-fill',
          description: 'Our quizzes feature carefully crafted questions to test your knowledge and skills.'
        },
        {
          title: 'Track Your Progress',
          icon: 'bi-graph-up-arrow',
          description: 'Monitor your performance and see how your knowledge improves over time.'
        },
        {
          title: 'Learn as You Go',
          icon: 'bi-mortarboard-fill',
          description: 'Gain new knowledge with detailed explanations for each question.'
        }
      ]
    }
  },
  mounted() {
    // Any initialization logic can go here
    console.log('Landing page mounted');
  }
}
</script>

<style scoped>
.hover-effect {
  transition: transform 0.3s ease-in-out;
}

.hover-effect:hover {
  transform: translateY(-5px);
}

.navbar-brand {
  font-size: 1.5rem;
}

.nav-link {
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 0.375rem;
}

.btn {
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
}

.card {
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
