<template>
  <div>
    <AdminNavBar />

  <div class="container py-4">
    <div class="row">
      <!-- Overview Cards -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Total Users</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.total_users }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Total Quizzes</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.total_quizzes }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Total Subjects</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.total_subjects }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-warning shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Total Attempts</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.total_attempts }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="row">
      <!-- Subject Performance Chart -->
      <div class="col-xl-6 col-lg-6">
        <div class="card shadow mb-4 chart-card">
          <div class="card-header py-3 bg-dark">
            <h6 class="m-0 font-weight-bold text-white">Subject Performance Overview</h6>
          </div>
          <div class="card-body">
            <canvas id="subjectPerformanceChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Subject Popularity Pie Chart -->
      <div class="col-xl-6 col-lg-6">
        <div class="card shadow mb-4 chart-card" >
          <div class="card-header py-3 bg-dark">
            <h6 class="m-0 font-weight-bold text-white">Subject Popularity</h6>
          </div>
          <div class="card-body" style="height: 325px;">
            <canvas id="subjectPopularity"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- Top Performers by Quiz -->
    <div class="row">
      <div class="col-12">
        <div class="card shadow mb-4">
          <div class="card-header py-3 bg-dark">
            <h6 class="m-0 font-weight-bold text-white">Top Performers by Quiz</h6>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Quiz</th>
                    <th>User</th>
                    <th>Marks</th>
                  </tr>
                </thead>
                <tbody>
                  <!-- CONVERTED: Vue.js loop for top performers -->
                  <template v-for="quiz in topPerformers" :key="quiz.quiz_title">
                    <tr v-for="performer in quiz.performers" :key="`${quiz.quiz_title}-${performer.username}`">
                      <td>{{ quiz.quiz_title }}</td>
                      <td>{{ performer.username }}</td>
                      <td>{{ performer.score }}</td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity Table -->
    <div class="row">
      <div class="col-12">
        <div class="card shadow mb-4">
          <div class="card-header py-3 bg-dark">
            <h6 class="m-0 font-weight-bold text-white">Recent Quiz Attempts</h6>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>User</th>
                    <th>Quiz</th>
                    <th>Score</th>
                    <th>Time</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <!-- CONVERTED: Vue.js loop for recent attempts -->
                  <tr v-for="attempt in attemptsToday" :key="`${attempt.user}-${attempt.time}`">
                    <td>{{ attempt.user }}</td>
                    <td>{{ attempt.quiz_title }}</td>
                    <td>{{ attempt.score }}</td>
                    <td>{{ attempt.time }}</td>
                    <td>
                      <!-- CONVERTED: Vue.js conditional rendering -->
                      <span v-if="attempt.completed" class="badge bg-success">Completed</span>
                      <span v-else class="badge bg-warning">In Progress</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


    <FootPage />
  </div>
</template>

<script>
// ADDED: Import Chart.js
// import Chart from 'chart.js/auto';
import AdminNavBar from '@/components/AdminNavBar.vue';
import FootPage from '@/components/FootPage.vue';

export default {
  name: 'adminsummary',
  components: {
    AdminNavBar,
    FootPage
  },
  data() {
    return {
      // ADDED: New data properties for API response
      stats: {
        total_users: 0,
        total_quizzes: 0,
        active_quizzes: 0,
        total_subjects: 0,
        total_attempts: 0
      },
      attemptsToday: [],
      subjectPerformance: [],
      attemptDistribution: [],
      topPerformers: [],
      message: "",
      category: ""
    }
  },
  methods: {
     //Method to fetch dashboard data
    async fetchDashboardData() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch('http://127.0.0.1:5000/api/admin/summary', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.stats = data.stats;
          this.attemptsToday = data.attempts_today;
          this.subjectPerformance = data.subject_performance;
          this.attemptDistribution = data.attempt_distribution;
          this.topPerformers = data.top_performers;
          console.log('Dashboard data fetched successfully:', data);
          
          // Create charts after data is loaded
          this.$nextTick(() => {
            this.createCharts();
          });
        } else {
          console.error('Failed to fetch dashboard data');
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    },

     createCharts() {
    this.createSubjectPerformanceChart();
    this.createSubjectPopularityChart(); // FIXED: Changed method name to match
  },

  createSubjectPerformanceChart() {
    const ctx = document.getElementById('subjectPerformanceChart');
    // ADDED: Check if element exists before getting context
    if (!ctx) {
      console.error('Canvas element subjectPerformanceChart not found');
      return;
    }
    
    new Chart(ctx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: this.subjectPerformance.map(item => item.subject),
        datasets: [{
          label: 'Average Score (%)',
          data: this.subjectPerformance.map(item => item.avg_score),
          backgroundColor: 'rgba(54, 162, 235, 0.8)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  },

  // FIXED: Changed method name and canvas ID to match template
  createSubjectPopularityChart() {
    const ctx = document.getElementById('subjectPopularity');
    // ADDED: Check if element exists before getting context
    if (!ctx) {
      console.error('Canvas element subjectPopularity not found');
      return;
    }
    
    new Chart(ctx.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: this.attemptDistribution.map(item => item.subject),
        datasets: [{
          data: this.attemptDistribution.map(item => item.count),
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#4BC0C0',
            '#9966FF',
            '#FF9F40'
          ]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });
  },

  // ADDED: Enhanced data fetching with better error handling
  async fetchDashboardData() {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch('http://127.0.0.1:5000/api/admin/summary', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        this.stats = data.stats;
        this.attemptsToday = data.attempts_today;
        this.subjectPerformance = data.subject_performance;
        this.attemptDistribution = data.attempt_distribution;
        this.topPerformers = data.top_performers;
        
        // IMPROVED: Wait for DOM update and add delay for safety
        this.$nextTick(() => {
          setTimeout(() => {
            this.createCharts();
          }, 100);
        });
      } else {
        console.error('Failed to fetch dashboard data');
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  }
  },
  
  // ADDED: Fetch data when component mounts
  mounted() {
    this.fetchDashboardData();
  }
}
</script>

<style scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}
.chart-card {
  height: 400px; /* Fixed total height */
}

.fs-2 {
  font-size: 1.75rem;
}

.table th {
  border-top: none;
  font-weight: 600;
}
</style>
