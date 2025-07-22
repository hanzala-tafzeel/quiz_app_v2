<template>

  <NavPage/>


  <div class="container mt-2">
      <div class="row container">

    <div class="col-md-6">
      <h1 class="text-dark">Welcome, {{ currentUser }}</h1>
    </div>
    <div class="col-md-6">
      <form @submit.prevent="searchQuiz" class="float-end">
        <div class="input-group mb-3">
          <input
            v-model="search"
            type="text"
            class="form-control"
            placeholder="Search Quiz"
          />
          <button class="btn btn-dark" type="submit">Search</button>
        </div>
      </form>
    </div>
  </div>
    
    

    <!-- Upcoming Quizzes -->
    <div class="card mb-4">
      <div class="card-header bg-dark text-white">
        <h5 class="card-title mb-0">Upcoming Quizzes</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Quiz Title</th>
                <th>Date</th>
                <th>Duration(Min)</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(quiz, index) in upcomingQuizzes" :key="quiz.id">
                <td>{{ index + 1 }}</td>
                <td>{{ quiz.title }}</td>
                <td>{{ quiz.schedule_date }}</td>
                <td>{{ quiz.duration }}</td>
                <td>
                  <!-- <button class="btn btn-dark" @click="openDetailsModal(quiz)">
                    View
                  </button>
                  <button
                    class="btn btn-outline-dark"
                    @click="openUnavailableModal(quiz)"
                  >
                    Start
                  </button> -->
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- All Quizzes -->
    <div class="card mb-4">
      <div class="card-header bg-dark text-white">
        <h5 class="card-title mb-0">All Quizzes</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Quiz Title</th>
                <th>Date</th>
                <th>Duration(Min)</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(quiz, index) in quizzes" :key="quiz.id">
                <td>{{ index + 1 }}</td>
                <td>{{ quiz.title }}</td>
                <td>{{ quiz.schedule_date }}</td>
                <td>{{ quiz.duration }}</td>
                <td>
                <button class="btn btn-dark" @click="openDetailsModal(quiz)">
                  View
                </button>

                  <button
                    v-if="quiz.schedule_date > today"
                    class="btn btn-outline-dark"
                    @click="openUnavailableModal(quiz)"
                  >
                    Start
                  </button>
                  <router-link
                    v-else
                    :to="`/user/quiz/${quiz.id}`"
                    class="btn btn-outline-dark mx-2"
                  >
                    Start
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- modal for quiz details -->
    <!-- Modal for quiz details: single, bound to selectedQuiz -->
    <div
      class="modal fade"
      id="quizDetailsModal"
      tabindex="-1"
      aria-labelledby="quizDetailsModalLabel"
      aria-hidden="true"
      ref="quizModal"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content" v-if="selectedQuiz">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title" id="quizDetailsModalLabel">Quiz Details</h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              data-bs-dismiss="modal"
              aria-label="Close"
              @click="closeDetailsModal"
            ></button>
          </div>
          <div class="modal-body">
            <h4 class="fw-bold mb-4">
              Quiz Title:
              <span class="text-secondary">{{ selectedQuiz.title }}</span>
            </h4>
            <div class="mb-3">
              <p class="mb-1">
                <strong>Date:</strong>
                <span class="text-muted">{{ selectedQuiz.created_at }}</span>
              </p>
              <p class="mb-1">
                <strong>Duration:</strong>
                <span class="text-muted"
                  >{{ selectedQuiz.duration }} minutes</span
                >
              </p>
              <p class="mb-1">
                <strong>Description:</strong>
                <span class="text-muted">{{ selectedQuiz.description }}</span>
              </p>
              <p class="mb-1">
                <strong>Total Marks:</strong>
                <span class="text-muted">{{ selectedQuiz.total_marks }}</span>
              </p>
              <p class="mb-1">
                <strong>Passing Marks:</strong>
                <span class="text-muted">{{ selectedQuiz.pass_marks }}</span>
              </p>
            </div>
            <div class="alert alert-info mt-4">
              <i class="bi bi-info-circle-fill me-2"></i>
              Make sure to complete the quiz within the given duration.
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeDetailsModal"
              data-bs-dismiss="modal"
            >
              Close
            </button>
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
  name: "UserPage",
  components:{
    NavPage,
    FootPage
  },

  data() {
    return {
      currentUser: "Hanzala",
      search: "",
      quizzes: [], // local copy if you want (optional)
      upcomingQuizzes: [],
      selectedQuiz: null, 
    };
  },

  methods: {
    async fetchQuizzes() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/quizzes", {
          // adjust URL
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // optionally add Authorization header if needed
            // 'Authorization': `Bearer ${this.$store.state.token}`
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch quizzes");
        }

        const data = await response.json();

        // Commit quizzes to Vuex
        this.$store.commit("SET_QUIZZES", data.quizzes || []);

        // Optionally update local quizzes copy
        this.quizzes = data.quizzes || [];

        // You can add filtering for upcomingQuizzes here if needed
        const now = new Date();
        this.upcomingQuizzes = this.quizzes.filter((q) => {
          if (!q.schedule_date) return false;
          return new Date(q.schedule_date) > now;
        });
      } catch (error) {
        console.error("Error fetching quizzes:", error);
        // optionally show user message here
      }
    },

      openDetailsModal(quiz) {          // <-- Added
    this.selectedQuiz = quiz;
    // Show the modal using Bootstrap's JS
    // Wait for nextTick if needed
    this.$nextTick(() => {
      const modal = new bootstrap.Modal(document.getElementById('quizDetailsModal'));
      modal.show();
    });
  },
  closeDetailsModal() {            // <-- Added for nice UX
    this.selectedQuiz = null;
    const modal = bootstrap.Modal.getInstance(document.getElementById('quizDetailsModal'));
    if (modal) modal.hide();
  }
  },

  mounted() {
    this.fetchQuizzes(); // fetch quizzes when component mounts
  },
};
</script>

<style></style>
