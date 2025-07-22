<template>

    <NavBar />
  <div class="container py-4">
    <!-- User Stats Cards -->
    <div class="row">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Quizzes Taken</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ summary.quizzes_taken }}</div>
              </div>
              <div class="col-auto">
                <i class="bi bi-check-circle fa-2x text-gray-300"></i>
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
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Average Score</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ summary.avg_score }}%</div>
              </div>
              <div class="col-auto">
                <i class="bi bi-percent fa-2x text-gray-300"></i>
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
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Upcoming Quizzes</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ summary.upcoming_quizzes }}</div>
              </div>
              <div class="col-auto">
                <i class="bi bi-calendar-event fa-2x text-gray-300"></i>
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
                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Pass Rate</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ summary.pass_rate }}%</div>
              </div>
              <div class="col-auto">
                <i class="bi bi-trophy fa-2x"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="row">
      <!-- Performance Timeline -->
      <div class="col-xl-8 col-lg-7">
        <div class="card shadow mb-4">
          <div class="card-header py-3 bg-dark">
            <h6 class="m-0 font-weight-bold text-white">Your Performance Timeline</h6>
          </div>
          <div class="card-body">
            <div class="chart-area" style="min-height: 303px;">
              <canvas id="performanceTimelineChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Subject-wise Performance -->
      <div class="col-xl-4 col-lg-5">
        <div class="card shadow mb-4">
          <div class="card-header py-3 bg-dark">
            <h6 class="m-0 font-weight-bold text-white">Subject-wise Performance</h6>
          </div>
          <div class="card-body">
            <div class="chart-pie" style="min-height: 303px;">
              <canvas id="subjectPerformanceChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Quizzes Table -->
    <div class="row">
      <div class="col-12">
        <div class="card shadow mb-4">
          <div class="card-header py-3 bg-dark">
            <h6 class="m-0 font-weight-bold text-white">Recent Quiz Attempts</h6>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <!-- CONVERTED: Show message when no attempts -->
              <div v-if="recentAttempts.length === 0" class="text-center py-3 text-muted">
                No quiz attempts yet
              </div>
              <table v-else class="table table-bordered">
                <thead>
                  <tr>
                    <th>Quiz Title</th>
                    <th>Date</th>
                    <th>Score</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <!-- CONVERTED: Vue.js loop for recent attempts -->
                  <tr v-for="attempt in recentAttempts" :key="attempt.attempt_id">
                    <td>{{ attempt.quiz_title }}</td>
                    <td>{{ attempt.date }}</td>
                    <td>{{ attempt.score }}%</td>
                    <td>
                      <!-- CONVERTED: Vue.js conditional rendering -->
                      <span v-if="attempt.score >= 60" class="badge bg-success">Passed</span>
                      <span v-else class="badge bg-danger">Failed</span>
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
</template>

<script>

import NavBar from '@/components/NavBar.vue';
import FootPage from '@/components/FootPage.vue';

export default {
  name: 'userSummary',
  components:{
    NavBar,
    FootPage
  },
  data() {
    return {
      // CONVERTED: Data properties for API response
      summary: {
        quizzes_taken: 0,
        avg_score: 0,
        upcoming_quizzes: 0,
        pass_rate: 0
      },
      recentAttempts: [],
      subjectPerformance: [],
      // Chart instances
      timelineChart: null,
      subjectChart: null
    }
  },
  methods: {
  
    async fetchUserSummary() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch('http://127.0.0.1:5000/api/summary', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.summary = data.summary;
          this.recentAttempts = data.recent_attempts;
          this.subjectPerformance = data.subject_performance;
          
          // Create charts after data is loaded
          this.$nextTick(() => {
            setTimeout(() => {
              this.createCharts();
            }, 100);
          });
        } else {
          console.error('Failed to fetch user summary');
        }
      } catch (error) {
        console.error('Error fetching user summary:', error);
      }
    },

    // CONVERTED: Method to create Chart.js charts
    createCharts() {
      this.createPerformanceTimelineChart();
      this.createSubjectPerformanceChart();
    },

    // CONVERTED: Performance Timeline Line Chart
    createPerformanceTimelineChart() {
      const ctx = document.getElementById('performanceTimelineChart');
      if (!ctx) {
        console.error('Canvas element performanceTimelineChart not found');
        return;
      }

      // Destroy existing chart if it exists
      if (this.timelineChart) {
        this.timelineChart.destroy();
      }

      // Extract timeline data from recent attempts
      const timelineLabels = this.recentAttempts.map(attempt => attempt.date);
      const timelineScores = this.recentAttempts.map(attempt => attempt.score);

      this.timelineChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
          labels: timelineLabels.reverse(), // Show chronological order
          datasets: [{
            label: 'Quiz Scores',
            data: timelineScores.reverse(),
            backgroundColor: 'rgba(78, 115, 223, 0.05)',
            borderColor: 'rgba(78, 115, 223, 1)',
            tension: 0.3,
            fill: true
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

    // CONVERTED: Subject Performance Radar Chart
    createSubjectPerformanceChart() {
      const ctx = document.getElementById('subjectPerformanceChart');
      if (!ctx) {
        console.error('Canvas element subjectPerformanceChart not found');
        return;
      }

      // Destroy existing chart if it exists
      if (this.subjectChart) {
        this.subjectChart.destroy();
      }

      // Extract subject data
      const subjectNames = this.subjectPerformance.map(item => item.subject);
      const subjectScores = this.subjectPerformance.map(item => item.avg_score);

      this.subjectChart = new Chart(ctx.getContext('2d'), {
        type: 'radar',
        data: {
          labels: subjectNames,
          datasets: [{
            label: 'Your Performance',
            data: subjectScores,
            backgroundColor: 'rgba(78, 115, 223, 0.2)',
            borderColor: 'rgba(78, 115, 223, 1)',
            pointBackgroundColor: 'rgba(78, 115, 223, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(78, 115, 223, 1)'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              ticks: {
                stepSize: 20
              }
            }
          },
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      });
    }
  },
  
  // CONVERTED: Fetch data when component mounts
  mounted() {
    this.fetchUserSummary();
  },

  // CONVERTED: Cleanup charts when component is destroyed
  beforeUnmount() {
    if (this.timelineChart) {
      this.timelineChart.destroy();
    }
    if (this.subjectChart) {
      this.subjectChart.destroy();
    }
  }
}
</script>

<style scoped>
.border-left-primary {
  border-left: 4px solid #007bff !important;
}

.border-left-success {
  border-left: 4px solid #28a745 !important;
}

.border-left-info {
  border-left: 4px solid #17a2b8 !important;
}

.border-left-warning {
  border-left: 4px solid #ffc107 !important;
}

.text-gray-800 {
  color: #5a5c69 !important;
}

.text-gray-300 {
  color: #dddfeb !important;
}

.text-xs {
  font-size: 0.75rem;
}

.shadow {
  box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
}

.no-gutters {
  margin-right: 0;
  margin-left: 0;
}

.no-gutters > .col {
  padding-right: 0;
  padding-left: 0;
}

.fa-2x {
  font-size: 2rem;
}
</style>
