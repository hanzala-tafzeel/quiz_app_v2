<template>

    <NavBar />
  <div class="container py-5 ">
    <div class="row justify-content-center align-items-center p-0">
      <div class="col-12 col-md-6 col-lg-5">
        <div class="bg-white shadow-lg rounded-3 p-4 p-md-5">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted">Loading profile...</p>
          </div>

          <!-- Error State -->
          <div v-if="error" class="alert alert-danger d-flex justify-content-between align-items-center">
            <span>{{ error }}</span>
            <button @click="fetchUserProfile" class="btn btn-outline-danger btn-sm">Retry</button>
          </div>

          <!-- Profile Content -->
          <div v-if="!loading && !error && currentUser">
            <!-- Profile Header -->
            <div class="text-center mb-4">
              <div class="bg-dark text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                <i class="bi bi-person-fill" style="font-size: 2.5rem;"></i>
              </div>
              <h2 class="mb-0">Account Details</h2>
            </div>

            <!-- Profile Information -->
            <div class="list-group list-group-flush">
              <!-- Username Section -->
              <div class="list-group-item border-0 px-0 py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <small class="text-muted d-block">Username</small>
                    <strong>{{ currentUser.username }}</strong>
                  </div>
                  <button @click="openEditModal" class="btn btn-outline-dark btn-sm">
                    <i class="bi bi-pencil-square"></i> Edit
                  </button>
                </div>
              </div>

              <!-- Email Section -->
              <div class="list-group-item border-0 px-0 py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <small class="text-muted d-block">Email Address</small>
                    <strong>{{ currentUser.email }}</strong>
                  </div>
                  <span class="badge bg-secondary">Read Only</span>
                </div>
              </div>

              <!-- Phone Section -->
              <div class="list-group-item border-0 px-0 py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <small class="text-muted d-block">Phone Number</small>
                    <strong>{{ currentUser.phone || 'Not provided' }}</strong>
                  </div>
                  <button @click="openEditModal" class="btn btn-outline-dark btn-sm">
                    <i class="bi bi-pencil-square"></i> Edit
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="showEditModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form @submit.prevent="updateProfile">
            <div class="modal-header">
              <h5 class="modal-title">Edit Profile</h5>
              <button @click="closeEditModal" type="button" class="btn-close" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input 
                  id="username"
                  v-model="editForm.username" 
                  type="text" 
                  class="form-control" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="phone" class="form-label">Phone Number</label>
                <input 
                  id="phone"
                  v-model="editForm.phone" 
                  type="tel" 
                  class="form-control"
                  placeholder="Enter phone number"
                >
              </div>
            </div>
            <div class="modal-footer">
              <button @click="closeEditModal" type="button" class="btn btn-outline-dark">Cancel</button>
              <button 
                type="submit" 
                class="btn btn-dark"
                :disabled="updating"
              >
                <span v-if="updating" class="spinner-border spinner-border-sm me-1"></span>
                {{ updating ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal Backdrop -->
    <div v-if="showEditModal" class="modal-backdrop fade show"></div>
  </div>

  <!-- Toast Notifications -->
  <div class="toast-container position-fixed top-0 end-0 p-3">
    <div v-if="message" :class="['toast', 'show', messageType === 'success' ? 'bg-success' : 'bg-danger']">
      <div class="toast-body text-white">
        {{ message }}
      </div>
    </div>
  </div>

  <div class="mt-5 mb-5">
    
  </div>
  <FootPage />
</template>

<script>
import FootPage from '@/components/FootPage.vue';
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'userProfile',
  components: {
    NavBar,
    FootPage
  },
  data() {
    return {
      currentUser: null,
      loading: false,
      error: null,
      showEditModal: false,
      updating: false,
      editForm: {
        username: '',
        phone: ''
      },
      message: '',
      messageType: 'success'
    }
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      this.loading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No authentication token found');
        }

        const response = await fetch('http://127.0.0.1:5000/api/user', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Session expired. Please login again.');
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const userData = await response.json();
        this.currentUser = userData;
      } catch (err) {
        this.error = err.message || 'Failed to fetch user profile. Please try again.';
        console.error('Error fetching user profile:', err);
      } finally {
        this.loading = false;
      }
    },

    openEditModal() {
      this.editForm = {
        username: this.currentUser.username,
        phone: this.currentUser.phone || ''
      };
      this.showEditModal = true;
    },

    closeEditModal() {
      this.showEditModal = false;
      this.editForm = {
        username: '',
        phone: ''
      };
    },

    async updateProfile() {
      this.updating = true;
      
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No authentication token found');
        }

        const response = await fetch('http://127.0.0.1:5000/api/user', {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.editForm.username,
            phone: this.editForm.phone
          })
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Session expired. Please login again.');
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update current user data
        this.currentUser = data.user;
        
        this.showMessage(data.message || 'Profile updated successfully!', 'success');
        this.closeEditModal();
        
      } catch (err) {
        this.showMessage(err.message || 'Failed to update profile. Please try again.', 'error');
        console.error('Error updating profile:', err);
      } finally {
        this.updating = false;
      }
    },

    showMessage(text, type) {
      this.message = text;
      this.messageType = type;
      setTimeout(() => {
        this.message = '';
      }, 5000);
    }
  }
}
</script>

<style scoped>
/* Minimal custom styles - Bootstrap handles most of the styling */
.modal.show {
  background: rgba(0,0,0,0.5);
}

.toast-container .toast {
  min-width: 250px;
}

/* Ensure Bootstrap Icons work if not already included */
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css");
</style>