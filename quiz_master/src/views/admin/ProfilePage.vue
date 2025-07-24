<template>
 <div class="page-wrapper d-flex flex-column min-vh-100">
    <AdminNavBar/>
  <div class="container py-4">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col">
        <h1 class="h2 text-dark mb-0">User Management</h1>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row ">
      <div class="col-md-4 mb-3">
        <div class="card text-center">
          <div class="card-body">
            <h6 class="card-title text-muted text-uppercase">Total Users</h6>
            <h2 class="card-text text-primary mb-0">{{ users.length }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-center">
          <div class="card-body">
            <h6 class="card-title text-muted text-uppercase">Active Users</h6>
            <h2 class="card-text text-success mb-0">{{ activeUsersCount }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-center">
          <div class="card-body">
            <h6 class="card-title text-muted text-uppercase">Inactive Users</h6>
            <h2 class="card-text text-danger mb-0">{{ inactiveUsersCount }}</h2>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary mb-3" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-muted">Loading users...</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="alert alert-danger d-flex justify-content-between align-items-center">
      <span>{{ error }}</span>
      <button @click="fetchUsers" class="btn btn-outline-danger btn-sm">Retry</button>
    </div>

    <!-- Users Table -->
    <div v-if="!loading && !error" class="card">
      <div class="card-header d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center bg-dark text-white">
        <h5 class="card-title mb-2 mb-md-0 ">Users</h5>
        <div class="d-flex flex-column flex-md-row gap-2">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search users..." 
            class="form-control form-control-sm"
            style="width: 200px;"
          >
          <select v-model="statusFilter" class="form-select form-select-sm" style="width: 150px;">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </div>

      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Username</th>
                <th scope="col">Phone</th>
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td class="fw-semibold">{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.phone || 'N/A' }}</td>
                <td>
                  <span 
                    :class="['badge', user.is_active ? 'bg-success' : 'bg-danger']"
                  >
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="btn-group btn-group-sm">
                    <button 
                      @click="editUser(user)" 
                      class="btn btn-outline-primary"
                      :disabled="updatingUserId === user.id"
                    >
                      <span v-if="updatingUserId === user.id" class="spinner-border spinner-border-sm me-1"></span>
                        <i class="bi bi-pencil-fill"></i>
                      Edit
                    </button>
                    <button 
                      @click="confirmDeleteUser(user)" 
                      class="btn btn-outline-danger"
                      :disabled="deletingUserId === user.id"
                    >
                      <span v-if="deletingUserId === user.id" class="spinner-border spinner-border-sm me-1"></span>
                        <i class="bi bi-trash-fill"></i>
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="filteredUsers.length === 0" class="text-center py-5">
          <div class="text-muted">
            <i class="fas fa-users fa-3x mb-3"></i>
            <p class="mb-0">No users found matching your criteria.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Edit User</h5>
            <button @click="closeEditModal" type="button" class="btn-close btn-close-white"></button>
          </div>
          <form @submit.prevent="updateUser">
            <div class="modal-body">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input 
                  id="username"
                  v-model="editForm.username" 
                  type="text" 
                  required 
                  class="form-control"
                >
              </div>
              <div class="mb-3">
                <label for="phone" class="form-label">Phone</label>
                <input 
                  id="phone"
                  v-model="editForm.phone" 
                  type="tel" 
                  class="form-control"
                >
              </div>
              <div class="form-check">
                <input 
                  v-model="editForm.is_active" 
                  type="checkbox" 
                  id="is_active"
                  class="form-check-input"
                >
                <label for="is_active" class="form-check-label">
                  Active User
                </label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" @click="closeEditModal" class="btn btn-secondary">
                Cancel
              </button>
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="updatingUserId === editForm.id"
              >
                <span v-if="updatingUserId === editForm.id" class="spinner-border spinner-border-sm me-1"></span>
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-sm modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Confirm Delete</h5>
            <button @click="closeDeleteModal" type="button" class="btn-close btn-close-white"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete user <strong>{{ userToDelete?.username }}</strong>?</p>
            <p class="text-danger small mb-0">This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button @click="closeDeleteModal" class="btn btn-secondary">Cancel</button>
            <button 
              @click="deleteUser" 
              class="btn btn-danger"
              :disabled="deletingUserId === userToDelete?.id"
            >
              <span v-if="deletingUserId === userToDelete?.id" class="spinner-border spinner-border-sm me-1"></span>
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Backdrop -->
    <div v-if="showEditModal || showDeleteModal" class="modal-backdrop fade show"></div>
  </div>

  <!-- Toast Notifications -->
  <div class="toast-container position-fixed top-0 end-0 p-3">
    <div v-if="message" :class="['toast', 'show', messageType === 'success' ? 'bg-success' : 'bg-danger']">
      <div class="toast-body text-white">
        {{ message }}
      </div>
    </div>
  </div>

  <FootPage/>

</div>
</template>

<script>
import AdminNavBar from '@/components/AdminNavBar.vue';
import FootPage from '@/components/FootPage.vue';

export default {
  name: 'AdminUsersPage',
  components:{
    AdminNavBar,
    FootPage
  },    
  data() {
    return {
      users: [],
      loading: false,
      error: null,
      searchQuery: '',
      statusFilter: '',
      showEditModal: false,
      showDeleteModal: false,
      editForm: {
        id: null,
        username: '',
        phone: '',
        is_active: true
      },
      userToDelete: null,
      updatingUserId: null,
      deletingUserId: null,
      message: '',
      messageType: 'success'
    }
  },
  computed: {
    filteredUsers() {
      let filtered = this.users;
      
      // Apply search filter
      if (this.searchQuery) {
        filtered = filtered.filter(user => 
          user.username.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (user.phone && user.phone.includes(this.searchQuery))
        );
      }
      
      // Apply status filter
      if (this.statusFilter) {
        filtered = filtered.filter(user => {
          if (this.statusFilter === 'active') return user.is_active;
          if (this.statusFilter === 'inactive') return !user.is_active;
          return true;
        });
      }
      
      return filtered;
    },
    activeUsersCount() {
      return this.users.filter(user => user.is_active).length;
    },
    inactiveUsersCount() {
      return this.users.filter(user => !user.is_active).length;
    }
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.error = null;
      
      try {
        const token = window.sessionStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/users', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        this.users = data.users;
      } catch (err) {
        this.error = 'Failed to fetch users. Please check your connection and try again.';
        console.error('Error fetching users:', err);
      } finally {
        this.loading = false;
      }
    },
    
    editUser(user) {
      this.editForm = {
        id: user.id,
        username: user.username,
        phone: user.phone || '',
        is_active: user.is_active
      };
      this.showEditModal = true;
    },
    
    async updateUser() {
      this.updatingUserId = this.editForm.id;
      
      try {
        const token = window.sessionStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5000/api/users/${this.editForm.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.editForm.username,
            phone: this.editForm.phone,
            is_active: this.editForm.is_active
          })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update user in local array
        const userIndex = this.users.findIndex(u => u.id === this.editForm.id);
        if (userIndex !== -1) {
          this.users[userIndex] = data.user;
        }
        
        this.showMessage('User updated successfully!', 'success');
        this.closeEditModal();
      } catch (err) {
        this.showMessage('Failed to update user. Please try again.', 'error');
        console.error('Error updating user:', err);
      } finally {
        this.updatingUserId = null;
      }
    },
    
    confirmDeleteUser(user) {
      this.userToDelete = user;
      this.showDeleteModal = true;
    },
    
    async deleteUser() {
      this.deletingUserId = this.userToDelete.id;
      
      try {
        const token = window.sessionStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5000/api/users/${this.userToDelete.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Remove user from local array
        this.users = this.users.filter(u => u.id !== this.userToDelete.id);
        
        this.showMessage('User deleted successfully!', 'success');
        this.closeDeleteModal();
      } catch (err) {
        this.showMessage('Failed to delete user. Please try again.', 'error');
        console.error('Error deleting user:', err);
      } finally {
        this.deletingUserId = null;
      }
    },
    
    closeEditModal() {
      this.showEditModal = false;
      this.editForm = {
        id: null,
        username: '',
        phone: '',
        is_active: true
      };
    },
    
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.userToDelete = null;
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

/* Fix for search input and select width on mobile */
@media (max-width: 768px) {
  .card-header .form-control,
  .card-header .form-select {
    width: 100% !important;
  }
}
</style>