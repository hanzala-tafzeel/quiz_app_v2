
<template>
    
    <div class="page-wrapper d-flex flex-column min-vh-100">

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container">
        <router-link class="navbar-brand fw-bold" to="/">QuizMaster</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-md mx-auto gap-2">
            <li class="nav-item rounded">
              <router-link class="nav-link active" aria-current="page" to="/">
                <i class="bi bi-house-fill me-2"></i>Home
              </router-link>
            </li>
            <li class="nav-item rounded">
              <router-link class="nav-link" to="/login">
                <i class="bi bi-box-arrow-in-right me-2"></i>Login
              </router-link>
            </li>
            <li class="nav-item rounded">
              <router-link class="nav-link" to="/register">
                <i class="bi bi-clipboard2-check-fill me-2"></i>Signup
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container py-5">
        <div class="row justify-content-center align-items-center p-0">
            <div class="col-12 col-md-6 ">
                <div class="bg-white shadow-lg rounded-3 p-3 p-md-5">
                    <!-- Register Header -->
                    <div class="text-center mb-4">
                        <div class="bg-dark text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3"
                            style="width: 80px; height: 80px;">
                            <i class="bi bi-person-plus-fill"></i>
                        </div>
                        <h2 class="mb-0">Register</h2>
                    </div>

                    <div class="messages text-center">
                        <div class="alert alert-{{ category }} ">{{ message }}</div>

                    </div>

                    <!-- Registration Form -->
                    <form class="row g-3" @submit="registerUser">
                        <!-- Full Name -->
                        <div class="col-12">
                            <label for="fullname" class="form-label text-muted">Full Name</label>
                            <div class="input-group">
                                <span class="input-group-text bg-dark text-white">
                                    <i class="bi bi-person-fill"></i>
                                </span>
                                <input type="text" class="form-control" id="fullname" placeholder="Enter your full name"
                                    v-model="formData.fullname">
                            </div>
                        </div>

                        <!-- Email -->
                        <div class="col-md-6">
                            <label for="inputEmail" class="form-label text-muted">Email</label>
                            <div class="input-group">
                                <span class="input-group-text bg-dark text-white">
                                    <i class="bi bi-envelope-fill"></i>
                                </span>
                                <input type="email" class="form-control" id="inputEmail" placeholder="Enter your email"
                                    v-model="formData.email">
                            </div>
                        </div>

                        <!-- Password -->
                        <div class="col-md-6">
                            <label for="inputPassword4" class="form-label text-muted">Password</label>
                            <div class="input-group">
                                <span class="input-group-text bg-dark text-white">
                                    <i class="bi bi-lock-fill"></i>
                                </span>
                                <input type="password" class="form-control" id="inputPassword4"
                                    placeholder="Create password" v-model="formData.password">
                            </div>
                        </div>

                        <!-- Mobile Number -->
                        <div class="col-12">
                            <label for="inputAddress" class="form-label text-muted">Mobile Number</label>
                            <div class="input-group">
                                <span class="input-group-text bg-dark text-white">
                                    <i class="bi bi-phone-fill"></i>
                                </span>
                                <input type="tel" class="form-control" id="inputAddress"
                                    placeholder="Enter your mobile number" v-model="formData.mobile"
                                    pattern="[0-9]{10}">
                            </div>
                        </div>


                        <!-- Submit Button -->
                        <div class="col-12">
                            <button type="submit" class="btn btn-dark w-100 py-2 mb-3">
                                <i class="bi bi-person-plus-fill me-2"></i>Register
                            </button>
                        </div>

                        <!-- Login Link -->
                        <div class="col-12 text-center">

                            <router-link to="/login" class="text-decoration-none text-dark">
                                <i class="bi bi-box-arrow-in-right me-2"></i>Already have an account? Login here

                            </router-link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <FootPage/>

    </div>

</template>


<script>


import NavPage from '@/components/NavBar.vue';
import FootPage from '@/components/FootPage.vue';

export default {
    naeme: 'RegisterPage',
    components: {
        NavPage,
        FootPage,
    },
    data() {
        return {
            formData: {
                fullname: "",
                email: "",
                password: "",
                mobile: ""
            },
            message: "",
            category: ""
        }
    },
    methods: {
async registerUser(event) {
  event.preventDefault();

  try {
    const response = await fetch("http://127.0.0.1:5000/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(this.formData)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Registration failed.");
    }

    // Show a success message
    this.message = data.message || "Registration successful! Please log in.";
    this.category = "success";

    // Optionally clear the form
    this.formData.email = "";
    this.formData.password = "";
    // clear other fields if you have them, e.g., this.formData.username = "";

    // After a short delay, redirect to login page
    setTimeout(() => {
      this.$router.push("/login");
    }, 1500); // 1.5 seconds for user to read the message

  } catch (error) {
    this.message = error.message || "Registration failed. Please try again.";
    this.category = "danger";
  }
}

    },


}

</script>



<style></style>
