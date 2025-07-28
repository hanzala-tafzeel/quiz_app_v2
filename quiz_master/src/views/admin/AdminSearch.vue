<template>
    <div class="search-page">
      <!-- Navbar -->
       <AdminNavBar/>

  
      <div class="container py-4">
        <!-- Search Header -->
        <div class="row mb-4">
          <div class="col-12">
            <h1 class="text-center mb-4">Search Everything</h1>
            <p class="text-center text-muted">Find subjects, quizzes, and questions across our platform</p>
          </div>
        </div>
  
        <!-- Search Controls -->
        <div class="row mb-4">
          <div class="col-md-8 mx-auto">
            <div class="card shadow-sm">
              <div class="card-body">
                <!-- Main Search Input -->
                <div class="input-group input-group-lg mb-3">
                  <span class="input-group-text bg-dark text-white">
                    <i class="bi bi-search"></i>
                  </span>
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="searchQuery" 
                    placeholder="Search subjects, quizzes, questions..." 
                    @input="performSearch"
                    @keyup.enter="performSearch"
                  />
                  <button 
                    class="btn btn-outline-secondary" 
                    type="button" 
                    @click="clearSearch"
                    v-if="searchQuery"
                  >
                    <i class="bi bi-x-circle"></i>
                  </button>
                </div>
  
                <!-- Search Filters -->
                <div class="row g-3">
                  <div class="col-md-6">
                    <select class="form-select" v-model="searchType" @change="performSearch">
                      <option value="all">All Results</option>
                      <option value="subjects">Subjects Only</option>
                      <option value="quizzes">Quizzes Only</option>
                      <option value="questions">Questions Only</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <button class="btn btn-dark w-100" @click="performSearch">
                      <i class="bi bi-search me-2"></i>Search
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Search Results Summary -->
        <div class="row mb-3" v-if="hasSearched">
          <div class="col-12">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0">
                Search Results 
                <span class="text-muted">
                  ({{ totalResults }} found{{ searchQuery ? ` for "${searchQuery}"` : '' }})
                </span>
              </h5>
              <small class="text-muted">
                {{ searchTime }}ms
              </small>
            </div>
            <hr>
          </div>
        </div>
  
        <!-- No Results -->
        <div v-if="hasSearched && totalResults === 0" class="row">
          <div class="col-12 text-center">
            <div class="card bg-light">
              <div class="card-body py-5">
                <i class="bi bi-search display-1 text-muted"></i>
                <h3 class="mt-3">No results found</h3>
                <p class="text-muted">Try different keywords or check your spelling</p>
                <button class="btn btn-outline-dark" @click="clearSearch">Clear Search</button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Search Results -->
        <div v-if="hasSearched && totalResults > 0">
          <!-- Subjects Results -->
          <div v-if="filteredSubjects.length > 0 && (searchType === 'all' || searchType === 'subjects')" class="mb-5">
            <h4 class="mb-3">
              <i class="bi bi-book-fill text-primary me-2"></i>
              Subjects ({{ filteredSubjects.length }})
            </h4>
            <div class="row g-3">
              <div v-for="subject in filteredSubjects" :key="'subject-' + subject.id" class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm border-start border-primary border-3">
                  <div class="card-body">
                    <h6 class="card-title">{{ subject.name }}</h6>
                    <p class="card-text text-muted small">{{ subject.description }}</p>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-muted">
                        <i class="bi bi-list-ul me-1"></i>{{ subject.chapters_count || 0 }} chapters
                      </small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Quizzes Results -->
          <div v-if="filteredQuizzes.length > 0 && (searchType === 'all' || searchType === 'quizzes')" class="mb-5">
            <h4 class="mb-3">
              <i class="bi bi-question-circle-fill text-success me-2"></i>
              Quizzes ({{ filteredQuizzes.length }})
            </h4>
            <div class="row g-3">
              <div v-for="quiz in filteredQuizzes" :key="'quiz-' + quiz.id" class="col-md-6 col-lg-4">
                <div class="card h-100 shadow-sm border-start border-success border-3">
                  <div class="card-body">
                    <h6 class="card-title">{{ quiz.title }}</h6>
                    <p class="card-text text-muted small">{{ quiz.description }}</p>
                    <div class="row text-center mb-2">
                      <div class="col-4">
                        <small class="text-muted">
                          <i class="bi bi-clock me-1"></i>{{ quiz.duration }}m
                        </small>
                      </div>
                      <div class="col-4">
                        <small class="text-muted">
                          <i class="bi bi-list-ol me-1"></i>{{ quiz.questions_count || 0 }} Q's
                        </small>
                      </div>
                      <div class="col-4">
                        <small class="text-muted">
                          <i class="bi bi-star me-1"></i>{{ quiz.total_marks || 0 }} pts
                        </small>
                      </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-muted">{{ getChapterName(quiz.chapter_id) }}</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Questions Results -->
          <div v-if="filteredQuestions.length > 0 && (searchType === 'all' || searchType === 'questions')" class="mb-5">
            <h4 class="mb-3">
              <i class="bi bi-chat-square-text-fill text-warning me-2"></i>
              Questions ({{ filteredQuestions.length }})
            </h4>
            <div class="row g-3">
              <div v-for="question in filteredQuestions" :key="'question-' + question.id" class="col-12">
                <div class="card shadow-sm border-start border-warning border-3">
                  <div class="card-body">
                    <div class="row">
                      <div class="col-md-8">
                        <h6 class="card-title">{{ question.question_text }}</h6>
                        <div class="row g-2 mt-2">
                          <div class="col-sm-6">
                            <small class="text-muted d-block">A) {{ question.option1 }}</small>
                            <small class="text-muted d-block">B) {{ question.option2 }}</small>
                          </div>
                          <div class="col-sm-6">
                            <small class="text-muted d-block">C) {{ question.option3 }}</small>
                            <small class="text-muted d-block">D) {{ question.option4 }}</small>
                          </div>
                        </div>
                      </div>
                      <div class="col-md-4 text-end">
                        <div class="mb-2">
                          <span class="badge bg-warning text-dark">{{ question.marks }} marks</span>
                        </div>
                        <small class="text-muted d-block">{{ getQuizTitle(question.quiz_id) }}</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Quick Search Suggestions -->
        <div v-if="!hasSearched" class="row">
          <div class="col-12">
            <div class="card bg-light">
              <div class="card-body text-center py-5">
                <i class="bi bi-lightbulb display-1 text-muted mb-3"></i>
                <h4>Quick Search Suggestions</h4>
                <div class="row g-2 mt-3 justify-content-center">
                  <div class="col-auto">
                    <button class="btn btn-outline-dark btn-sm" @click="quickSearch('Mathematics')">Mathematics</button>
                  </div>
                  <div class="col-auto">
                    <button class="btn btn-outline-dark btn-sm" @click="quickSearch('Science')">Science</button>
                  </div>
                  <div class="col-auto">
                    <button class="btn btn-outline-dark btn-sm" @click="quickSearch('History')">History</button>
                  </div>
                  <div class="col-auto">
                    <button class="btn btn-outline-dark btn-sm" @click="quickSearch('Python')">Python</button>
                  </div>
                  <div class="col-auto">
                    <button class="btn btn-outline-dark btn-sm" @click="quickSearch('Quiz')">Quiz</button>
                  </div>
                </div>
              </div>
            </div>
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
    name: 'AdminSearch',
    components: {
        AdminNavBar,
        FootPage
    },
    data() {
      return {
        searchQuery: '',
        searchType: 'all',
        hasSearched: false,
        searchTime: 0,
        
        // Results data
        allSubjects: [],
        allQuizzes: [],
        allQuestions: [],
        allChapters: [],
        
        // Filtered results
        filteredSubjects: [],
        filteredQuizzes: [],
        filteredQuestions: []
      }
    },
    computed: {
      totalResults() {
        return this.filteredSubjects.length + this.filteredQuizzes.length + this.filteredQuestions.length;
      }
    },
    methods: {
      async performSearch() {
        if (!this.searchQuery.trim() && this.searchType === 'all') {
          this.clearSearch();
          return;
        }
  
        const startTime = performance.now();
        this.hasSearched = true;
  
        try {
          // Fetch data if not already loaded
          if (this.allSubjects.length === 0) {
            await this.fetchAllData();
          }
  
          // Filter results based on search query and type
          this.filterResults();
  
          const endTime = performance.now();
          this.searchTime = Math.round(endTime - startTime);
  
        } catch (error) {
          console.error('Search error:', error);
          this.showMessage('Search failed. Please try again.', 'danger');
        }
      },
  
      async fetchAllData() {
        try {
          // Fetch subjects
          const subjectsResponse = await fetch('http://127.0.0.1:5000/api/subjects/');
          const subjectsData = await subjectsResponse.json();
          this.allSubjects = subjectsData.subjects || [];
  
          // Fetch quizzes
          const quizzesResponse = await fetch('http://127.0.0.1:5000/api/quizzes');
          const quizzesData = await quizzesResponse.json();
          this.allQuizzes = quizzesData.quizzes || [];
  
          // Fetch chapters for reference
          const chaptersResponse = await fetch('http://127.0.0.1:5000/api/chapters');
          const chaptersData = await chaptersResponse.json();
          this.allChapters = chaptersData.chapters || [];
  
          // Extract questions from quizzes
          this.allQuestions = [];
          this.allQuizzes.forEach(quiz => {
            if (quiz.questions) {
              quiz.questions.forEach(question => {
                this.allQuestions.push({
                  ...question,
                  quiz_id: quiz.id,
                  quiz_title: quiz.title
                });
              });
            }
          });
  
        } catch (error) {
          console.error('Failed to fetch data:', error);
        }
      },
  
      filterResults() {
        const query = this.searchQuery.toLowerCase().trim();
  
        // Filter subjects
        if (this.searchType === 'all' || this.searchType === 'subjects') {
          this.filteredSubjects = this.allSubjects.filter(subject => 
            subject.name.toLowerCase().includes(query) ||
            subject.description.toLowerCase().includes(query)
          );
        } else {
          this.filteredSubjects = [];
        }
  
        // Filter quizzes
        if (this.searchType === 'all' || this.searchType === 'quizzes') {
          this.filteredQuizzes = this.allQuizzes.filter(quiz => 
            quiz.title.toLowerCase().includes(query) ||
            quiz.description.toLowerCase().includes(query)
          );
        } else {
          this.filteredQuizzes = [];
        }
  
        // Filter questions
        if (this.searchType === 'all' || this.searchType === 'questions') {
          this.filteredQuestions = this.allQuestions.filter(question => 
            question.question_text.toLowerCase().includes(query) ||
            question.option1.toLowerCase().includes(query) ||
            question.option2.toLowerCase().includes(query) ||
            question.option3.toLowerCase().includes(query) ||
            question.option4.toLowerCase().includes(query)
          );
        } else {
          this.filteredQuestions = [];
        }
      },
  
      clearSearch() {
        this.searchQuery = '';
        this.searchType = 'all';
        this.hasSearched = false;
        this.filteredSubjects = [];
        this.filteredQuizzes = [];
        this.filteredQuestions = [];
      },
  
      quickSearch(term) {
        this.searchQuery = term;
        this.performSearch();
      },
  
      getChapterName(chapterId) {
        const chapter = this.allChapters.find(c => c.id === chapterId);
        return chapter ? chapter.name : 'Unknown Chapter';
      },
  
      getQuizTitle(quizId) {
        const quiz = this.allQuizzes.find(q => q.id === quizId);
        return quiz ? quiz.title : 'Unknown Quiz';
      },
  
      showMessage(text, type) {
        console.log(`${type}: ${text}`);
      }
    },
  
    mounted() {
      this.fetchAllData();
      
      // Check if there's a search query in URL params
      const urlParams = new URLSearchParams(window.location.search);
      const query = urlParams.get('q');
      if (query) {
        this.searchQuery = query;
        this.performSearch();
      }
    }
  }
  </script>
  
  <style scoped>

  .card {
    transition: transform 0.2s ease-in-out;
  }
  
  .card:hover {
    transform: translateY(-2px);
  }
  
  .border-start {
    border-left-width: 4px !important;
  }
  </style>
  