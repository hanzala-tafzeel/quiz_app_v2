<template>
  <div class="container py-4">
    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex align-items-center justify-content-between">
          <div>
            <h2 class="mb-2">
              <i class="bi bi-clock-history me-2 text-primary"></i>
              Quiz History
            </h2>
            <p class="text-muted mb-0">Track your quiz performance and progress</p>
          </div>
          <div>
            <button 
              @click="fetchAttempts" 
              class="btn btn-outline-primary"
              :disabled="loading"
            >
              <i class="bi bi-arrow-clockwise me-2"></i>
              {{ loading ? 'Refreshing...' : 'Refresh' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="text-primary mb-2">
              <i class="bi bi-journal-text" style="font-size: 2rem;"></i>
            </div>
            <h4 class="mb-1">{{ totalAttempts }}</h4>
            <small class="text-muted">Total Attempts</small>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="text-success mb-2">
              <i class="bi bi-check-circle" style="font-size: 2rem;"></i>
            </div>
            <h4 class="mb-1">{{ completedAttempts }}</h4>
            <small class="text-muted">Completed</small>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="text-info mb-2">
              <i class="bi bi-percent" style="font-size: 2rem;"></i>
            </div>
            <h4 class="mb-1">{{ averageScore.toFixed(1) }}%</h4>
            <small class="text-muted">Average Score</small>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body text-center">
            <div class="text-warning mb-2">
              <i class="bi bi-trophy" style="font-size: 2rem;"></i>
            </div>
            <h4 class="mb-1">{{ bestScore.toFixed(1) }}%</h4>
            <small class="text-muted">Best Score</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading your quiz history...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="attempts.length === 0" class="text-center py-5">
      <div class="mb-4">
        <i class="bi bi-inbox" style="font-size: 4rem; color: #dee2e6;"></i>
      </div>
      <h4 class="text-muted mb-3">No Quiz Attempts Yet</h4>
      <p class="text-muted mb-4">Start taking quizzes to see your history here</p>
      <button 
        @click="$router.push('/')" 
        class="btn btn-primary btn-lg"
      >
        <i class="bi bi-play-circle me-2"></i>Take Your First Quiz
      </button>
    </div>

    <!-- Quiz Attempts List -->
    <div v-else>
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-dark text-white">
          <h5 class="mb-0">
            <i class="bi bi-list-ul me-2"></i>
            Quiz Attempts ({{ attempts.length }})
          </h5>
        </div>
        <div class="card-body p-0">
          <!-- Desktop View -->
          <div class="d-none d-md-block">
            <div class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="bg-light">
                  <tr>
                    <th class="border-0">Quiz Title</th>
                    <th class="border-0">Date</th>
                    <th class="border-0 text-center">Score</th>
                    <th class="border-0 text-center">Percentage</th>
                    <th class="border-0 text-center">Status</th>
                    <th class="border-0 text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="attempt in paginatedAttempts" 
                    :key="attempt.id"
                    class="attempt-row"
                  >
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="me-3">
                          <div 
                            class="rounded-circle d-flex align-items-center justify-content-center"
                            :class="getStatusColor(attempt.percentage)"
                            style="width: 40px; height: 40px; font-size: 0.8rem; font-weight: bold;"
                          >
                            {{ attempt.percentage.toFixed(0) }}%
                          </div>
                        </div>
                        <div>
                          <h6 class="mb-1">{{ attempt.quiz_title }}</h6>
                          <small class="text-muted">Quiz ID: {{ attempt.quiz_id }}</small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div>
                        <div class="fw-medium">{{ formatDate(attempt.start_time) }}</div>
                        <small class="text-muted">{{ formatTime(attempt.start_time) }}</small>
                      </div>
                    </td>
                    <td class="text-center">
                      <span class="fw-bold">{{ attempt.score }}</span> / {{ attempt.total_marks }}
                    </td>
                    <td class="text-center">
                      <div class="progress" style="height: 20px;">
                        <div 
                          class="progress-bar"
                          :class="getProgressBarClass(attempt.percentage)"
                          :style="{ width: attempt.percentage + '%' }"
                        >
                          {{ attempt.percentage.toFixed(1) }}%
                        </div>
                      </div>
                    </td>
                    <td class="text-center">
                      <span 
                        class="badge"
                        :class="attempt.is_completed ? 'bg-success' : 'bg-warning'"
                      >
                        {{ attempt.is_completed ? 'Completed' : 'In Progress' }}
                      </span>
                    </td>
                    <td class="text-center">
                      <button 
                        @click="viewResults(attempt.id)"
                        class="btn btn-sm btn-outline-primary me-2"
                        :disabled="!attempt.is_completed"
                      >
                        <i class="bi bi-eye"></i>
                      </button>
                      <button 
                        @click="retakeQuiz(attempt.quiz_id)"
                        class="btn btn-sm btn-outline-secondary"
                      >
                        <i class="bi bi-arrow-clockwise"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Mobile View -->
          <div class="d-md-none">
            <div 
              v-for="attempt in paginatedAttempts" 
              :key="attempt.id"
              class="border-bottom p-3"
            >
              <div class="d-flex align-items-start justify-content-between mb-2">
                <div class="flex-grow-1">
                  <h6 class="mb-1">{{ attempt.quiz_title }}</h6>
                  <small class="text-muted">{{ formatDate(attempt.start_time) }} at {{ formatTime(attempt.start_time) }}</small>
                </div>
                <div class="text-end">
                  <div 
                    class="badge fs-6 px-2 py-1"
                    :class="getScoreBadgeClass(attempt.percentage)"
                  >
                    {{ attempt.percentage.toFixed(1) }}%
                  </div>
                </div>
              </div>
              
              <div class="row align-items-center mb-3">
                <div class="col-6">
                  <small class="text-muted">Score:</small>
                  <div class="fw-bold">{{ attempt.score }} / {{ attempt.total_marks }}</div>
                </div>
                <div class="col-6 text-end">
                  <span 
                    class="badge"
                    :class="attempt.is_completed ? 'bg-success' : 'bg-warning'"
                  >
                    {{ attempt.is_completed ? 'Completed' : 'In Progress' }}
                  </span>
                </div>
              </div>
              
              <div class="d-flex gap-2">
                <button 
                  @click="viewResults(attempt.id)"
                  class="btn btn-sm btn-outline-primary flex-fill"
                  :disabled="!attempt.is_completed"
                >
                  <i class="bi bi-eye me-1"></i>View Results
                </button>
                <button 
                  @click="retakeQuiz(attempt.quiz_id)"
                  class="btn btn-sm btn-outline-secondary flex-fill"
                >
                  <i class="bi bi-arrow-clockwise me-1"></i>Retake
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
        <nav>
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button 
                class="page-link" 
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
              >
                Previous
              </button>
            </li>
            <li 
              v-for="page in visiblePages" 
              :key="page"
              class="page-item" 
              :class="{ active: currentPage === page }"
            >
              <button 
                class="page-link" 
                @click="changePage(page)"
              >
                {{ page }}
              </button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <button 
                class="page-link" 
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
              >
                Next
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuizHistory',
  data() {
    return {
      loading: false,
      attempts: [],
      currentPage: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    totalAttempts() {
      return this.attempts.length;
    },
    completedAttempts() {
      return this.attempts.filter(attempt => attempt.is_completed).length;
    },
    averageScore() {
      if (this.completedAttempts === 0) return 0;
      const totalPercentage = this.attempts
        .filter(attempt => attempt.is_completed)
        .reduce((sum, attempt) => sum + attempt.percentage, 0);
      return totalPercentage / this.completedAttempts;
    },
    bestScore() {
      if (this.completedAttempts === 0) return 0;
      return Math.max(...this.attempts
        .filter(attempt => attempt.is_completed)
        .map(attempt => attempt.percentage));
    },
    totalPages() {
      return Math.ceil(this.attempts.length / this.itemsPerPage);
    },
    paginatedAttempts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.attempts.slice(start, end);
    },
    visiblePages() {
      const pages = [];
      const start = Math.max(1, this.currentPage - 2);
      const end = Math.min(this.totalPages, this.currentPage + 2);
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    }
  },
  methods: {
    async fetchAttempts() {
      try {
        this.loading = true;
        
        const token = localStorage.getItem("token");
        const response = await fetch('http://127.0.0.1:5000/api/attempts', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          // Sort attempts by start_time in descending order (newest first)
          this.attempts = data.attempts.sort((a, b) => 
            new Date(b.start_time) - new Date(a.start_time)
          );
        } else {
          console.error('Failed to fetch quiz attempts');
          if (response.status === 401) {
            this.$router.push('/login');
          }
        }
      } catch (error) {
        console.error('Error fetching quiz attempts:', error);
      } finally {
        this.loading = false;
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatTime(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    getStatusColor(percentage) {
      if (percentage >= 80) return 'bg-success text-white';
      if (percentage >= 60) return 'bg-warning text-dark';
      return 'bg-danger text-white';
    },

    getProgressBarClass(percentage) {
      if (percentage >= 80) return 'bg-success';
      if (percentage >= 60) return 'bg-warning';
      return 'bg-danger';
    },

    getScoreBadgeClass(percentage) {
      if (percentage >= 80) return 'bg-success';
      if (percentage >= 60) return 'bg-warning';
      return 'bg-danger';
    },

    viewResults(attemptId) {
      this.$router.push(`/user/quiz/${attemptId}/score`);
    },

    retakeQuiz(quizId) {
      this.$router.push(`/quiz/${quizId}`);
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    }
  },

  mounted() {
    this.fetchAttempts();
  }
}
</script>

<style scoped>
.attempt-row:hover {
  background-color: rgba(0, 123, 255, 0.05);
}

.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.progress {
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: bold;
}

.border-0 {
  border: 0 !important;
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
}

@media (max-width: 767.98px) {
  .container {
    padding-left: 15px;
    padding-right: 15px;
  }
}
</style>
