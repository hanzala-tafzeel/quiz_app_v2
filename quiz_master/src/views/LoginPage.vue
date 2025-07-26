
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
  <!-- login form  -->
  <div class="container py-5">
    <div class="row justify-content-center align-items-center p-0">
      <div class="col-12 col-md-6 col-lg-5">
        <div class="bg-white shadow-lg rounded-3 p-4 p-md-5">
          <!-- Login Header -->
          <div class="text-center mb-4">
            <div
              class="bg-dark text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3"
              style="width: 80px; height: 80px"
            >
              <i class="bi bi-person-fill" style="font-size: 2.5rem"></i>
            </div>
            <h2 class="mb-0">Login</h2>
          </div>

          <!-- Flash Messages -->
          <div class="messages">
            <div :class="['alert', 'text-center', 'alert-' + category]">
              {{ message }}
            </div>
          </div>

          <!-- Login Form -->
          <form @submit="loginUser">
            <div class="mb-4">
              <label for="exampleInputEmail1" class="form-label text-muted"
                >Email address</label
              >
              <div class="input-group">
                <span class="input-group-text bg-dark text-white">
                  <i class="bi bi-envelope-fill"></i>
                </span>
                <input
                  type="email"
                  class="form-control"
                  id="exampleInputEmail1"
                  aria-describedby="emailHelp"
                  v-model="formData.email"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div class="mb-4">
              <label for="exampleInputPassword1" class="form-label text-muted"
                >Password</label
              >
              <div class="input-group">
                <span class="input-group-text bg-dark text-white">
                  <i class="bi bi-lock-fill"></i>
                </span>
                <input
                  type="password"
                  class="form-control"
                  id="exampleInputPassword1"
                  v-model="formData.password"
                  placeholder="Enter your password"
                />
              </div>
            </div>

            <button type="submit" class="btn btn-dark w-100 py-2 mb-3">
              <i class="bi bi-box-arrow-in-right me-2"></i>Login
            </button>

            <div class="text-center">
              <router-link
                to="/register"
                class="text-decoration-none text-dark"
              >
                <i class="bi bi-person-plus-fill me-2"></i>Don't have an
                account? Register here
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

export default{
  name: 'LoginPage',
  components: { NavPage, FootPage },
  data() {
    return {
      formData: {
        email: "",
        password: "",
      },
      message: "",
      category: "",
    };
  },
  methods: {
    async loginUser(event) {
      event.preventDefault();
      try {
        // Call API directly here
        const response = await fetch("http://127.0.0.1:5000/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.formData),
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.message);

        // Commit to store

        this.$store.commit("SET_LOGIN_DATA", {
          user: data.user,
          token: data.token,
          userRole: data.role,
        });

        // Save token in localStorage (optional)
        window.sessionStorage.setItem('token', data.token);
        window.sessionStorage.setItem('user', JSON.stringify(data.user));
        window.sessionStorage.setItem('userRole', data.role);
        window.sessionStorage.setItem('isAuthenticated', true);

        console.log("window.sessionStorage", window.sessionStorage.getItem('user'));
        // Redirect based on role
        if (data.role === "admin") {
          this.$router.push("/admin");
        } else if (data.role === "user") {
          this.$router.push("/user");
        } else {
          this.$router.push("/");
        }

        // Success message
        this.message = data.message || "Login successful!";
        this.category = "success";
        // Optionally clear form
        this.formData.email = "";
        this.formData.password = "";

      } catch (error) {
        this.message = error.message || "Login failed. Invalid credentials.";
        this.category = "danger";
      }
    }
  }
}
</script>



<style></style>
