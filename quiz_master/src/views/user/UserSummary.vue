<template>

<div class="page-wrapper d-flex flex-column min-vh-100">
  <NavBar />
  <div class="container py-4">
    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading your dashboard...</p>
    </div>

    <!-- Main Dashboard Content -->
    <div v-else>
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
                <div v-if="!hasTimelineData" class="d-flex align-items-center justify-content-center h-100 text-muted">
                  <div class="text-center">
                    <i class="bi bi-graph-up fa-3x mb-3"></i>
                    <p>No performance data available yet</p>
                  </div>
                </div>
                <canvas v-else id="performanceTimelineChart"></canvas>
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
                <div v-if="!hasSubjectData" class="d-flex align-items-center justify-content-center h-100 text-muted">
                  <div class="text-center">
                    <i class="bi bi-pie-chart fa-3x mb-3"></i>
                    <p>No subject data available yet</p>
                  </div>
                </div>
                <canvas v-else id="subjectPerformanceChart"></canvas>
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
                <div v-if="recentAttempts.length === 0" class="text-center py-5 text-muted">
                  <i class="bi bi-journal-text fa-3x mb-3"></i>
                  <p>No quiz attempts yet</p>
                  <small>Start taking quizzes to see your performance here</small>
                </div>
                <table v-else class="table table-bordered table-hover">
                  <thead class="table-dark">
                    <tr>
                      <th>Quiz Title</th>
                      <th>Date</th>
                      <th>Score</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="attempt in recentAttempts" :key="attempt.attempt_id">
                      <td class="fw-bold">{{ attempt.quiz_title }}</td>
                      <td>{{ formatDate(attempt.date) }}</td>
                      <td>
                        <span class="fw-bold" :class="getScoreClass(attempt.score)">
                          {{ attempt.score }}%
                        </span>
                      </td>
                      <td>
                        <span v-if="attempt.score >= 60" class="badge bg-success">
                          <i class="bi bi-check-circle me-1"></i>Passed
                        </span>
                        <span v-else class="badge bg-danger">
                          <i class="bi bi-x-circle me-1"></i>Failed
                        </span>
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

    <!-- Error State -->
    <div v-if="hasError" class="alert alert-danger text-center">
      <i class="bi bi-exclamation-triangle fa-2x mb-3"></i>
      <h5>Failed to load dashboard data</h5>
      <p>Please try refreshing the page or contact support if the problem persists.</p>
      <button @click="fetchUserSummary" class="btn btn-outline-danger">
        <i class="bi bi-arrow-clockwise me-1"></i>Retry
      </button>
    </div>
  </div>

  <FootPage />

</div>

</template>

<script>
import Chart from 'chart.js/auto';

import NavBar from '@/components/NavBar.vue';
import FootPage from '@/components/FootPage.vue';

