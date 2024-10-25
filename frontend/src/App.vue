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

    <!-- Table for displaying data -->
    <table v-if="apiResponse && apiResponse.success" border="1" cellpadding="10" cellspacing="0">
      <thead>
        <tr>
          <th>Position</th>
          <th>Name</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in apiResponse.data" :key="entry.account_id">
          <td>{{ entry.pos }}</td>
          <td>{{ entry.name }}</td>
          <td>{{ entry.score }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Error Message -->
    <p v-if="apiResponse && !apiResponse.success">Failed to fetch data.</p>
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
      apiResponse: null, // Stores the API response data
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
        this.apiResponse = { success: false }; // Set response to indicate failure
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

table {
  margin-top: 20px;
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
}
</style>
