<template>
 <div class="page-wrapper d-flex flex-column min-vh-100">

  <!-- search for user -->
  <NavBar />
  <div class="container py-4">

    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex align-items-center justify-content-between">
          <div>
            <h2 class="mb-2">
              <i class="bi bi-collection me-2 text-dark"></i>
              Browse Subjects & Quizzes
            </h2>
            <p class="text-muted mb-0">Explore subjects, chapters, and available quizzes</p>
          </div>
          <div class="d-flex gap-2">
            <!-- View toggle buttons -->
            <button @click="viewMode = 'card'" class="btn"
              :class="viewMode === 'card' ? 'btn-dark' : 'btn-outline-dark'">
              <i class="bi bi-grid"></i>
            </button>
            <button @click="viewMode = 'list'" class="btn"
              :class="viewMode === 'list' ? 'btn-dark' : 'btn-outline-dark'">
              <i class="bi bi-list"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Filter Controls -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm bg-light">
          <div class="card-body">
            <div class="row g-3">
              <!-- Search input -->
              <div class="col-md-4">
                <label class="form-label text-dark">Search</label>
                <div class="input-group">
                  <input v-model="searchQuery" type="text" class="form-control border-secondary"
                    placeholder="Search subjects, chapters, or quizzes...">
                  <button v-if="searchQuery" @click="clearSearch" class="btn btn-outline-secondary" type="button">
                    <i class="bi bi-x"></i>
                  </button>
                </div>
              </div>

              <!-- Subject filter -->
              <div class="col-md-3">
                <label class="form-label text-dark">Filter by Subject</label>
                <select v-model="selectedSubject" class="form-select border-secondary">
                  <option value="">All Subjects</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
              </div>

              <!-- Chapter filter -->
              <div class="col-md-3">
                <label class="form-label text-dark">Filter by Chapter</label>
                <select v-model="selectedChapter" class="form-select border-secondary" :disabled="!selectedSubject">
                  <option value="">All Chapters</option>
                  <option v-for="chapter in availableChapters" :key="chapter.id" :value="chapter.id">
                    {{ chapter.name }}
                  </option>
                </select>
              </div>

              <!-- Content type filter -->
              <div class="col-md-2">
                <label class="form-label text-dark">Show</label>
                <select v-model="contentFilter" class="form-select border-secondary">
                  <option value="all">All Content</option>
                  <option value="subjects">Subjects Only</option>
                  <option value="chapters">Chapters Only</option>
                  <option value="quizzes">Quizzes Only</option>
                </select>
              </div>
            </div>

            <!-- Active filters display -->
            <div v-if="hasActiveFilters" class="mt-3">
              <div class="d-flex align-items-center gap-2 flex-wrap">
                <small class="text-muted">Active filters:</small>
                <span v-if="searchQuery" class="badge bg-dark">
                  Search: "{{ searchQuery }}"
                  <button @click="searchQuery = ''" class="btn-close btn-close-white ms-1"
                    style="font-size: 0.6rem;"></button>
                </span>
                <span v-if="selectedSubject" class="badge bg-secondary">
                  Subject: {{ getSubjectName(selectedSubject) }}
                  <button @click="selectedSubject = ''" class="btn-close btn-close-white ms-1"
                    style="font-size: 0.6rem;"></button>
                </span>
                <span v-if="selectedChapter" class="badge bg-dark-subtle text-dark">
                  Chapter: {{ getChapterName(selectedChapter) }}
                  <button @click="selectedChapter = ''" class="btn-close ms-1" style="font-size: 0.6rem;"></button>
                </span>
                <button @click="clearAllFilters" class="btn btn-sm btn-outline-dark">
                  Clear All
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-dark" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading content...</p>
    </div>

    <!-- Content Display -->
    <div v-else>
      <!-- Card View -->
      <div v-if="viewMode === 'card'">
        <!-- Subjects display -->
        <div v-if="contentFilter === 'all' || contentFilter === 'subjects'">
          <h4 class="mb-3 text-dark" v-if="filteredSubjects.length > 0">
            <i class="bi bi-book me-2"></i>Subjects
            <span class="badge bg-secondary ms-2">{{ filteredSubjects.length }}</span>
          </h4>
          <div class="row g-4 mb-5">
            <div v-for="subject in filteredSubjects" :key="`subject-${subject.id}`" class="col-lg-4 col-md-6">
              <div class="card h-100 border-0 shadow-sm hover-card bg-white">
                <div class="card-header bg-dark text-white">
                  <h5 class="mb-0">
                    <i class="bi bi-journal-bookmarks me-2"></i>
                    {{ subject.name }}
                  </h5>
                </div>
                <div class="card-body">
                  <p class="text-muted mb-3">{{ subject.description || 'No description available' }}</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">
                      {{ getSubjectChapterCount(subject.id) }} chapters
                    </small>
                    <button @click="selectSubject(subject.id)" class="btn btn-sm btn-dark">
                      View Chapters
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Chapters display -->
        <div v-if="(contentFilter === 'all' || contentFilter === 'chapters') && filteredChapters.length > 0">
          <h4 class="mb-3 text-dark">
            <i class="bi bi-collection me-2"></i>Chapters
            <span class="badge bg-secondary ms-2">{{ filteredChapters.length }}</span>
          </h4>
          <div class="row g-4 mb-5">
            <div v-for="chapter in filteredChapters" :key="`chapter-${chapter.id}`" class="col-lg-4 col-md-6">
              <div class="card h-100 border-0 shadow-sm hover-card bg-white">
                <div class="card-header bg-dark text-white">
                  <h6 class="mb-0">
                    <i class="bi bi-bookmark me-2"></i>
                    {{ chapter.name }}
                  </h6>
                  <small class="opacity-75">{{ getSubjectName(chapter.subject_id) }}</small>
                </div>
                <div class="card-body">
                  <p class="text-muted mb-3">{{ chapter.description || 'No description available' }}</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">
                      {{ getChapterQuizCount(chapter.id) }} quizzes
                    </small>
                    <button @click="selectChapter(chapter.id)" class="btn btn-sm btn-secondary">
                      View Quizzes
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quizzes display -->
        <div v-if="(contentFilter === 'all' || contentFilter === 'quizzes') && filteredQuizzes.length > 0">
          <h4 class="mb-3 text-dark">
            <i class="bi bi-play-circle me-2"></i>Quizzes
            <span class="badge bg-secondary ms-2">{{ filteredQuizzes.length }}</span>
          </h4>
          <div class="row g-4">
            <div v-for="quiz in filteredQuizzes" :key="`quiz-${quiz.id}`" class="col-lg-4 col-md-6">
              <div class="card h-100 border-0 shadow-sm hover-card bg-white">
                <div class="card-header bg-dark text-white border-bottom">
                  <h6 class="mb-0">
                    <i class="bi bi-patch-question me-2"></i>
                    {{ quiz.title }}
                  </h6>
                  <small class="text-white">{{ getQuizChapterName(quiz.chapter_id) }}</small>
                </div>
                <div class="card-body">
                  <p class="text-muted mb-3">{{ quiz.description || 'No description available' }}</p>
                  <div class="row text-center mb-3">
                    <div class="col-4">
                      <small class="text-muted d-block">Duration</small>
                      <strong>{{ quiz.duration }}m</strong>
                    </div>
                    <div class="col-4">
                      <small class="text-muted d-block">Total Marks</small>
                      <strong>{{ quiz.total_marks }}</strong>
                    </div>
                    <div class="col-4">
                      <small class="text-muted d-block">Status</small>
                      <span class="badge" :class="quiz.is_active ? 'bg-dark' : 'bg-secondary'">
                        {{ quiz.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="card-footer bg-transparent">
                  <div class="d-flex gap-2">
                    <button @click="viewQuizDetails(quiz)" class="btn btn-sm btn-outline-dark flex-fill">
                      <i class="bi bi-eye me-1"></i>Details
                    </button>
                    <router-link :to="`/user/quiz/${quiz.id}`" class="btn btn-sm btn-dark flex-fill"
                      :disabled="!quiz.is_active">
                      <i class="bi bi-play me-1"></i>Start Quiz
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="card border-0 shadow-sm bg-white">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="border-0 text-dark">Type</th>
                  <th class="border-0 text-dark">Name</th>
                  <th class="border-0 text-dark">Parent</th>
                  <th class="border-0 text-dark">Details</th>
                  <th class="border-0 text-center text-dark">Actions</th>
                </tr>
              </thead>
              <tbody>
                <!-- Combined list view for all content types -->
                <tr v-for="item in combinedFilteredContent" :key="item.key">
                  <td>
                    <span class="badge" :class="getTypeBadgeClass(item.type)">
                      <i :class="getTypeIcon(item.type)" class="me-1"></i>
                      {{ item.type }}
                    </span>
                  </td>
                  <td>
                    <strong class="text-dark">{{ item.name }}</strong>
                    <br>
                    <small class="text-muted">{{ item.description }}</small>
                  </td>
                  <td>
                    <span class="text-muted">{{ item.parent || '-' }}</span>
                  </td>
                  <td>
                    <small class="text-muted">{{ item.details }}</small>
                  </td>
                  <td class="text-center">
                    <div class="btn-group" role="group">
                      <button v-if="item.type === 'Subject'" @click="selectSubject(item.id)"
                        class="btn btn-sm btn-outline-dark">
                        <i class="bi bi-eye"></i>
                      </button>
                      <button v-if="item.type === 'Chapter'" @click="selectChapter(item.id)"
                        class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-eye"></i>
                      </button>
                      <button v-if="item.type === 'Quiz'" @click="viewQuizDetails(item.originalData)"
                        class="btn btn-sm btn-outline-dark">
                        <i class="bi bi-info-circle"></i>
                      </button>
                      <button v-if="item.type === 'Quiz' && item.originalData.is_active"
                        @click="startQuiz(item.originalData)" class="btn btn-sm btn-dark">
                        <i class="bi bi-play"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && combinedFilteredContent.length === 0" class="text-center py-5">
        <div class="mb-4">
          <i class="bi bi-search" style="font-size: 4rem; color: #6c757d;"></i>
        </div>
        <h4 class="text-muted mb-3">No Content Found</h4>
        <p class="text-muted mb-4">Try adjusting your search or filter criteria</p>
        <button @click="clearAllFilters" class="btn btn-dark">
          Clear All Filters
        </button>
      </div>
    </div>

    <!-- Quiz Details Modal -->
    <div v-if="selectedQuiz" class="modal-backdrop" @click="closeQuizModal">
      <div class="modal-dialog modal-lg modal-dialog-centered" @click.stop>
        <div class="modal-content bg-white">

          <!-- Modal Header -->
          <div class="modal-header d-flex justify-content-between align-items-center bg-dark text-white px-4 py-3">
            <h5 class="modal-title m-0">{{ selectedQuiz.title }}</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeQuizModal"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body px-4 py-3">
            <div class="row g-3">

              <!-- Quiz Information -->
              <div class="col-md-6">
                <h6 class="text-dark mb-2">Quiz Information</h6>
                <ul class="list-unstyled mb-3">
                  <li><strong>Duration:</strong> {{ selectedQuiz.duration }} minutes</li>
                  <li><strong>Total Marks:</strong> {{ selectedQuiz.total_marks }}</li>
                  <li><strong>Pass Marks:</strong> {{ selectedQuiz.pass_marks }}</li>
                  <li><strong>Status:</strong>
                    <span class="badge" :class="selectedQuiz.is_active ? 'bg-dark' : 'bg-secondary'">
                      {{ selectedQuiz.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </li>
                </ul>
              </div>

              <!-- Chapter & Subject -->
              <div class="col-md-6">
                <h6 class="text-dark mb-2">Chapter & Subject</h6>
                <ul class="list-unstyled mb-3">
                  <li><strong>Chapter:</strong> {{ getQuizChapterName(selectedQuiz.chapter_id) }}</li>
                  <li><strong>Subject:</strong> {{ getQuizSubjectName(selectedQuiz.chapter_id) }}</li>
                  <li><strong>Schedule Date:</strong> {{ formatDate(selectedQuiz.schedule_date) }}</li>
                  <li><strong>Created:</strong> {{ formatDate(selectedQuiz.created_at) }}</li>
                </ul>
              </div>

            </div>

            <!-- Description -->
            <div class="mt-4">
              <h6 class="text-dark mb-2">Description</h6>
              <p class="text-muted mb-0">{{ selectedQuiz.description || 'No description available' }}</p>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer d-flex justify-content-between px-4 py-3">
            <button type="button" class="btn btn-secondary" @click="closeQuizModal">
              Close
            </button>
            <button type="button" class="btn btn-dark" @click="startQuiz(selectedQuiz)"
              :disabled="!selectedQuiz.is_active">
              <i class="bi bi-play me-1"></i> Start Quiz
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
import NavBar from '@/components/NavBar.vue';
import FootPage from '@/components/FootPage.vue';
export default {
  name: 'BrowseContent',
  components: {
    NavBar,
    FootPage
  },
  data() {
    return {
      loading: false,
      viewMode: 'card', // 'card' or 'list'

      // Filter and search states
      searchQuery: '',
      selectedSubject: '',
      selectedChapter: '',
      contentFilter: 'all', // 'all', 'subjects', 'chapters', 'quizzes'

      // Data arrays
      subjects: [],
      chapters: [],
      quizzes: [],

      // Modal state
      selectedQuiz: null
    }
  },
  computed: {
    // Computed property for available chapters based on selected subject
    availableChapters() {
      if (!this.selectedSubject) return this.chapters;
      return this.chapters.filter(chapter => chapter.subject_id == this.selectedSubject);
    },

    // Filtered subjects based on search and filters
    filteredSubjects() {
      let filtered = this.subjects;

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(subject =>
          subject.name.toLowerCase().includes(query) ||
          (subject.description && subject.description.toLowerCase().includes(query))
        );
      }

      if (this.selectedSubject) {
        filtered = filtered.filter(subject => subject.id == this.selectedSubject);
      }

      return filtered;
    },

    // Filtered chapters based on search and filters
    filteredChapters() {
      let filtered = this.chapters;

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(chapter =>
          chapter.name.toLowerCase().includes(query) ||
          (chapter.description && chapter.description.toLowerCase().includes(query))
        );
      }

      if (this.selectedSubject) {
        filtered = filtered.filter(chapter => chapter.subject_id == this.selectedSubject);
      }

      if (this.selectedChapter) {
        filtered = filtered.filter(chapter => chapter.id == this.selectedChapter);
      }

      return filtered;
    },

    // Filtered quizzes based on search and filters
    filteredQuizzes() {
      let filtered = this.quizzes;

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(quiz =>
          quiz.title.toLowerCase().includes(query) ||
          (quiz.description && quiz.description.toLowerCase().includes(query))
        );
      }

      if (this.selectedChapter) {
        filtered = filtered.filter(quiz => quiz.chapter_id == this.selectedChapter);
      } else if (this.selectedSubject) {
        const subjectChapterIds = this.chapters
          .filter(chapter => chapter.subject_id == this.selectedSubject)
          .map(chapter => chapter.id);
        filtered = filtered.filter(quiz => subjectChapterIds.includes(quiz.chapter_id));
      }

      return filtered;
    },

    // Combined content for list view
    combinedFilteredContent() {
      let content = [];

      if (this.contentFilter === 'all' || this.contentFilter === 'subjects') {
        content = content.concat(
          this.filteredSubjects.map(subject => ({
            key: `subject-${subject.id}`,
            type: 'Subject',
            id: subject.id,
            name: subject.name,
            description: subject.description || 'No description',
            parent: null,
            details: `${this.getSubjectChapterCount(subject.id)} chapters`,
            originalData: subject
          }))
        );
      }

      if (this.contentFilter === 'all' || this.contentFilter === 'chapters') {
        content = content.concat(
          this.filteredChapters.map(chapter => ({
            key: `chapter-${chapter.id}`,
            type: 'Chapter',
            id: chapter.id,
            name: chapter.name,
            description: chapter.description || 'No description',
            parent: this.getSubjectName(chapter.subject_id),
            details: `${this.getChapterQuizCount(chapter.id)} quizzes`,
            originalData: chapter
          }))
        );
      }

      if (this.contentFilter === 'all' || this.contentFilter === 'quizzes') {
        content = content.concat(
          this.filteredQuizzes.map(quiz => ({
            key: `quiz-${quiz.id}`,
            type: 'Quiz',
            id: quiz.id,
            name: quiz.title,
            description: quiz.description || 'No description',
            parent: this.getQuizChapterName(quiz.chapter_id),
            details: `${quiz.duration}m, ${quiz.total_marks} marks`,
            originalData: quiz
          }))
        );
      }

      return content;
    },

    // Check if any filters are active
    hasActiveFilters() {
      return this.searchQuery || this.selectedSubject || this.selectedChapter || this.contentFilter !== 'all';
    }
  },
  methods: {
    // Fetch all data from APIs
    async fetchAllData() {
      this.loading = true;
      try {
        await Promise.all([
          this.fetchSubjects(),
          this.fetchChapters(),
          this.fetchQuizzes()
        ]);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        this.loading = false;
      }
    },

    // Fetch subjects from API
    async fetchSubjects() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/subjects');
        if (response.ok) {
          const data = await response.json();
          this.subjects = data.subjects || [];
        }
      } catch (error) {
        console.error('Error fetching subjects:', error);
      }
    },

    // Fetch chapters from API
    async fetchChapters() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/chapters');
        if (response.ok) {
          const data = await response.json();
          this.chapters = data.chapters || [];
        }
      } catch (error) {
        console.error('Error fetching chapters:', error);
      }
    },

    // Fetch quizzes from API
    async fetchQuizzes() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/quizzes');
        if (response.ok) {
          const data = await response.json();
          this.quizzes = data.quizzes || [];
        }
      } catch (error) {
        console.error('Error fetching quizzes:', error);
      }
    },

    // Helper methods for counting and name resolution
    getSubjectChapterCount(subjectId) {
      return this.chapters.filter(chapter => chapter.subject_id === subjectId).length;
    },

    getChapterQuizCount(chapterId) {
      return this.quizzes.filter(quiz => quiz.chapter_id === chapterId).length;
    },

    getSubjectName(subjectId) {
      const subject = this.subjects.find(s => s.id === subjectId);
      return subject ? subject.name : 'Unknown Subject';
    },

    getChapterName(chapterId) {
      const chapter = this.chapters.find(c => c.id === chapterId);
      return chapter ? chapter.name : 'Unknown Chapter';
    },

    getQuizChapterName(chapterId) {
      return this.getChapterName(chapterId);
    },

    getQuizSubjectName(chapterId) {
      const chapter = this.chapters.find(c => c.id === chapterId);
      return chapter ? this.getSubjectName(chapter.subject_id) : 'Unknown Subject';
    },

    // Filter and search methods
    selectSubject(subjectId) {
      this.selectedSubject = subjectId;
      this.selectedChapter = '';
      this.contentFilter = 'all';
    },

    selectChapter(chapterId) {
      const chapter = this.chapters.find(c => c.id === chapterId);
      if (chapter) {
        this.selectedSubject = chapter.subject_id;
        this.selectedChapter = chapterId;
        this.contentFilter = 'all';
      }
    },

    clearSearch() {
      this.searchQuery = '';
    },

    clearAllFilters() {
      this.searchQuery = '';
      this.selectedSubject = '';
      this.selectedChapter = '';
      this.contentFilter = 'all';
    },

    // Quiz related methods
    viewQuizDetails(quiz) {
      this.selectedQuiz = quiz;
    },

    closeQuizModal() {
      this.selectedQuiz = null;
    },

    startQuiz(quiz) {
      if (quiz.is_active) {

        this.$router.push(`user/quiz/${quiz.id}`);
      }
    },

    // Utility methods for list view
    getTypeBadgeClass(type) {
      switch (type) {
        case 'Subject': return 'bg-dark';
        case 'Chapter': return 'bg-secondary';
        case 'Quiz': return 'bg-light text-dark';
        default: return 'bg-secondary';
      }
    },

    getTypeIcon(type) {
      switch (type) {
        case 'Subject': return 'bi bi-journal-bookmarks';
        case 'Chapter': return 'bi bi-bookmark';
        case 'Quiz': return 'bi bi-patch-question';
        default: return 'bi bi-circle';
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString();
    }
  },

  mounted() {
    // Fetch all data when component mounts
    this.fetchAllData();
  }
}
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

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
  max-width: 800px;
  width: 95%;
  max-height: 90vh;
  overflow-y: auto;
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
}

.border-0 {
  border: 0 !important;
}

@media (max-width: 767.98px) {
  .container {
    padding-left: 15px;
    padding-right: 15px;
  }
}
</style>