export default {
  name: 'userSummary',
  components: {
    NavBar,
    FootPage
  },
  data() {
    return {
      isLoading: true,
      hasError: false,
      summary: {
        quizzes_taken: 0,
        avg_score: 0,
        upcoming_quizzes: 0,
        pass_rate: 0
      },
      recentAttempts: [],
      subjectPerformance: [],
      timelineChart: null,
      subjectChart: null
    }
  },
  computed: {
    hasTimelineData() {
      return this.recentAttempts && this.recentAttempts.length > 0;
    },
    hasSubjectData() {
      return this.subjectPerformance && this.subjectPerformance.length > 0;
    }
  },
  methods: {
    async fetchUserSummary() {
      this.isLoading = true;
      this.hasError = false;

      try {
        const token = window.sessionStorage.getItem('token');
        
        if (!token) {
          throw new Error('No authentication token found');
        }

        const response = await fetch('http://127.0.0.1:5000/api/summary', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Validate and set data with fallbacks
        this.summary = {
          quizzes_taken: data.summary?.quizzes_taken || 0,
          avg_score: data.summary?.avg_score || 0,
          upcoming_quizzes: data.summary?.upcoming_quizzes || 0,
          pass_rate: data.summary?.pass_rate || 0
        };
        
        this.recentAttempts = Array.isArray(data.recent_attempts) ? data.recent_attempts : [];
        this.subjectPerformance = Array.isArray(data.subject_performance) ? data.subject_performance : [];
        
        // Create charts after data is loaded and DOM is updated
        this.$nextTick(() => {
          setTimeout(() => {
            this.createCharts();
          }, 100);
        });

      } catch (error) {
        console.error('Error fetching user summary:', error);
        this.hasError = true;
      } finally {
        this.isLoading = false;
      }
    },

    createCharts() {
      try {
        this.createPerformanceTimelineChart();
      } catch (error) {
        console.error('Error creating timeline chart:', error);
      }
      
      try {
        this.createSubjectPerformanceChart();
      } catch (error) {
        console.error('Error creating subject chart:', error);
      }
    },

    createPerformanceTimelineChart() {
      const ctx = document.getElementById('performanceTimelineChart');
      if (!ctx) {
        console.warn('Canvas element performanceTimelineChart not found');
        return;
      }

      // Destroy existing chart if it exists
      if (this.timelineChart) {
        this.timelineChart.destroy();
        this.timelineChart = null;
      }

      // Validate data availability
      if (!this.hasTimelineData) {
        console.log('No recent attempts data available for timeline chart');
        return;
      }

      // Extract and validate data
      const timelineData = this.recentAttempts
        .filter(attempt => attempt.date && attempt.score !== undefined && attempt.score !== null)
        .map(attempt => ({
          date: attempt.date,
          score: parseFloat(attempt.score) || 0
        }))
        .reverse(); // Show chronological order

      if (timelineData.length === 0) {
        console.log('No valid data for timeline chart after filtering');
        return;
      }

      const timelineLabels = timelineData.map(item => item.date);
      const timelineScores = timelineData.map(item => item.score);

      this.timelineChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
          labels: timelineLabels,
          datasets: [{
            label: 'Quiz Scores',
            data: timelineScores,
            backgroundColor: 'rgba(78, 115, 223, 0.05)',
            borderColor: 'rgba(78, 115, 223, 1)',
            tension: 0.3,
            fill: true,
            borderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: 'rgba(78, 115, 223, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(78, 115, 223, 1)',
            hidden: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            intersect: false,
            mode: 'index'
          },
          plugins: {
            legend: {
              display: true,
              position: 'bottom'
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  return `Score: ${context.parsed.y}%`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              display: true,
              title: {
                display: true,
                text: 'Score (%)'
              },
              ticks: {
                stepSize: 10
              }
            },
            x: {
              display: true,
              title: {
                display: true,
                text: 'Date'
              }
            }
          }
        }
      });
    },

    createSubjectPerformanceChart() {
      const ctx = document.getElementById('subjectPerformanceChart');
      if (!ctx) {
        console.warn('Canvas element subjectPerformanceChart not found');
        return;
      }

      // Destroy existing chart if it exists
      if (this.subjectChart) {
        this.subjectChart.destroy();
        this.subjectChart = null;
      }

      // Validate data availability
      if (!this.hasSubjectData) {
        console.log('No subject performance data available');
        return;
      }

      // Extract and validate data
      const validSubjectData = this.subjectPerformance.filter(item => 
        item.subject && 
        item.avg_score !== undefined && 
        item.avg_score !== null
      );

      if (validSubjectData.length === 0) {
        console.log('No valid subject data for radar chart after filtering');
        return;
      }

      const subjectNames = validSubjectData.map(item => item.subject);
      const subjectScores = validSubjectData.map(item => parseFloat(item.avg_score) || 0);

      this.subjectChart = new Chart(ctx.getContext('2d'), {
        type: 'radar',
        data: {
          labels: subjectNames,
          datasets: [{
            label: 'Average Performance',
            data: subjectScores,
            backgroundColor: 'rgba(78, 115, 223, 0.2)',
            borderColor: 'rgba(78, 115, 223, 1)',
            pointBackgroundColor: 'rgba(78, 115, 223, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(78, 115, 223, 1)',
            borderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            hidden: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            intersect: false
          },
          plugins: {
            legend: {
              display: true,
              position: 'bottom'
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  return `${context.dataset.label}: ${context.parsed.r}%`;
                }
              }
            }
          },
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              min: 0,
              display: true,
              ticks: {
                stepSize: 20,
                callback: function(value) {
                  return value + '%';
                }
              },
              grid: {
                color: 'rgba(0, 0, 0, 0.1)'
              },
              angleLines: {
                color: 'rgba(0, 0, 0, 0.1)'
              }
            }
          }
        }
      });
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        });
      } catch (error) {
        return dateString;
      }
    },

    getScoreClass(score) {
      const numScore = parseFloat(score) || 0;
      if (numScore >= 80) return 'text-success';
      if (numScore >= 60) return 'text-warning';
      return 'text-danger';
    }
  },
  
  mounted() {
    this.fetchUserSummary();
  },

  beforeUnmount() {
    // Cleanup charts when component is destroyed
    if (this.timelineChart) {
      this.timelineChart.destroy();
      this.timelineChart = null;
    }
    if (this.subjectChart) {
      this.subjectChart.destroy();
      this.subjectChart = null;
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

.fa-3x {
  font-size: 3rem;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.075);
}

.card-header {
  border-radius: 0.375rem 0.375rem 0 0 !important;
}

.badge {
  font-size: 0.75em;
}

.btn-outline-danger:hover {
  color: #fff;
  background-color: #dc3545;
  border-color: #dc3545;
}

/* Animation for loading */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fadeIn 0.5s ease-in-out;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .fa-2x {
    font-size: 1.5rem;
  }
  
  .fa-3x {
    font-size: 2rem;
  }
  
  .h5 {
    font-size: 1rem;
  }
}
</style>
