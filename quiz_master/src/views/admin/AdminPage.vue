<template>
  <!-- page for admin to manage subjects and chapters -->

  <div class="page-wrapper d-flex flex-column min-vh-100">
    <AdminNavBar />

    <div class="container py-4">

      <!-- toast to display msg -->
      <div class="toast-container position-fixed top-0 end-0 p-3">
        <div v-if="message" :class="[
          'toast',
          'show',
          messageType === 'success' ? 'bg-success' : 'bg-danger',
        ]">
          <div class="toast-body text-white">
            {{ message }}
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-12 mb-4">
          <div class="d-flex justify-content-between align-items-center">
            <h1 class="text-center flex-grow-1">
              Subject and Chapter Management
            </h1>
          </div>
        </div>



        <div class="col-md-6">
          <h3 v-if="isAuthenticated" class="text-secondary">
            Welcome, {{ capitalize(user.username) }}!
          </h3>
          <div v-else>
            <p>You are not logged in.</p>
            <a href="/login">Login</a>
          </div>
        </div>

        <div class="col-md-6">
          <form @submit.prevent="searchSubjects" class="float-end">
            <div class="input-group mb-3">
              <input type="text" class="form-control" v-model="searchQuery" placeholder="Search Subject" />
              <button class="btn btn-dark" type="submit">Search</button>
            </div>
          </form>
        </div>

        <!-- Subjects Container -->
        <div class="col-12">
          <div class="row g-4">
            <div v-if="filteredSubjects.length === 0" class="col-12 text-center text-danger">
              <h3>No Subjects Found</h3>
            </div>

            <div v-for="subject in filteredSubjects" :key="subject.id" class="col-md-6 col-lg-4">
              <div class="card card-subject shadow-sm">
                <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
                  <h4 class="m-0">{{ subject.name }}</h4>
                  <div class="action-icons">
                    <a href="#" class="text-white me-2" @click.prevent="openEditSubjectModal(subject)">
                      <i class="bi bi-pencil"></i>
                    </a>
                    <a href="#" class="text-white" @click.prevent="openDeleteSubjectModal(subject)">
                      <i class="bi bi-trash3"></i>
                    </a>
                  </div>
                </div>
                <div class="card-body p-0">
                  <table class="table table-hover mb-0">
                    <thead>
                      <tr>
                        <th>Chapter Name</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="chapter in subject.chapters" :key="chapter.id">
                        <td>{{ chapter.name }}</td>
                        <td>
                          <a href="#" class="me-2" @click.prevent="
                            openEditChapterModal(chapter, subject)
                            ">
                            <i class="bi bi-pencil text-dark"></i>
                          </a>
                          <a href="#" @click.prevent="
                            openDeleteChapterModal(chapter, subject)
                            ">
                            <i class="bi bi-trash3 text-dark"></i>
                          </a>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="card-footer bg-white text-center">
                  <button class="btn btn-sm btn-dark" @click="openAddChapterModal(subject)">
                    <i class="bi bi-plus-circle me-2"></i>Add Chapter
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12 text-center mt-4">
          <button class="btn btn-dark" @click="openAddSubjectModal">
            <i class="bi bi-plus-circle me-2"></i>Add New Subject
          </button>
        </div>
      </div>

      <!-- Add Subject Modal -->
      <div v-if="modals.addSubject" class="modal-backdrop" @click="closeModal('addSubject')">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div class="modal-header bg-dark text-white">
              <h5 class="modal-title">Add New Subject</h5>
              <button type="button" class="btn-close btn-close-white" @click="closeModal('addSubject')"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="addSubject">
                <div class="mb-3">
                  <label for="subjectName" class="form-label">Subject Name</label>
                  <input type="text" class="form-control" id="subjectName" v-model="forms.subject.name" required />

                  <label for="subjectName" class="form-label">Subject Description</label>
                  <input type="text" class="form-control" id="subjectDescription" v-model="forms.subject.description"
                    required />
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeModal('addSubject')">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-dark">Add Subject</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Edit Subject Modal -->
      <div v-if="modals.editSubject" class="modal-backdrop" @click="closeModal('editSubject')">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div class="modal-header bg-dark text-white">
              <h5 class="modal-title">Edit Subject</h5>
              <button type="button" class="btn-close" @click="closeModal('editSubject')"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="updateSubject">
                <div class="mb-3">
                  <label for="editSubjectName" class="form-label">Subject Name</label>
                  <input type="text" class="form-control" id="editSubjectName" v-model="forms.subject.name" required />
                </div>
                <div class="mb-3">
                  <label for="editSubjectDescription" class="form-label">Subject Description</label>
                  <input type="text" class="form-control" id="editSubjectdescription"
                    v-model="forms.subject.description" required />
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeModal('editSubject')">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-dark">
                    Update Subject
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Delete Subject Confirmation Modal -->
      <div v-if="modals.deleteSubject" class="modal-backdrop" @click="closeModal('deleteSubject')">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div class="modal-header bg-dark text-white ">
              <h5 class="modal-title">Confirm Delete</h5>
              <button type="button" class="btn-close btn-close-white" @click="closeModal('deleteSubject')"></button>
            </div>
            <div class="modal-body">
              <p>
                Are you sure you want to delete the subject "{{
                  currentSubject?.name
                }}"? This will also delete all associated chapters.
              </p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal('deleteSubject')">
                Cancel
              </button>
              <button type="button" class="btn btn-danger" @click="deleteSubject">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Chapter Modal -->
      <div v-if="modals.addChapter" class="modal-backdrop" @click="closeModal('addChapter')">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div class="modal-header bg-dark text-white">
              <h5 class="modal-title">
                Add Chapter to {{ currentSubject?.name }}
              </h5>
              <button type="button" class="btn-close" @click="closeModal('addChapter')"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="addChapter">
                <div class="mb-3">
                  <label for="chapterName" class="form-label">Chapter Name</label>
                  <input type="text" class="form-control" id="chapterName" v-model="forms.chapter.name" required />
                </div>

                <div class="mb-3">
                  <label for="chapterDescriptiion" class="form-label">Chapter Description</label>
                  <input type="text" class="form-control" id="chapterDescription" v-model="forms.chapter.description"
                    required />
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeModal('addChapter')">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-dark">Add Chapter</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Edit Chapter Modal -->
      <div v-if="modals.editChapter" class="modal-backdrop" @click="closeModal('editChapter')">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div class="modal-header bg-dark text-white">
              <h5 class="modal-title">Edit Chapter</h5>
              <button type="button" class="btn-close" @click="closeModal('editChapter')"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="updateChapter">
                <div class="mb-3">
                  <label for="editChapterName" class="form-label">Chapter Name</label>
                  <input type="text" class="form-control" id="editChapterName" v-model="forms.chapter.name" required />
                </div>
                <div class="mb-3">
                  <label for="chapterDescriptiion" class="form-label">Chapter Description</label>
                  <input type="text" class="form-control" id="chapterDescription" v-model="forms.chapter.description"
                    required />
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeModal('editChapter')">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-dark">
                    Update Chapter
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Delete Chapter Confirmation Modal -->
      <div v-if="modals.deleteChapter" class="modal-backdrop" @click="closeModal('deleteChapter')">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div class="modal-header bg-dark text-white">
              <h5 class="modal-title">Confirm Delete</h5>
              <button type="button" class="btn-close btn-close-white" @click="closeModal('deleteChapter')"></button>
            </div>
            <div class="modal-body">
              <p>
                Are you sure you want to delete the chapter "{{
                  currentChapter?.name
                }}"?
              </p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal('deleteChapter')">
                Cancel
              </button>
              <button type="button" class="btn btn-danger" @click="deleteChapter">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <FootPage />

  </div>
