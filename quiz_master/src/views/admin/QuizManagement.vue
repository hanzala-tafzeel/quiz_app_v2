<template>
  <AdminNavBar />
  
  <div class="container py-4">
    <!-- Flash Messages -->
    <div v-if="messages.length > 0" class="messages">
      <div 
        v-for="(message, index) in messages" 
        :key="index"
        :class="`alert alert-${message.category} text-center`"
      >
        {{ message.text }}
        <button type="button" class="btn-close" @click="dismissMessage(index)"></button>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 mb-4">
        <div class="d-flex justify-content-between align-items-center">
          <h1 class="text-center flex-grow-1">Quiz Management</h1>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="col-md-6">
        <form @submit.prevent="searchQuiz" class="float-end">
          <div class="input-group mb-3">
            <input
              type="text"
              class="form-control"
              v-model="search"
              placeholder="Search Quiz"
            />
            <button class="btn btn-dark" type="submit">Search</button>
          </div>
        </form>
      </div>

      <!-- Quizzes Container -->
      <div class="col-12">
        <div class="row g-4">
          <div v-if="filteredQuizzes.length === 0" class="col-12 text-center text-danger">
            <h3>No Quizzes Found</h3>
          </div>

          <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="col-md-6">
            <div class="card h-100 shadow-sm">
              <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
                <h5 class="m-0">{{ quiz.title }}</h5>
                <div class="action-icons">
                  <a 
                    href="#" 
                    class="text-white me-2" 
                    @click.prevent="openEditQuizModal(quiz)"
                  >
                    <i class="bi bi-pencil"></i>
                  </a>
                  <a 
                    href="#" 
                    class="text-white" 
                    @click.prevent="openDeleteQuizModal(quiz)"
                  >
                    <i class="bi bi-trash3"></i>
                  </a>
                </div>
              </div>
              <div class="card-body p-0">
                <div class="table-container">
                  <table class="table table-hover mb-0">
                    <thead class="table-light sticky-top">
                      <tr>
                        <th>S.no</th>
                        <th>Question</th>
                        <th>Marks</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(question, index) in quiz.questions" :key="question.id">
                        <td>&nbsp;&nbsp;{{ index + 1 }}</td>
                        <td>{{ question.question_text }}</td>
                        <td>{{ question.marks }}</td>
                        <td>
                          <a 
                            href="#" 
                            class="me-2"
                            @click.prevent="openEditQuestionModal(question, quiz)"
                          >
                            <i class="bi bi-pencil text-dark"></i>
                          </a>
                          <a 
                            href="#" 
                            @click.prevent="openDeleteQuestionModal(question, quiz)"
                          >
                            <i class="bi bi-trash3 text-dark"></i>
                          </a>
                        </td>
                      </tr>
                      <tr v-if="!quiz.questions || quiz.questions.length === 0">
                        <td colspan="4" class="text-center text-muted py-3">
                          No questions added yet
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="card-footer bg-white text-center">
                <button 
                  class="btn btn-sm btn-dark me-2"
                  @click="openAddQuestionModal(quiz)"
                >
                  <i class="bi bi-plus-circle me-2"></i>Add Question
                </button>
                <a :href="getManageQuestionUrl(quiz.id)" class="btn btn-sm btn-dark">
                  <i class="bi bi-list-check me-2"></i>Manage Questions
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 text-center mt-4">
        <button
          class="btn btn-dark"
          @click="openAddQuizModal"
        >
          <i class="bi bi-plus-circle me-2"></i>Add New Quiz
        </button>
      </div>
    </div>

    <!-- Add Quiz Modal -->
    <div v-if="modals.addQuiz" class="modal-backdrop" @click="closeModal('addQuiz')">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Add New Quiz</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal('addQuiz')"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addQuiz">
              <div class="mb-3">
                <label for="chapterSelect" class="form-label">Select Chapter</label>
                <select
                  class="form-select"
                  id="chapterSelect"
                  v-model="formData.chapter_id"
                  required
                >
                  <option value="">Select Chapter</option>
                  <option
                    v-for="chapter in chapters"
                    :key="chapter.id"
                    :value="chapter.id"
                  >
                    {{ chapter.name }}
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label for="quizTitle" class="form-label">Quiz Title</label>
                <input
                  type="text"
                  class="form-control"
                  id="quizTitle"
                  v-model="formData.title"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="quizDescription" class="form-label">Quiz Description</label>
                <input
                  type="text"
                  class="form-control"
                  id="quizDescription"
                  v-model="formData.description"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="quizDate" class="form-label">Date of Quiz</label>
                <input
                  type="date"
                  class="form-control"
                  id="quizDate"
                  v-model="formData.date"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="quizDuration" class="form-label">Duration (minutes)</label>
                <input
                  type="number"
                  class="form-control"
                  id="quizDuration"
                  v-model="formData.duration"
                  required
                />
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModal('addQuiz')">Cancel</button>
                <button type="submit" class="btn btn-dark">Add Quiz</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Quiz Modal -->
    <div v-if="modals.editQuiz" class="modal-backdrop" @click="closeModal('editQuiz')">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Edit Quiz</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal('editQuiz')"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateQuiz">
              <div class="mb-3">
                <label for="editChapterSelect" class="form-label">Select Chapter</label>
                <select
                  class="form-select"
                  id="editChapterSelect"
                  v-model="editFormData.chapter_id"
                  required
                >
                  <option value="">Select Chapter</option>
                  <option
                    v-for="chapter in chapters"
                    :key="chapter.id"
                    :value="chapter.id"
                  >
                    {{ chapter.name }}
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label for="editQuizTitle" class="form-label">Quiz Title</label>
                <input
                  type="text"
                  class="form-control"
                  id="editQuizTitle"
                  v-model="editFormData.title"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="editQuizDescription" class="form-label">Quiz Description</label>
                <input
                  type="text"
                  class="form-control"
                  id="editQuizDescription"
                  v-model="editFormData.description"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="editQuizDate" class="form-label">Date of Quiz</label>
                <input
                  type="date"
                  class="form-control"
                  id="editQuizDate"
                  v-model="editFormData.date"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="editQuizDuration" class="form-label">Duration (minutes)</label>
                <input
                  type="number"
                  class="form-control"
                  id="editQuizDuration"
                  v-model="editFormData.duration"
                  required
                />
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModal('editQuiz')">Cancel</button>
                <button type="submit" class="btn btn-dark">Update Quiz</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Quiz Modal -->
    <div v-if="modals.deleteQuiz" class="modal-backdrop" @click="closeModal('deleteQuiz')">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" @click="closeModal('deleteQuiz')"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete the quiz "{{ selectedQuiz?.title }}"? This will also delete all associated questions.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal('deleteQuiz')">Cancel</button>
            <button type="button" class="btn btn-danger" @click="confirmDeleteQuiz">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Question Modal -->
