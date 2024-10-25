<template>
  <div>
    <h1>Welcome to Wayback CTF</h1>
    <form @submit.prevent="handleSubmit">
      <label for="linkInput">Enter the Link:</label>
      <input
        type="text"
        id="linkInput"
        v-model="link"
        placeholder="Enter the URL here"
      />
      <button type="submit">Submit</button>
    </form>

    <p v-if="submittedLink">Submitted Link: {{ submittedLink }}</p>
    <pre v-if="apiResponse">{{ apiResponse }}</pre> <!-- Display JSON response -->
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      link: "",
      submittedLink: null,
      apiResponse: null,
    };
  },
  methods: {
    async handleSubmit() {
      this.submittedLink = this.link;
      try {
        const response = await axios.post("http://localhost:3000/api/scoreboard", {
          link: this.link,
        });
        this.apiResponse = response.data; // Store API response in component data
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style scoped>
h1 {
  color: #42b983;
}

form {
  margin-top: 20px;
}

input {
  padding: 8px;
  margin-right: 10px;
  width: 300px;
}

button {
  padding: 8px 12px;
  cursor: pointer;
}
</style>
