<template>
  <!-- page for user dashboard -->

  <NavPage />

  <div class="container mt-2">
    <div class="row container">

      <div class="col-md-6">
        <h1 class="text-dark">Welcome, {{ capitalize(user.username) }}</h1>
      </div>
      <div class="col-md-6">
        <form @submit.prevent="searchQuiz" class="float-end">
          <div class="input-group mb-3">
            <input v-model="search" type="text" class="form-control" placeholder="Search Quiz" />
          </div>
        </form>
      </div>
    </div>

    <!-- Available Quizzes (Currently Open) -->
    <div class="card mb-4">
      <div class="card-header bg-success text-white">
        <h5 class="card-title mb-0">
          <i class="bi bi-play-circle me-2"></i>Available Quizzes
          <span class="badge bg-light text-dark ms-2">{{ availableQuizzes.length }}</span>
        </h5>
      </div>
      <div class="card-body">
        <div v-if="availableQuizzes.length === 0" class="text-center py-4 text-muted">
          <i class="bi bi-calendar-x" style="font-size: 3rem;"></i>
          <h5 class="mt-3">No Quizzes Available Right Now</h5>
          <p>Check the upcoming section for scheduled quizzes</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Quiz Title</th>
                <th>Questions</th>
                <th>Duration</th>
                <th>End Time</th>
                <th>Time Remaining</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quiz in availableQuizzes" :key="quiz.id">
                <td>
                  <strong>{{ quiz.title }}</strong>
                  <br>
                  <small class="text-muted">{{ quiz.description || 'No description' }}</small>
                </td>
                <td>
                  <span class="badge bg-info">{{ quiz.questions_count }} questions</span>
                </td>
                <td>{{ quiz.duration }} min</td>
                <td>
                  <span v-if="quiz.end_date">
                    {{ formatDateTime(quiz.end_date) }}
                  </span>
                  <span v-else class="text-muted">No end time</span>
                </td>
                <td>
                  <span v-if="quiz.end_date" :class="getTimeRemainingClass(quiz)">
                    {{ getTimeRemaining(quiz.end_date) }}
                  </span>
                  <span v-else class="text-success">Always available</span>
                </td>
                <td>
                  <div class="d-flex gap-2">
                    <button class="btn btn-outline-primary btn-sm" @click="openDetailsModal(quiz)">
                      <i class="bi bi-eye me-1"></i>View
                    </button>
                    <router-link 
                      :to="`/user/quiz/${quiz.id}`" 
                      class="btn btn-success btn-sm"
                    >
                      <i class="bi bi-play me-1"></i>Start Quiz
                    </router-link>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Upcoming Quizzes -->
    <div class="card mb-4">
      <div class="card-header bg-warning text-dark">
        <h5 class="card-title mb-0">
          <i class="bi bi-calendar-event me-2"></i>Upcoming Quizzes
          <span class="badge bg-dark text-white ms-2">{{ upcomingQuizzes.length }}</span>
        </h5>
      </div>
      <div class="card-body">
        <div v-if="upcomingQuizzes.length === 0" class="text-center py-4 text-muted">
          <i class="bi bi-calendar-plus" style="font-size: 3rem;"></i>
          <h5 class="mt-3">No Upcoming Quizzes</h5>
          <p>All scheduled quizzes will appear here</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Quiz Title</th>
                <th>Questions</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Starts In</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quiz in upcomingQuizzes" :key="quiz.id">
                <td>
                  <strong>{{ quiz.title }}</strong>
                  <br>
                  <small class="text-muted">{{ quiz.description || 'No description' }}</small>
                </td>
                <td>
                  <span class="badge bg-info">{{ quiz.questions_count }} questions</span>
                </td>
                <td>
                  {{ formatDateTime(quiz.start_date) }}
                </td>
                <td>
                  <span v-if="quiz.end_date">
                    {{ formatDateTime(quiz.end_date) }}
                  </span>
                  <span v-else class="text-muted">No end time</span>
                </td>
                <td class="text-primary">
                  {{ getTimeUntilStart(quiz.start_date) }}
                </td>
                <td>
                  <div class="d-flex gap-2">
                    <button class="btn btn-outline-primary btn-sm" @click="openDetailsModal(quiz)">
                      <i class="bi bi-eye me-1"></i>View
                    </button>
                    <button class="btn btn-warning btn-sm text-dark" disabled>
                      <i class="bi bi-clock me-1"></i>Not Available
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Expired Quizzes -->
    <div class="card mb-4">
      <div class="card-header bg-danger text-white">
        <h5 class="card-title mb-0">
          <i class="bi bi-x-circle me-2"></i>Expired Quizzes
          <span class="badge bg-light text-dark ms-2">{{ expiredQuizzes.length }}</span>
        </h5>
      </div>
      <div class="card-body">
        <div v-if="expiredQuizzes.length === 0" class="text-center py-4 text-muted">
          <i class="bi bi-check-circle" style="font-size: 3rem; color: #28a745;"></i>
          <h5 class="mt-3">No Expired Quizzes</h5>
          <p>Great! You haven't missed any quizzes yet</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Quiz Title</th>
                <th>Questions</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Expired</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quiz in expiredQuizzes" :key="quiz.id" class="table-light">
                <td>
                  <strong class="text-muted">{{ quiz.title }}</strong>
                  <br>
                  <small class="text-muted">{{ quiz.description || 'No description' }}</small>
                </td>
                <td>
                  <span class="badge bg-secondary">{{ quiz.questions_count }} questions</span>
                </td>
                <td class="text-muted">
                  {{ formatDateTime(quiz.start_date) }}
                </td>
                <td class="text-muted">
                  {{ formatDateTime(quiz.end_date) }}
                </td>
                <td class="text-danger">
                  {{ getTimeSinceExpiry(quiz.end_date) }} ago
                </td>
                <td>
                  <button class="btn btn-outline-secondary btn-sm" disabled>
                    <i class="bi bi-eye-slash me-1"></i>Expired
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Quiz Details Modal -->
    <div class="modal fade" id="quizDetailsModal" tabindex="-1" aria-labelledby="quizDetailsModalLabel"
      aria-hidden="true" ref="quizModal">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content" v-if="selectedQuiz">
          <div class="modal-header" :class="getModalHeaderClass(selectedQuiz)">
            <h5 class="modal-title text-white" id="quizDetailsModalLabel">
              {{ selectedQuiz.title }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"
              @click="closeDetailsModal"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <h6>Quiz Information</h6>
                <ul class="list-unstyled">
                  <li><strong>Duration:</strong> {{ selectedQuiz.duration }} minutes</li>
                  <li><strong>Total Questions:</strong> {{ selectedQuiz.questions_count }}</li>
                  <li><strong>Total Marks:</strong> {{ selectedQuiz.total_marks }}</li>
                  <li><strong>Pass Marks:</strong> {{ selectedQuiz.pass_marks }}</li>
                  <li><strong>Status:</strong> 
                    <span :class="getStatusBadgeClass(selectedQuiz)">
                      {{ getQuizStatus(selectedQuiz) }}
                    </span>
                  </li>
                </ul>
              </div>
              <div class="col-md-6">
                <h6>Schedule</h6>
                <ul class="list-unstyled">
                  <li v-if="selectedQuiz.start_date">
                    <strong>Starts:</strong> {{ formatDateTime(selectedQuiz.start_date) }}
                  </li>
                  <li v-if="selectedQuiz.end_date">
                    <strong>Ends:</strong> {{ formatDateTime(selectedQuiz.end_date) }}
                  </li>
                  <li v-if="!selectedQuiz.start_date && !selectedQuiz.end_date">
                    <strong>Schedule:</strong> <span class="text-success">Always Available</span>
                  </li>
                  <li>
                    <strong>Created:</strong> {{ formatDateTime(selectedQuiz.created_at) }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="mt-3">
              <h6>Description</h6>
              <p class="text-muted">{{ selectedQuiz.description || 'No description available' }}</p>
            </div>
            <div class="alert" :class="getAlertClass(selectedQuiz)">
              <i :class="getAlertIcon(selectedQuiz)" class="me-2"></i>
              {{ getAlertMessage(selectedQuiz) }}
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDetailsModal" data-bs-dismiss="modal">
              Close
            </button>
            <router-link 
              v-if="isQuizAvailable(selectedQuiz)" 
              :to="`/user/quiz/${selectedQuiz.id}`" 
              class="btn btn-success"
            >
              <i class="bi bi-play me-1"></i>Start Quiz
            </router-link>
          </div>
        </div>
      </div>
    </div>

  </div>

  <FootPage />
</template>

<script>
import NavPage from '@/components/NavBar.vue';
import FootPage from '@/components/FootPage.vue';

export default {
  name: "UserPage",
  components: {
    NavPage,
    FootPage
  },

  data() {
    return {
      search: "",
      quizzes: [],
      selectedQuiz: null,
      refreshInterval: null
    };
  },

  computed: {

    isAuthenticated() {
      return window.sessionStorage.getItem('isAuthenticated') === 'true';
    },
    user(){
      return JSON.parse(window.sessionStorage.getItem('user'));
    },
    // Available quizzes (currently open for attempts)
    availableQuizzes() {
      const now = new Date();
      return this.quizzes.filter(quiz => {
        // If not active, don't show
        if (!quiz.is_active) return false;
        
        // If no scheduling, quiz is always available
        if (!quiz.start_date && !quiz.end_date) {
          return true;
        }
        
        const startTime = quiz.start_date ? this.parseDateTime(quiz.start_date) : null;
        const endTime = quiz.end_date ? this.parseDateTime(quiz.end_date) : null;
        
        // Only start time set
        if (startTime && !endTime) {
          return now >= startTime;
        }
        
        // Only end time set
        if (!startTime && endTime) {
          return now <= endTime;
        }
        
        // Both times set
        if (startTime && endTime) {
          return now >= startTime && now <= endTime;
        }
        
        return false;
      }).filter(quiz => this.matchesSearch(quiz));
    },

    // Upcoming quizzes (not yet started)
    upcomingQuizzes() {
      const now = new Date();
      return this.quizzes.filter(quiz => {
        if (!quiz.is_active || !quiz.start_date) return false;
        const startTime = this.parseDateTime(quiz.start_date);
        return startTime > now;
      }).filter(quiz => this.matchesSearch(quiz));
    },

    // Expired quizzes (past end time)
    expiredQuizzes() {
      const now = new Date();
      return this.quizzes.filter(quiz => {
        if (!quiz.end_date) return false;
        const endTime = this.parseDateTime(quiz.end_date);
        return endTime < now;
      }).filter(quiz => this.matchesSearch(quiz));
    }
  },

  methods: {
    // Parse datetime from backend format "YYYY-MM-DD HH:MM:SS"
    parseDateTime(dateTimeString) {
      if (!dateTimeString) return null;
      // Convert "2025-07-25 14:30:00" to "2025-07-25T14:30:00"
      return new Date(dateTimeString.replace(' ', 'T'));
    },

    capitalize(str) {
      if (!str || typeof str !== "string") return "";
      return str.toString().charAt(0).toUpperCase() + str.slice(1);
    },

    // Search helper method
    matchesSearch(quiz) {
      if (!this.search.trim()) return true;
      const searchLower = this.search.toLowerCase();
      return quiz.title.toLowerCase().includes(searchLower) ||
             (quiz.description && quiz.description.toLowerCase().includes(searchLower));
    },

    // Check if quiz is currently available
    isQuizAvailable(quiz) {
      const now = new Date();
      
      // Not active means not available
      if (!quiz.is_active) return false;
      
      // No scheduling means always available
      if (!quiz.start_date && !quiz.end_date) {
        return true;
      }
      
      const startTime = quiz.start_date ? this.parseDateTime(quiz.start_date) : null;
      const endTime = quiz.end_date ? this.parseDateTime(quiz.end_date) : null;
      
      if (startTime && !endTime) {
        return now >= startTime;
      }
      
      if (!startTime && endTime) {
        return now <= endTime;
      }
      
      if (startTime && endTime) {
        return now >= startTime && now <= endTime;
      }
      
      return false;
    },

    // Get quiz status
    getQuizStatus(quiz) {
      if (!quiz.is_active) {
        return 'Inactive';
      }
      
      if (this.isQuizAvailable(quiz)) {
        return 'Available Now';
      } else if (quiz.start_date && this.parseDateTime(quiz.start_date) > new Date()) {
        return 'Upcoming';
      } else if (quiz.end_date && this.parseDateTime(quiz.end_date) < new Date()) {
        return 'Expired';
      }
      return 'Not Scheduled';
    },

    // Format datetime for display
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return 'Not set';
      return this.parseDateTime(dateTimeString).toLocaleString();
    },

    // Get time remaining until end
    getTimeRemaining(endDateTime) {
      if (!endDateTime) return 'No limit';
      
      const now = new Date();
      const end = this.parseDateTime(endDateTime);
      const diff = end - now;
      
      if (diff <= 0) return 'Expired';
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      
      if (days > 0) {
        return `${days}d ${hours}h`;
      } else if (hours > 0) {
        return `${hours}h ${minutes}m`;
      } else {
        return `${minutes}m`;
      }
    },

    // Get time until quiz starts
    getTimeUntilStart(startDateTime) {
      if (!startDateTime) return 'Not set';
      
      const now = new Date();
      const start = this.parseDateTime(startDateTime);
      const diff = start - now;
      
      if (diff <= 0) return 'Started';
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      
      if (days > 0) {
        return `${days}d ${hours}h`;
      } else if (hours > 0) {
        return `${hours}h ${minutes}m`;
      } else {
        return `${minutes}m`;
      }
    },

    // Get time since quiz expired
    getTimeSinceExpiry(endDateTime) {
      if (!endDateTime) return 'Unknown';
      
      const now = new Date();
      const end = this.parseDateTime(endDateTime);
      const diff = now - end;
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      
      if (days > 0) {
        return `${days}d ${hours}h`;
      } else if (hours > 0) {
        return `${hours}h ${minutes}m`;
      } else {
        return `${minutes}m`;
      }
    },

    // Get CSS class for time remaining
    getTimeRemainingClass(quiz) {
      if (!quiz.end_date) return 'text-success';
      
      const now = new Date();
      const end = this.parseDateTime(quiz.end_date);
      const diff = end - now;
      const hours = diff / (1000 * 60 * 60);
      
      if (hours <= 1) return 'text-danger fw-bold';
      if (hours <= 6) return 'text-warning fw-bold';
      return 'text-success';
    },

    // Get status badge class
    getStatusBadgeClass(quiz) {
      const status = this.getQuizStatus(quiz);
      switch (status) {
        case 'Available Now': return 'badge bg-success';
        case 'Upcoming': return 'badge bg-warning text-dark';
        case 'Expired': return 'badge bg-danger';
        case 'Inactive': return 'badge bg-secondary';
        default: return 'badge bg-secondary';
      }
    },

    // Get modal header class
    getModalHeaderClass(quiz) {
      const status = this.getQuizStatus(quiz);
      switch (status) {
        case 'Available Now': return 'bg-success';
        case 'Upcoming': return 'bg-warning';
        case 'Expired': return 'bg-danger';
        case 'Inactive': return 'bg-secondary';
        default: return 'bg-dark';
      }
    },

    // Get alert class for modal
    getAlertClass(quiz) {
      const status = this.getQuizStatus(quiz);
      switch (status) {
        case 'Available Now': return 'alert-success';
        case 'Upcoming': return 'alert-warning';
        case 'Expired': return 'alert-danger';
        case 'Inactive': return 'alert-secondary';
        default: return 'alert-info';
      }
    },

    // Get alert icon
    getAlertIcon(quiz) {
      const status = this.getQuizStatus(quiz);
      switch (status) {
        case 'Available Now': return 'bi bi-check-circle-fill';
        case 'Upcoming': return 'bi bi-clock-fill';
        case 'Expired': return 'bi bi-x-circle-fill';
        case 'Inactive': return 'bi bi-slash-circle-fill';
        default: return 'bi bi-info-circle-fill';
      }
    },

    // Get alert message
    getAlertMessage(quiz) {
      const status = this.getQuizStatus(quiz);
      switch (status) {
        case 'Available Now':
          if (quiz.end_date) {
            return `This quiz is currently available. Time remaining: ${this.getTimeRemaining(quiz.end_date)}`;
          }
          return 'This quiz is currently available with no time limit.';
        case 'Upcoming':
          return `This quiz will be available starting ${this.formatDateTime(quiz.start_date)}`;
        case 'Expired':
          return `This quiz expired on ${this.formatDateTime(quiz.end_date)}`;
        case 'Inactive':
          return 'This quiz is currently inactive and not available for attempts.';
        default:
          return 'Quiz schedule information is not available.';
      }
    },

    searchQuiz() {
      // Search is handled by computed properties
      if (this.search.trim()) {
        console.log(`Searching for: "${this.search}"`);
      }
    },

    async fetchQuizzes() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/quizzes", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch quizzes");
        }

        const data = await response.json();
        this.quizzes = data.quizzes || [];
        
        console.log("Fetched quizzes:", this.quizzes.length);
        console.log("Available:", this.availableQuizzes.length);
        console.log("Upcoming:", this.upcomingQuizzes.length);
        console.log("Expired:", this.expiredQuizzes.length);

      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    },

    openDetailsModal(quiz) {
      this.selectedQuiz = quiz;
      this.$nextTick(() => {
        const modal = new bootstrap.Modal(document.getElementById('quizDetailsModal'));
        modal.show();
      });
    },

    closeDetailsModal() {
      this.selectedQuiz = null;
      const modal = bootstrap.Modal.getInstance(document.getElementById('quizDetailsModal'));
      if (modal) modal.hide();
    }
  },

  mounted() {
    this.fetchQuizzes();
    
    // Auto-refresh every 60 seconds to update time remaining
    this.refreshInterval = setInterval(() => {
      this.fetchQuizzes();
    }, 60000);
  },

  beforeUnmount() {
    // Cleanup interval
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }
};
</script>

<style scoped>
</style>