<div v-if="modals.addQuestion" class="modal-backdrop" @click="closeModal('addQuestion')">
  <div class="modal-dialog" @click.stop>
    <div class="modal-content">
      <div class="modal-header bg-dark text-white">
        <h5 class="modal-title">Add Question to {{ selectedQuiz?.title }}</h5>
        <button type="button" class="btn-close btn-close-white" @click="closeModal('addQuestion')"></button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="addQuestion">
          <div class="mb-3">
            <label for="questionText" class="form-label">Question Text</label>
            <textarea
              class="form-control"
              id="questionText"
              rows="3"
              v-model="questionForm.question_text"
              required
            ></textarea>
          </div>

          <div class="mb-3">
            <label for="option1" class="form-label">Option 1</label>
            <input
              type="text"
              class="form-control"
              id="option1"
              v-model="questionForm.option1"
              required
            />
          </div>

          <div class="mb-3">
            <label for="option2" class="form-label">Option 2</label>
            <input
              type="text"
              class="form-control"
              id="option2"
              v-model="questionForm.option2"
              required
            />
          </div>

          <div class="mb-3">
            <label for="option3" class="form-label">Option 3</label>
            <input
              type="text"
              class="form-control"
              id="option3"
              v-model="questionForm.option3"
              required
            />
          </div>

          <div class="mb-3">
            <label for="option4" class="form-label">Option 4</label>
            <input
              type="text"
              class="form-control"
              id="option4"
              v-model="questionForm.option4"
              required
            />
          </div>

          <div class="mb-3">
            <label for="correctOpt" class="form-label">Correct Option</label>
            <select
              class="form-select"
              id="correctOpt"
              v-model="questionForm.correct_opt"
              required
            >
              <option value="">Select Correct Option</option>
              <option value="1">Option 1</option>
              <option value="2">Option 2</option>
              <option value="3">Option 3</option>
              <option value="4">Option 4</option>
            </select>
          </div>

          <div class="mb-3">
            <label for="questionMarks" class="form-label">Marks</label>
            <input
              type="number"
              class="form-control"
              id="questionMarks"
              v-model="questionForm.marks"
              required
            />
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal('addQuestion')">Cancel</button>
            <button type="submit" class="btn btn-dark">Add Question</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

    <!-- Edit Question Modal -->
    <div v-if="modals.editQuestion" class="modal-backdrop" @click="closeModal('editQuestion')">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Edit Question</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal('editQuestion')"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateQuestion">
              <div class="mb-3">
                <label for="editQuestionText" class="form-label">Question Text</label>
                <textarea
                  class="form-control"
                  id="editQuestionText"
                  rows="3"
                  v-model="questionForm.question_text"
                  required
                ></textarea>
              </div>

              <div class="row mb-3">

                
                <div class="col">
                  <label for="editOption1" class="form-label">Option 1</label>
                  <input
                  type="text"
                  class="form-control"
                  id="editOption1"
                  v-model="questionForm.option1"
                  required
                  />
                </div>
                <div class="col">
                  <label for="editOption2" class="form-label">Option 2</label>
                  <input
                  type="text"
                  class="form-control"
                  id="editOption2"
                  v-model="questionForm.option2"
                  required 
                  />
                </div>
              </div>

            <div class="row mb-3">

              
              <div class="col">
                <label for="editOption3" class="form-label">Option 3</label>
                <input
                type="text"
                class="form-control"
                  id="editOption3"
                  v-model="questionForm.option3"
                  required  
                />
              </div>
              <div class="col">
                <label for="editOption4" class="form-label">Option 4</label>
                <input
                  type="text"
                  class="form-control"
                  id="editOption4"
                  v-model="questionForm.option4"
                  required
                  />
                </div>
              </div>

              <div class="row mb-3">

                <div class="col">
                  <label for="editCorrectOpt" class="form-label">Correct Option</label>
                  <select
                  class="form-select"
                  id="editCorrectOpt"
                  v-model="questionForm.correct_opt"
                  required
                >
                  <option value="">Select Correct Option</option>
                  <option value="1">Option 1</option>
                  <option value="2">Option 2</option>
                  <option value="3">Option 3</option>
                  <option value="4">Option 4</option>
                </select>
              </div>
              
              
              
              <div class="col">
                <label for="editQuestionMarks" class="form-label">Marks</label>
                <input
                  type="number"
                  class="form-control"
                  id="editQuestionMarks"
                  v-model="questionForm.marks"
                  required
                  />
                </div>
                
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModal('editQuestion')">Cancel</button>
                <button type="submit" class="btn btn-dark">Update Question</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Question Modal -->
    <div v-if="modals.deleteQuestion" class="modal-backdrop" @click="closeModal('deleteQuestion')">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal('deleteQuestion')"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this question? </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal('deleteQuestion')">Cancel</button>
            <button type="button" class="btn btn-danger" @click="confirmDeleteQuestion">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <FootPage />
