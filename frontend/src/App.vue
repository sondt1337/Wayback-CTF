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
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      link: "", // lưu giá trị nhập vào
      submittedLink: null, // lưu link đã submit
    };
  },
  methods: {
    handleSubmit() {
      this.submittedLink = this.link; // lưu link khi submit
      // Bạn có thể thực hiện bất kỳ hành động nào với link này ở đây, ví dụ gọi API
      console.log("Submitted link:", this.link);
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
