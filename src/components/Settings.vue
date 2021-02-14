<template>
  <div class="settings">

    <v-card class="kubeconfig-manager">
      <v-card-title>Kubeconfig path</v-card-title>

      <ul id="kubeconfig-list">
        <li v-for="kubeconfig in kubeconfigs" :key="kubeconfig">
          {{ getKubeconfigText(kubeconfig) }}
        </li>
      </ul>
      <v-card-actions>
        <v-btn @click="addKubeconfigDialog = true">
          Update kubeconfig path
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-dialog
      v-model="addKubeconfigDialog"
      v-if="addKubeconfigDialog"
      width="600"
    >
      <v-card>
        <v-card-title> Please select the path </v-card-title>
        <v-card-text>
          <v-text-field v-model="kubeconfigToAdd"> </v-text-field>
          <v-btn @click="addKubeconfig()"> Update kubeconfig path </v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  components: {},
  name: "Settings",
  props: {},
  data: function () {
    return {
      kubeconfigs: [],
      activeKubeconfig: null,
      loading: false,
      kubeconfigToAdd: null,
      addKubeconfigDialog: false,
    };
  },
  methods: {
    backToList: function () {
      this.$emit("backToList");
    },
    fetchKubeconfigs: function () {
      this.loading = true;
      axios
        .get("http://127.0.0.1:5000/api/kubeconfig")
        .then(
          (response) => (
            (this.kubeconfigs = response.data.kubeconfigs),
            (this.activeKubeconfig = response.data.activeKubeconfig)
          )
        )
        .catch((error) => console.log(error))
        .finally(() => (this.loading = false));
    },
    getKubeconfigText(kubeconfig) {
      if (kubeconfig === this.activeKubeconfig) {
        return kubeconfig + " (Active)";
      } else {
        return kubeconfig;
      }
    },
    addKubeconfig() {
      this.addKubeconfigDialog = false;
      axios
        .post("http://127.0.0.1:5000/api/kubeconfig", {
          kubeconfig: this.kubeconfigToAdd,
        })
        .then(
          (response) => (
            (this.kubeconfigs = response.data.kubeconfigs),
            (this.activeKubeconfig = response.data.activeKubeconfig)
          )
        )
        .catch((error) => console.log(error))
        .finally(() => (this.fetchKubeconfigs(), (this.loading = false)));
    },
  },
  mounted() {
    this.fetchKubeconfigs();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.kubeconfig-manager {
    padding: 32px;
    margin: 16px;
}
</style>