</template>

<script>
import AdminNavBar from "@/components/AdminNavBar.vue";
import FootPage from "@/components/FootPage.vue";
export default {
  name: "AdminPage",
  components: {
    AdminNavBar,
    FootPage,
  },
  data() {
    return {
      searchQuery: "",
      message: '',           // Single message text
      messageType: 'success',
      modals: {
        addSubject: false,
        editSubject: false,
        deleteSubject: false,
        addChapter: false,
        editChapter: false,
        deleteChapter: false,
      },
      forms: {
        subject: {
          id: null,
          name: "",
          description: "",
        },
        chapter: {
          id: null,
          name: "",
          description: "",
          subjectId: null,
        },
      },
      currentSubject: null,
      currentChapter: null,
    };
  },
  computed: {
    isAuthenticated() {
      return window.sessionStorage.getItem('isAuthenticated') === 'true';
    },
    user() {
      return JSON.parse(window.sessionStorage.getItem('user'));
    },
    subjects() {
      // Always read from Vuex store
      return this.$store.getters.getSubjects;
    },
    filteredSubjects() {
      if (!this.searchQuery) return this.subjects;
      return this.subjects.filter((subject) =>
        subject.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchSubjects() {
      try {
        console.log("window.sessionStorage", window.sessionStorage.getItem('user'));

        const response = await fetch("http://127.0.0.1:5000/api/subjects", {
          method: "GET"
        });
        const data = await response.json();
        // You *may* have a chapters field on each subject after another API call
        // If not, just work with subjects for now
        const subjects = (data.subjects || []).map((subject) => ({
          ...subject,
          chapters: subject.chapters || [], // fallback in case missing
        }));
        this.$store.commit("SET_SUBJECTS", subjects);
      } catch (err) {
        this.showMessage("Failed to fetch subjects!", "danger");
      }
    },

    capitalize(str) {
      if (!str || typeof str !== "string") return "";
      return str.toString().charAt(0).toUpperCase() + str.slice(1);
    },

    searchSubjects() {
      // Search functionality is handled by computed property
      // This method can be used for API calls if needed
    },

    dismissMessage(index) {
      this.messages.splice(index, 1);
    },

    showMessage(text, type = 'success') {
      this.message = text;
      this.messageType = type;
      setTimeout(() => {
        this.message = '';
      }, 5000);
    },

    // Modal management
    openModal(modalName) {
      this.modals[modalName] = true;
    },

    closeModal(modalName) {
      this.modals[modalName] = false;
      this.resetForms();
    },

    resetForms() {
      this.forms.subject = { id: null, name: "" };
      this.forms.chapter = { id: null, name: "", subjectId: null };
      this.currentSubject = null;
      this.currentChapter = null;
    },

    // Subject operations
    openAddSubjectModal() {
      this.resetForms();
      this.openModal("addSubject");
    },

    openEditSubjectModal(subject) {
      this.currentSubject = subject;
      this.forms.subject = {
        id: subject.id,
        name: subject.name,
        description: subject.description || "",
      };
      this.openModal("editSubject");
    },

    openDeleteSubjectModal(subject) {
      this.currentSubject = subject;
      this.openModal("deleteSubject");
    },

    async addSubject() {
      // Check for duplicates in current Vuex state
      if (
        this.subjects.some(
          (s) => s.name.toLowerCase() === this.forms.subject.name.toLowerCase()
        )
      ) {
        this.showMessage("Subject already exists!", "danger");
        return;
      }

      try {
        // API call to add subject

        const token = window.sessionStorage.getItem('token');
        console.log(token)

        const response = await fetch("http://127.0.0.1:5000/api/subjects", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            name: this.forms.subject.name,
            description: this.forms.subject.description || "",
          }),
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to add subject");
        }

        await this.fetchSubjects();

        this.showMessage("Subject added successfully!", "success");
        this.closeModal("addSubject");
        this.resetForms();
      } catch (error) {
        this.showMessage(
          error.message || "An error occurred while adding subject",
          "danger"
        );
      }
    },

    async updateSubject() {
      // Check for duplicates in current Vuex state
      if (
        this.subjects.some(
          (s) =>
            s.name.toLowerCase() === this.forms.subject.name.toLowerCase() &&
            s.id !== this.currentSubject.id
        )
      ) {
        this.showMessage("Subject already exists!", "danger");
        return;
      }

      try {
        // API call to add subject
        const subject_id = this.currentSubject.id;
        const token = window.sessionStorage.getItem('token');
        console.log("JWT token:", token);
        const response = await fetch(
          `http://127.0.0.1:5000/api/subjects/${subject_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              name: this.forms.subject.name,
              description: this.forms.subject.description || "",
            }),
          }
        );

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to update subject");
        }

        await this.fetchSubjects();

        this.showMessage("Subject Updated successfully!", "success");
        this.closeModal("editSubject");
        this.resetForms();
      } catch (error) {
        this.showMessage(
          error.message || "An error occurred while updating subject",
          "danger"
        );
      }
    },

    async deleteSubject() {
      try {
        // API call to add subject
        console.log("JWT token:", this.$store.state.token);
        const subject_id = this.currentSubject.id;
        const token = window.sessionStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${subject_id}`,{
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(
            errData.message ||
            "Failed to Delete subject Probaly your tokes has expired"
          );
        }

        await this.fetchSubjects();

        this.showMessage("Subject Deleted successfully!", "success");
        this.closeModal("deleteSubject");
        this.resetForms();
      } catch (error) {
        this.showMessage(
          error.message || "An error occurred while adding subject",
          "danger"
        );
      }
    },

    // Chapter operations
    openAddChapterModal(subject) {
      this.currentSubject = subject;
      this.forms.chapter.subjectId = subject.id;
      this.openModal("addChapter");
    },

    openEditChapterModal(chapter, subject) {
      this.currentChapter = chapter;
      this.currentSubject = subject;
      this.forms.chapter = {
        id: chapter.id,
        name: chapter.name,
        description: chapter.description || "",
        subjectId: subject.id,
      };
      this.openModal("editChapter");
    },

    openDeleteChapterModal(chapter, subject) {
      this.currentChapter = chapter;
      this.currentSubject = subject;
      this.openModal("deleteChapter");
    },

    async addChapter() {
      try {
        // API call to add subject
        console.log("JWT token:", this.$store.state.token);
        const subject_id = this.currentSubject.id;
        const token = window.sessionStorage.getItem('token');

        const response = await fetch(
          `http://127.0.0.1:5000/api/subjects/${subject_id}/chapters`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              name: this.forms.chapter.name,
              description: this.forms.chapter.description || "",
            }),
          }
        );

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to add subject");
        }

        await this.fetchSubjects();

        this.showMessage("Chapter added successfully!", "success");
        this.closeModal("addChapter");
        this.resetForms();
      } catch (error) {
        this.showMessage(
          error.message || "An error occurred while adding chapter",
          "danger"
        );
      }
      this.closeModal("addChapter");
    },

    async updateChapter() {
      const token = window.sessionStorage.getItem('token');

      try {
        const chapter_id = this.currentChapter.id;
        const subject_id = this.currentSubject.id;
        const response = await fetch(
          `http://127.0.0.1:5000/api/chapters/${chapter_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              name: this.forms.chapter.name,
              description: this.forms.chapter.description || "",
              subject_id: subject_id,
            }),
          }
        );

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to update chapter");
        }

        await this.fetchSubjects();

        this.showMessage("Chapter updated successfully!", "success");

        this.closeModal("editChapter");
      } catch (error) {
        this.showMessage(
          error.message || "An error occurred while updating chapter",
          "danger"
        );
      }
    },

    async deleteChapter() {
      try {
        // API call to add subject
        console.log("JWT token:", this.$store.state.token);
        const chapter_id = this.currentChapter.id;
        const token = window.sessionStorage.getItem('token');
        const response = await fetch(
          `http://127.0.0.1:5000/api/chapters/${chapter_id}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to Delete Chapter");
        }

        await this.fetchSubjects();

        this.showMessage("Chapter Deleted successfully!", "success");
        this.closeModal("deleteChapter");
        this.resetForms();
      } catch (error) {
        this.showMessage(
          error.message || "An error occurred while deleting chapter",
          "danger"
        );
      }

      this.closeModal("deleteChapter");
    },
  },
  mounted() {
    this.fetchSubjects();
  },
};
</script>

<style scoped>
.toast-container .toast {
  min-width: 250px;
}

.card-subject {
  transition: transform 0.2s ease-in-out;
}

.card-subject:hover {
  transform: translateY(-2px);
}

.action-icons a {
  margin-left: 10px;
  text-decoration: none;
}

.action-icons a:hover {
  opacity: 0.7;
}

/* Modal Styles */
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

.modal-content {
  border: none;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.modal-title {
  margin: 0;
  flex-grow: 1;
}



.modal-body {
  padding: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #dee2e6;
}



.alert {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.375rem;
}

.alert-success {
  color: #155724;
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

.alert-warning {
  color: #856404;
  background-color: #fff3cd;
  border-color: #ffeaa7;
}

.alert-info {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}

.btn-close {
  position: absolute;
  background: #000;
  top: 0.75rem;
  right: 1.25rem;
}
</style>
