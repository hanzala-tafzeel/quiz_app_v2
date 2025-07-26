<template>

<div class="page-wrapper d-flex flex-column min-vh-100">
  <NavPage/>
  <div class="container py-4">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading quiz results...</p>
    </div>

    <!-- Quiz Results Content -->
    <div v-else>


      <!-- Quiz Summary Card -->
      <div class="card mb-4 border-0 shadow-sm">
        <div class="card-header bg-dark text-white">
          <h5 class="mb-0">
            <i class="bi bi-graph-up me-2"></i>Quiz Summary
          </h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-3 col-6 text-center mb-3">
              <div class="border rounded-3 py-3">
                <h4 class="text-primary mb-1">{{ quizData.id }}</h4>
                <small class="text-muted">Quiz ID</small>
              </div>
            </div>
            <div class="col-md-3 col-6 text-center mb-3">
              <div class="border rounded-3 py-3">
                <h4 class="text-info mb-1">{{ quizData.questions.length }}</h4>
                <small class="text-muted">Questions</small>
              </div>
            </div>
            <div class="col-md-3 col-6 text-center mb-3">
              <div class="border rounded-3 py-3">
                <h4 class="text-warning mb-1">{{ correctAnswers }}</h4>
                <small class="text-muted">Correct</small>
              </div>
            </div>
            <div class="col-md-3 col-6 text-center mb-3">
              <div class="border rounded-3 py-3">
                <h4 class="text-danger mb-1">{{ incorrectAnswers }}</h4>
                <small class="text-muted">Incorrect</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Question Navigation Header -->
      <div class="card mb-3 border-0 shadow-sm">
        <div class="card-body py-3">
          <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
              <h6 class="mb-0 me-3">Question Navigation:</h6>
              <span class="text-muted">{{ currentQuestionIndex + 1 }} of {{ quizData.questions.length }}</span>
            </div>
            <div class="progress" style="width: 200px; height: 8px;">
              <div 
                class="progress-bar" 
                role="progressbar" 
                :style="{ width: ((currentQuestionIndex + 1) / quizData.questions.length) * 100 + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Current Question Display -->
      <div class="card border-0 shadow-sm mb-4" v-if="currentQuestion">
        <div class="card-header bg-dark text-white">
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="mb-0">
              <i class="bi bi-question-circle me-2"></i>Question {{ currentQuestionIndex + 1 }}
            </h5>
            <div class="d-flex gap-2">
              <span class="badge bg-light text-dark">
                <i class="bi bi-star-fill me-1"></i>{{ currentQuestion.marks }} marks
              </span>
              <span 
                class="badge"
                :class="currentQuestion.is_correct ? 'bg-success' : 'bg-danger'"
              >
                <i :class="currentQuestion.is_correct ? 'bi bi-check-lg' : 'bi bi-x-lg'" class="me-1"></i>
                {{ currentQuestion.is_correct ? 'Correct' : 'Incorrect' }}
              </span>
            </div>
          </div>
        </div>
        <div class="card-body">
          <!-- Question Text -->
          <div class="mb-4">
            <h6 class="mb-3">{{ currentQuestion.text }}</h6>
          </div>

          <!-- Options -->
          <div class="options-list">
            <div 
              v-for="(option, optionIndex) in currentQuestion.options" 
              :key="optionIndex"
              class="option-item mb-3 p-3 rounded-3 border"
              :class="getOptionClass(currentQuestion, optionIndex)"
            >
              <div class="d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center">
                  <span class="me-3 fw-bold text-muted">{{ String.fromCharCode(65 + optionIndex) }}.</span>
                  <span>{{ option }}</span>
                </div>
                <div class="d-flex gap-2">
                  <!-- Your Choice Badge -->
                  <span 
                    v-if="currentQuestion.selected_option === optionIndex" 
                    class="badge bg-primary"
                  >
                    <i class="bi bi-person-check me-1"></i>Your Choice
                  </span>
                  <!-- Correct Answer Badge -->
                  <span 
                    v-if="currentQuestion.correct_option === optionIndex" 
                    class="badge bg-success"
                  >
                    <i class="bi bi-check-circle me-1"></i>Correct Answer
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body py-3">
          <div class="d-flex justify-content-between align-items-center">
            <button 
              @click="previousQuestion" 
              class="btn btn-outline-secondary"
              :disabled="currentQuestionIndex === 0"
            >
              <i class="bi bi-chevron-left me-2"></i>Previous
            </button>
            
            <div class="d-flex align-items-center gap-2">
              <!-- Question Numbers -->
              <div class="d-flex flex-wrap gap-1">
                <button
                  v-for="(question, index) in quizData.questions"
                  :key="index"
                  @click="goToQuestion(index)"
                  class="btn btn-sm"
                  :class="getQuestionNumberClass(question, index)"
                  style="width: 35px; height: 35px;"
                >
                  {{ index + 1 }}
                </button>
              </div>
            </div>
            
            <button 
              @click="nextQuestion" 
              class="btn btn-outline-secondary"
              :disabled="currentQuestionIndex === quizData.questions.length - 1"
            >
              Next<i class="bi bi-chevron-right ms-2"></i>
            </button>
          </div>
        </div>
      </div>

            <!-- Result Status Card -->
        <div class="card mb-4 border-0 shadow-lg">
        <div class="card-body text-center py-5">
          <div >
            <i 
              :class="quizData.passed ? 'bi bi-check-circle-fill text-success' : 'bi bi-x-circle-fill text-danger'" 
              style="font-size: 4rem;"
            ></i>
          </div>
          <h2 class="mb-3" :class="quizData.passed ? 'text-success' : 'text-danger'">
            {{ quizData.passed ? 'Congratulations!' : 'Better Luck Next Time!' }}
          </h2>
          <h4 class="text-muted mb-4">{{ quizData.title }}</h4>
          <div class="row justify-content-center">
            <div class="col-md-6">
              <div class="bg-light rounded-3 p-4">
                <h1 class="display-4 mb-0" :class="quizData.passed ? 'text-success' : 'text-danger'">
                  {{ quizData.percentage.toFixed(1) }}%
                </h1>
                <p class="text-muted mb-0">{{ quizData.score }} / {{ quizData.total_marks }} marks</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      
    </div>
  </div>

  </div>

  <FootPage/>
