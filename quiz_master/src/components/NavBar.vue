<script>
export default {
    name: 'NavPage',

    methods: {
        logout() {
            this.$store.dispatch('logout')

            // Redirect to login page
            this.$router.push('/login')

            // Optional: Show success message
            console.log('Logged out successfully')
        }
    }

};
</script>

<template>
    <div>

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="#"></a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-md mx-auto gap-2">
                        <li class="nav-item rounded">
                            <!-- <a class="nav-link active" aria-current="page" href="#"><i class="bi bi-house-fill me-2"></i>Home</a> -->
                            <router-link to="/user" class="nav-link"><i
                                    class="bi bi-house-fill me-2"></i>Home</router-link>
                        </li>
                        <li class="nav-item rounded">

                            <!-- <a class="nav-link " href="{{url_for('quiz_management')}}"><i class="bi bi-clipboard me-2"></i>Quiz</a> -->
                            <router-link to="/user/quizzes" class="nav-link"><i
                                    class="bi bi-clipboard me-2"></i>Quiz</router-link>
                        </li>
                        <li class="nav-item rounded">
                            <!-- <a class="nav-link" href="{{url_for('admin_summary')}}"><i class="bi bi-book-half me-2"></i>Summary </a> -->
                            <router-link to="/user/summary" class="nav-link"><i
                                    class="bi bi-book-half me-2"></i>Summary</router-link>
                        </li>
                        <li class="nav-item dropdown rounded">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
                                data-bs-toggle="dropdown" aria-expanded="false"><i
                                    class="bi bi-person-fill me-2"></i>Profile</a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                                <li>
                                    <!-- <a class="dropdown-item" href="{{url_for('user_management')}}">Account</a> -->
                                    <router-link to="/user/profile" class="dropdown-item">Account</router-link>
                                    <router-link to="/user/profile/history" class="dropdown-item">History</router-link>
                                </li>

                                <li>
                                    <hr class="dropdown-divider">
                                </li>
                                <li><a class="dropdown-item" @click="logout">Logout</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

    </div>
</template>

<style></style>