</template>

<script>
import FootPage from "@/components/FootPage.vue";
import AdminNavBar from "@/components/AdminNavBar.vue";

export default {
  name: "QuizManagement",
  components: {
    FootPage,
    AdminNavBar,
  },
  data() {
    return {
      messages: [],
      search: "",
      selectedQuiz: null,
      selectedQuestion: null,
      modals: {
        addQuiz: false,
        editQuiz: false,
        deleteQuiz: false,
        addQuestion: false,
        editQuestion: false,
        deleteQuestion: false
      },
      formData: {
        chapter_id: "",
        title: "",
        description: "",
        date: "",
        duration: "",
      },
      editFormData: {
        id: "",
        chapter_id: "",
        title: "",
        description: "",
        date: "",
        duration: "",
      },
      questionForm: {
        id: null,
        question_text: "",
        marks: "",
        option1: "",    
        option2: "",    
        option3: "",    
        option4: "",    
        correct_opt: "",

        quiz_id: null
      }
    };
  },
  computed: {
    quizzes() {
      return this.$store.state.quizzes || [];
    },
    chapters() {
      return this.$store.state.chapters || [];
    },
    filteredQuizzes() {
      if (!this.search) return this.quizzes;
      return this.quizzes.filter(quiz =>
        quiz.title.toLowerCase().includes(this.search.toLowerCase())
      );
    }
  },
  methods: {
    // Message handling
    dismissMessage(index) {
      this.messages.splice(index, 1);
    },
    
    showMessage(text, category = 'success') {
      this.messages.push({ text, category });
      setTimeout(() => {
        this.messages.shift();
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
      this.formData = {
        chapter_id: "",
        title: "",
        description: "",
        date: "",
        duration: "",
      };
      this.editFormData = {
        id: "",
        chapter_id: "",
        title: "",
        description: "",
        date: "",
        duration: "",
      };
      this.questionForm = {
        id: null,
        question_text: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_opt: "",
        marks: "",
        quiz_id: null
      };
      this.selectedQuiz = null;
      this.selectedQuestion = null;
    },

    // Quiz modal methods
    openAddQuizModal() {
      this.resetForms();
      this.openModal('addQuiz');
    },

    openEditQuizModal(quiz) {
      this.selectedQuiz = quiz;
      this.editFormData = {
        id: quiz.id,
        chapter_id: quiz.chapter_id,
        title: quiz.title,
        description: quiz.description,
        date: quiz.date,
        duration: quiz.duration,
      };
      this.openModal('editQuiz');
    },

    openDeleteQuizModal(quiz) {
      this.selectedQuiz = quiz;
      this.openModal('deleteQuiz');
    },

    // Question modal methods
    openAddQuestionModal(quiz) {
      this.selectedQuiz = quiz;
      this.questionForm.quiz_id = quiz.id;
      this.openModal('addQuestion');
    },

    openEditQuestionModal(question, quiz) {
      this.selectedQuestion = question;
      this.selectedQuiz = quiz;
      this.questionForm = {
        id: question.id,
        question_text: question.question_text,
        option1: question.option1,
        option2: question.option2,
        option3: question.option3,
        option4: question.option4,
        correct_opt: question.correct_opt,
        marks: question.marks,
        quiz_id: quiz.id
      };
      this.openModal('editQuestion');
    },

    openDeleteQuestionModal(question, quiz) {
      this.selectedQuestion = question;
      this.selectedQuiz = quiz;
      this.openModal('deleteQuestion');
    },

    // API calls
    async fetchQuizzes() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/quizzes");
        const data = await response.json();
        const quizzes = (data.quizzes || []).map((quiz) => ({
          ...quiz,
          questions: quiz.questions || []
        }));
        this.$store.commit("SET_QUIZZES", quizzes);
      } catch (err) {
        this.showMessage("Failed to fetch quizzes!", "danger");
      }
    },

    async fetchChapters() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/chapters");
        const data = await response.json();
        const chapters = (data.chapters || []).map((chapter) => ({
          ...chapter,
        }));
        this.$store.commit("SET_CHAPTERS", chapters);
      } catch (err) {
        this.showMessage("Failed to fetch chapters!", "danger");
      }
    },

    // Quiz CRUD operations
    async addQuiz() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:5000/api/quizzes", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.formData),
        });
        
        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to add quiz");
        }

        await this.fetchQuizzes();
        this.showMessage("Quiz added successfully!", "success");
        this.closeModal('addQuiz');
        
      } catch (error) {
        this.showMessage(error.message || "Failed to add quiz.", "danger");
      }
    },

    async updateQuiz() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${this.editFormData.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            chapter_id: this.editFormData.chapter_id,
            title: this.editFormData.title,
            description: this.editFormData.description,
            date: this.editFormData.date,
            duration: this.editFormData.duration,
          }),
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to update quiz");
        }

        await this.fetchQuizzes();
        this.showMessage("Quiz updated successfully!", "success");
        this.closeModal('editQuiz');
        
      } catch (error) {
        this.showMessage(error.message || "Failed to update quiz.", "danger");
      }
    },

    async confirmDeleteQuiz() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${this.selectedQuiz.id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to delete quiz");
        }

        await this.fetchQuizzes();
        this.showMessage("Quiz deleted successfully!", "success");
        this.closeModal('deleteQuiz');
        
      } catch (error) {
        this.showMessage(error.message || "Failed to delete quiz.", "danger");
      }
    },

    // Question CRUD operations
    async addQuestion() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${this.selectedQuiz.id}/questions`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.questionForm),
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to add question");
        }

        await this.fetchQuizzes();
        this.showMessage("Question added successfully!", "success");
        this.closeModal('addQuestion');
        
      } catch (error) {
        this.showMessage(error.message || "Failed to add question.", "danger");
      }
    },

    async updateQuestion() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/questions/${this.selectedQuestion.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            question_text: this.questionForm.question_text,
            marks: this.questionForm.marks,
            quiz_id: this.selectedQuiz.id
          }),
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to update question");
        }

        await this.fetchQuizzes();
        this.showMessage("Question updated successfully!", "success");
        this.closeModal('editQuestion');
        
      } catch (error) {
        this.showMessage(error.message || "Failed to update question.", "danger");
      }
    },

    async confirmDeleteQuestion() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/questions/${this.selectedQuestion.id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || "Failed to delete question");
        }

        await this.fetchQuizzes();
        this.showMessage("Question deleted successfully!", "success");
        this.closeModal('deleteQuestion');
        
      } catch (error) {
        this.showMessage(error.message || "Failed to delete question.", "danger");
      }
    },

    // Utility methods
    searchQuiz() {
      // Search functionality is handled by computed property
    },

    getManageQuestionUrl(quizId) {
      return `/manage_questions/${quizId}`;
    },
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  },
};
</script>




<style scoped>

.table-container {
  max-height: 300px;
  overflow-y: auto;
  border-radius: 0;
}

.table-container::-webkit-scrollbar {
  width: 6px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.sticky-top {
  position: sticky;
  top: 0;
  z-index: 10;
}

.card-body {
  padding: 0 !important;
}

.table th {
  font-size: 0.875rem;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
  padding: 0.75rem 0.5rem;
}

.table td {
  font-size: 0.875rem;
  padding: 0.75rem 0.5rem;
  vertical-align: middle;
}

.table td:nth-child(2) {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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

.messages {
  margin-bottom: 1rem;
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
  border-color: #ffeeba;
}
.alert-info {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}
.messages .btn-close {
  position: absolute;
  top: 0.5rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
}
.messages .btn-close:hover {
  opacity: 0.8;
}

.table-container {
  max-height: 300px;
  overflow-y: auto;
  border-radius: 0;
}

.table-container::-webkit-scrollbar {
  width: 6px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.sticky-top {
  position: sticky;
  top: 0;
  z-index: 10;
}

.card-body {
  padding: 0 !important;
}

.table th {
  font-size: 0.875rem;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
  padding: 0.75rem 0.5rem;
}

.table td {
  font-size: 0.875rem;
  padding: 0.75rem 0.5rem;
  vertical-align: middle;
}

.table td:nth-child(2) {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}
</style>