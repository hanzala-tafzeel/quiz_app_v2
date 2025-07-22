<template>
  <div>
    <!-- Pop up to start quiz -->
    <div 
      v-if="showStartModal" 
      class="modal-backdrop" 
      @click.stop
    >
      <div class="modal-dialog modal-dialog-centered" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Start Quiz</h5>
          </div>
          <div class="modal-body">
            <p>The quiz will be for {{ Math.floor(quizData.duration / 60) }} minutes. Once started, the timer cannot be paused.</p>
            <ul class="list-group">
              <li class="list-group-item">Total Questions: {{ quizData.questions ? quizData.questions.length : 0 }}</li>
              <li class="list-group-item">Duration: {{ Math.floor(quizData.duration / 60) }} minutes</li>
            </ul>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-dark" @click="startQuiz">Start Quiz</button>
          </div>
        </div>
      </div>
    </div>

    <div class="container-fluid py-4">
      <div class="row">
        <!-- Left Fixed Section -->
        <div class="col-md-3 fixed-left">
          <div class="card shadow">
            <div class="card-body">
              <h4 class="card-title text-dark mb-4">Quiz Summary</h4>
              <ul class="list-group list-group-flush">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Quiz ID:</span>
                  <span class="badge bg-dark">{{ quizData.id }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Total Marks:</span>
                  <span class="badge bg-dark">{{ quizData.total_marks }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Total Questions:</span>
                  <span class="badge bg-dark">{{ quizData.questions ? quizData.questions.length : 0 }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Duration:</span>
                  <span class="badge bg-dark">{{ Math.floor(quizData.duration / 60) }} minutes</span>
                </li>
              </ul>

              <!-- Enhanced Timer Display -->
              <div class="mt-4">
                <div class="card" :class="timeRemaining <= 300 ? 'border-danger' : 'border-success'">
                  <div class="card-body text-center p-3">
                    <h5 class="card-title mb-2">
                      <i class="bi bi-clock me-2"></i>Time Remaining
                    </h5>
                    <h3 class="mb-0" :class="timeRemaining <= 300 ? 'text-danger' : 'text-success'">
                      {{ formatTimeRemaining(timeRemaining) }}
                    </h3>
                    <div class="progress mt-3" style="height: 8px;">
                      <div 
                        class="progress-bar" 
                        :class="timeRemaining <= 300 ? 'bg-danger' : 'bg-success'"
                        role="progressbar" 
                        :style="`width: ${(timeRemaining / quizData.duration) * 100}%`"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Question Navigation -->
              <div class="mt-4">
                <h5 class="card-title text-dark mb-3">Question Navigation</h5>
                <div class="d-flex flex-wrap gap-2">
                  <button 
                    v-for="(question, index) in quizData.questions" 
                    :key="question.id"
                    class="btn btn-sm"
                    :class="currentQuestionIndex === index ? 'btn-dark' : (answers[question.id] !== null ? 'btn-success' : 'btn-outline-dark')"
                    @click="goToQuestion(index)"
                  >
                    {{ index + 1 }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Scrollable Section -->
        <div class="col-md-9">
          <!-- Quiz Header -->
          <div class="card mb-4 shadow">
            <div class="card-header bg-dark text-white">
              <h3 class="mb-0">{{ quizData.title }}</h3>
            </div>
          </div>

          <!-- Single Question Display -->
          <div v-if="quizData.questions.length > 0" class="card shadow mb-4">
            <div class="card-header bg-light">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Question {{ currentQuestionIndex + 1 }} of {{ quizData.questions.length }}</h5>
                <span class="badge bg-secondary">Marks: {{ currentQuestion.marks }}</span>
              </div>
            </div>
            <div class="card-body">
              <h4 class="mb-4">{{ currentQuestion.text }}</h4>
              
              <!-- Options -->
              <div class="d-flex flex-column gap-3">
                <div 
                  v-for="(option, optionIndex) in currentQuestion.options" 
                  :key="optionIndex"
                  class="form-check p-3 border rounded"
                  :class="answers[currentQuestion.id] === optionIndex ? 'border-primary bg-light' : 'border-secondary'"
                >
                  <input 
                    class="form-check-input" 
                    type="radio" 
                    :name="`question_${currentQuestion.id}`"
                    :id="`option${optionIndex}_${currentQuestion.id}`" 
                    :value="optionIndex"
                    :disabled="!quizStarted"
                    v-model="answers[currentQuestion.id]"
                  >
                  <label 
                    class="form-check-label ms-2 fw-normal" 
                    :for="`option${optionIndex}_${currentQuestion.id}`"
                  >
                    {{ option }}
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Navigation Buttons -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <button 
              type="button" 
              class="btn btn-outline-secondary"
              @click="previousQuestion"
              :disabled="currentQuestionIndex === 0 || !quizStarted"
            >
              <i class="bi bi-arrow-left me-2"></i>Previous
            </button>

            <div class="text-center">
              <span class="text-muted">
                Question {{ currentQuestionIndex + 1 }} of {{ quizData.questions.length }}
              </span>
            </div>

            <div>
              <button 
                v-if="currentQuestionIndex < quizData.questions.length - 1"
                type="button" 
                class="btn btn-outline-secondary"
                @click="nextQuestion"
                :disabled="!quizStarted"
              >
                Next<i class="bi bi-arrow-right ms-2"></i>
              </button>
              
              <button 
                v-if="currentQuestionIndex === quizData.questions.length - 1"
                type="button" 
                class="btn btn-success"
                @click="submitQuiz"
                :disabled="!quizStarted"
              >
                <i class="bi bi-check-circle me-2"></i>Submit Quiz
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'quizPage',
  props: {
    quizId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      quizData: {
        id: null,
        title: '',
        duration: 0,
        total_marks: 0,
        questions: []
      },
      showStartModal: true,
      quizStarted: false,
      timeRemaining: 0,
      timer: null,
      answers: {},
      loading: false,
      currentQuestionIndex: 0
    }
  },
  computed: {
    currentQuestion() {
      return this.quizData.questions[this.currentQuestionIndex] || {};
    }
  },
  methods: {
    async fetchQuizData() {
      try {
        this.loading = true;
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${this.quizId}/attempt`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.quizData = data;
          this.timeRemaining = this.quizData.duration;
          
          const answersObj = {};
          this.quizData.questions.forEach(question => {
            answersObj[question.id] = null;
          });
          this.answers = answersObj;
          
        } else {
          console.error('Failed to fetch quiz data');
          this.$router.push('/');
        }
      } catch (error) {
        console.error('Error fetching quiz data:', error);
        this.$router.push('/');
      } finally {
        this.loading = false;
      }
    },

    startQuiz() {
      this.quizStarted = true;
      this.showStartModal = false;
      this.startTimer();
    },

    startTimer() {
      this.timer = setInterval(() => {
        this.timeRemaining--;

        if (this.timeRemaining <= 0) {
          clearInterval(this.timer);
          alert("Time is up!");
          this.submitQuiz();
        }
      }, 1000);
    },

    formatTimeRemaining(seconds) {
      const minutes = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    },

    // Navigation methods
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

    async submitQuiz() {
      if (this.timer) {
        clearInterval(this.timer);
      }

      try {
        this.loading = true;
        
        const responses = Object.entries(this.answers)
          .filter(([questionId, selectedOption]) => selectedOption !== null)
          .map(([questionId, selectedOption]) => ({
            question_id: parseInt(questionId),
            selected_option: parseInt(selectedOption)
          }));

        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${this.quizId}/attempt`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            responses: responses
          })
        });

        if (response.ok) {
          const result = await response.json();
          sessionStorage.setItem('quizResult', JSON.stringify(result));
          this.$router.push(`/user/quiz/${result.attempt_id}/score`);
        } else {
          const errorData = await response.json();
          console.error('Failed to submit quiz:', errorData);
          alert(`Failed to submit quiz: ${errorData.message || 'Please try again.'}`);
        }
      } catch (error) {
        console.error('Error submitting quiz:', error);
        alert('Error submitting quiz. Please try again.');
      } finally {
        this.loading = false;
      }
    }
  },

  mounted() {
    this.fetchQuizData();
  },

  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
}
</script>

<style scoped>
.fixed-left {
  position: sticky;
  top: 20px;
  height: calc(100vh - 40px);
  overflow-y: auto;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-dialog {
  background: white;
  border-radius: 0.375rem;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.gap-2 {
  gap: 0.5rem;
}

.gap-3 {
  gap: 1rem;
}
</style>