</template>

<script>

import NavPage from '@/components/NavBar.vue';
import FootPage from '@/components/FootPage.vue';

export default {
  name: 'quizScore',
  components:{
    NavPage,
    FootPage
  },   

  props: {
    attemptId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      loading: true,
      currentQuestionIndex: 0,
      quizData: {
        id: null,
        title: '',
        total_marks: 0,
        score: 0,
        percentage: 0,
        passed: false,
        start_time: null,
        end_time: null,
        questions: []
      }
    }
  },
  computed: {
    correctAnswers() {
      return this.quizData.questions.filter(q => q.is_correct).length;
    },
    incorrectAnswers() {
      return this.quizData.questions.filter(q => !q.is_correct).length;
    },
    currentQuestion() {
      return this.quizData.questions[this.currentQuestionIndex] || null;
    }
  },
  methods: {
    async fetchQuizResults() {
      try {
        this.loading = true;
        

        const token = window.sessionStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5000/api/attempts/${this.attemptId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.quizData = data;
        } else {
          console.error('Failed to fetch quiz results');
          this.$router.push('/');
        }
      } catch (error) {
        console.error('Error fetching quiz results:', error);
        this.$router.push('/');
      } finally {
        this.loading = false;
      }
    },

    getOptionClass(question, optionIndex) {
      const isSelected = question.selected_option === optionIndex;
      const isCorrect = question.correct_option === optionIndex;
      
      if (isCorrect && isSelected) {
        return 'border-success bg-success bg-opacity-10'; // Correct and selected
      } else if (isCorrect) {
        return 'border-success bg-success bg-opacity-25'; // Correct answer
      } else if (isSelected) {
        return 'border-danger bg-danger bg-opacity-10'; // Wrong selection
      }
      return 'border-light'; // Default
    },

    getQuestionNumberClass(question, index) {
      const isActive = index === this.currentQuestionIndex;
      if (isActive) {
        return question.is_correct ? 'btn-success' : 'btn-danger';
      } else {
        return question.is_correct ? 'btn-outline-success' : 'btn-outline-danger';
      }
    },

    nextQuestion() {
      if (this.currentQuestionIndex < this.quizData.questions.length - 1) {
        this.currentQuestionIndex++;
      }
    },

    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
      }
    },

    goToQuestion(index) {
      this.currentQuestionIndex = index;
    },

    retakeQuiz() {
      this.$router.push(`/quiz/${this.quizData.id}`);
    }
  },

  mounted() {
    this.fetchQuizResults();
  }
}
</script>

<style scoped>
.option-item {
  transition: all 0.2s ease-in-out;
}

.option-item:hover {
  transform: translateX(5px);
}

.bg-opacity-10 {
  --bs-bg-opacity: 0.1;
}

.bg-opacity-25 {
  --bs-bg-opacity: 0.25;
}

.shadow-lg {
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175) !important;
}

.border-0 {
  border: 0 !important;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.progress {
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
}
</style>