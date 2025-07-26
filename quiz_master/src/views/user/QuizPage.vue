<template>
  
  <div>
    <!-- Start Quiz Modal -->
    <div v-if="showStartModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">
              <i class="bi bi-play-circle me-2"></i>Start Quiz
            </h5>
          </div>
          <div class="modal-body">
            <div class="alert alert-info mb-3">
              <i class="bi bi-info-circle me-2"></i>
              The quiz will be for {{ Math.floor(quizData.duration / 60) }} minutes. Once started, the timer cannot be paused.
            </div>
            <div class="row g-3">
              <div class="col-6">
                <div class="card text-center h-100">
                  <div class="card-body">
                    <h3 class="text-dark mb-1">{{ quizData.questions ? quizData.questions.length : 0 }}</h3>
                    <small class="text-muted">Questions</small>
                  </div>
                </div>
              </div>
              <div class="col-6">
                <div class="card text-center h-100">
                  <div class="card-body">
                    <h3 class="text-dark mb-1">{{ Math.floor(quizData.duration / 60) }}</h3>
                    <small class="text-muted">Minutes</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-dark btn-lg w-100" @click="startQuiz">
              <i class="bi bi-play-fill me-2"></i>Start Quiz
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Quiz Container -->
    <div class="container-fluid py-3">
      <div class="row g-3">
        <!-- Sidebar - Collapsible on Mobile -->
        <div class="col-lg-3">
          <div class="position-sticky" style="top: 1rem;">
            <!-- Mobile Toggle Button -->
            <button class="btn btn-outline-dark d-lg-none w-100 mb-3" type="button" 
                    data-bs-toggle="collapse" data-bs-target="#quizSidebar">
              <i class="bi bi-list me-2"></i>Quiz Info & Navigation
            </button>

            <!-- Collapsible Sidebar Content -->
            <div class="collapse d-lg-block" id="quizSidebar">
              <!-- Quiz Summary -->
              <div class="card mb-3">
                <div class="card-header bg-dark text-white">
                  <h6 class="mb-0">
                    <i class="bi bi-clipboard-data me-2"></i>Quiz Summary
                  </h6>
                </div>
                <div class="card-body">
                  <div class="row g-2 text-center">
                    <div class="col-6">
                      <div class="bg-light rounded p-2">
                        <div class="fw-bold text-dark">{{ quizData.id }}</div>
                        <small class="text-muted">Quiz ID</small>
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="bg-light rounded p-2">
                        <div class="fw-bold text-dark">{{ quizData.total_marks }}</div>
                        <small class="text-muted">Total Marks</small>
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="bg-light rounded p-2">
                        <div class="fw-bold text-dark">{{ quizData.questions ? quizData.questions.length : 0 }}</div>
                        <small class="text-muted">Questions</small>
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="bg-light rounded p-2">
                        <div class="fw-bold text-dark">{{ Math.floor(quizData.duration / 60) }}</div>
                        <small class="text-muted">Minutes</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Timer -->
              <div class="card mb-3">
                <div class="card-body text-center">
                  <div class="mb-2">
                    <i class="bi bi-clock" :class="timeRemaining <= 300 ? 'text-danger' : 'text-success'"></i>
                    <small class="text-muted ms-1">Time Remaining</small>
                  </div>
                  <h4 class="mb-2" :class="timeRemaining <= 300 ? 'text-danger' : 'text-success'">
                    {{ formatTimeRemaining(timeRemaining) }}
                  </h4>
                  <div class="progress" style="height: 6px;">
                    <div class="progress-bar" 
                         :class="timeRemaining <= 300 ? 'bg-danger' : 'bg-success'"
                         :style="`width: ${(timeRemaining / quizData.duration) * 100}%`"></div>
                  </div>
                </div>
              </div>

              <!-- Question Navigation -->
              <div class="card">
                <div class="card-header">
                  <h6 class="mb-0">
                    <i class="bi bi-grid-3x3-gap me-2"></i>Questions
                  </h6>
                </div>
                <div class="card-body">
                  <div class="d-grid gap-2" style="grid-template-columns: repeat(auto-fit, minmax(40px, 1fr)); display: grid;">
                    <button v-for="(question, index) in quizData.questions" 
                            :key="question.id" 
                            class="btn btn-sm"
                            :class="getQuestionButtonClass(index, question.id)"
                            @click="goToQuestion(index)">
                      {{ index + 1 }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content -->
        <div class="col-lg-9">
          <!-- Quiz Title -->
          <div class="card mb-3">
            <div class="card-header bg-dark text-white">
              <h4 class="mb-0">{{ quizData.title }}</h4>
            </div>
          </div>

          <!-- Current Question -->
          <div v-if="quizData.questions.length > 0" class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center flex-wrap">
              <div class="mb-2 mb-sm-0">
                <h5 class="mb-0">Question {{ currentQuestionIndex + 1 }}</h5>
                <small class="text-muted">of {{ quizData.questions.length }} questions</small>
              </div>
              <span class="badge bg-secondary fs-6">{{ currentQuestion.marks }} marks</span>
            </div>
            
            <div class="card-body">
              <!-- Question Text -->
              <div class="mb-4">
                <h5 class="lh-base">{{ currentQuestion.text }}</h5>
              </div>

              <!-- Answer Options -->
              <div class="d-grid gap-3">
                <div v-for="(option, optionIndex) in currentQuestion.options" 
                     :key="optionIndex"
                     class="card border"
                     :class="getOptionClass(optionIndex)"
                     style="cursor: pointer;"
                     @click="selectOption(optionIndex)">
                  <div class="card-body py-3">
                    <div class="d-flex align-items-start">
                      <div class="form-check me-3">
                        <input class="form-check-input" 
                               type="radio" 
                               :name="`question_${currentQuestion.id}`"
                               :id="`option${optionIndex}_${currentQuestion.id}`" 
                               :value="optionIndex" 
                               :disabled="!quizStarted"
                               v-model="answers[currentQuestion.id]">
                      </div>
                      <label class="form-check-label flex-grow-1 lh-base user-select-none" 
                             :for="`option${optionIndex}_${currentQuestion.id}`">
                        {{ option }}
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Navigation Controls -->
          <div class="card">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-4 mb-2 mb-md-0">
                  <button type="button" 
                          class="btn btn-outline-secondary w-100 w-md-auto" 
                          @click="previousQuestion"
                          :disabled="currentQuestionIndex === 0 || !quizStarted">
                    <i class="bi bi-arrow-left me-2"></i>Previous
                  </button>
                </div>
                
                <div class="col-md-4 text-center mb-2 mb-md-0">
                  <div class="progress mb-2" style="height: 4px;">
                    <div class="progress-bar bg-dark" 
                         :style="`width: ${((currentQuestionIndex + 1) / quizData.questions.length) * 100}%`"></div>
                  </div>
                  <small class="text-muted">
                    {{ currentQuestionIndex + 1 }} of {{ quizData.questions.length }}
                  </small>
                </div>

                <div class="col-md-4 text-end">
                  <button v-if="currentQuestionIndex < quizData.questions.length - 1" 
                          type="button"
                          class="btn btn-outline-secondary w-100 w-md-auto" 
                          @click="nextQuestion" 
                          :disabled="!quizStarted">
                    Next<i class="bi bi-arrow-right ms-2"></i>
                  </button>

                  <button v-else 
                          type="button"
                          class="btn btn-success w-100 w-md-auto" 
                          @click="submitQuiz" 
                          :disabled="!quizStarted">
                    <i class="bi bi-check-circle me-2"></i>Submit Quiz
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" 
         style="background-color: rgba(0,0,0,0.5); z-index: 2000;">
      <div class="spinner-border text-dark" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuizPage',
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
        const token = window.sessionStorage.getItem('token');
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

    selectOption(optionIndex) {
      if (this.quizStarted) {
        this.answers[this.currentQuestion.id] = optionIndex;
      }
    },

    getQuestionButtonClass(index, questionId) {
      if (this.currentQuestionIndex === index) {
        return 'btn-dark';
      } else if (this.answers[questionId] !== null) {
        return 'btn-success';
      } else {
        return 'btn-outline-secondary';
      }
    },

    getOptionClass(optionIndex) {
      return this.answers[this.currentQuestion.id] === optionIndex 
        ? 'border-dark bg-dark bg-opacity-10' 
        : 'border-secondary';
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

        const token = window.sessionStorage.getItem('token');
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