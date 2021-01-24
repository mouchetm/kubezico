<template>
  <div class="pods-list">
    <v-card class="resource-list" outlined>
      <v-toolbar tile>
        <v-toolbar-title>List of {{ resourceType }}</v-toolbar-title>
        <v-toolbar-title
          ><v-btn @click="backToList()"> Back to list </v-btn></v-toolbar-title
        >
        <v-toolbar-title
          ><v-btn @click="refresh()"> Refresh </v-btn></v-toolbar-title
        >
      </v-toolbar>
      <v-card-text>
        <div class="pod-list-items">
          <v-data-table
            :items="pods"
            :headers="headers"
            :items-per-page="100"
            :search="search"
            :loading="loading"
          >
            <template v-slot:top>
              <v-text-field
                v-model="search"
                label="Search"
                class="mx-4"
              ></v-text-field>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon @click="displayJson(item)"> fas fa-info </v-icon>
              <v-icon
                v-if="resourceType === 'pod'"
                @click="showContainers(item)"
              >
                fas fa-angle-double-right
              </v-icon>
            </template>
          </v-data-table>
        </div>
      </v-card-text>
    </v-card>
    <v-dialog
      v-model="dialog"
      v-if="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <div class="resource-details-card"></div>
      <v-card>
        <v-toolbar tile>
          <v-toolbar-title
            >{{ item.metadata.name }} in
            {{ item.metadata.namespace }}</v-toolbar-title
          >
          <v-toolbar-title
            ><v-btn @click="closeDialog()">Close</v-btn></v-toolbar-title
          >
        </v-toolbar>
        <v-card-text>
          <vue-json-pretty :data="item"> </vue-json-pretty>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="logDialog"
      v-if="logDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-title>
          Logs for pod {{ item.metadata.name }} in {{ item.metadata.namespace }}
          <v-btn @click="closeLogDialog()">Close</v-btn>
        </v-card-title>
        <v-card-text>
          <v-virtual-scroll :items="logs" height="600" item-height="64">
            <template v-slot:default="{ item }">
              <v-list-item :key="item">
                <v-list-item-content>
                  <v-list-item-title>
                    {{ item }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>

              <v-divider></v-divider>
            </template>
          </v-virtual-scroll>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="containerDialog" v-if="containerDialog" width="600">
      <v-card>
        <v-card-title> Please select the container </v-card-title>
        <v-card-text>
          <ul id="example-1">
            <li v-for="container in containers" :key="container.name">
              <a class="container-item" @click="showLogs(container)">
                {{ container.name }}</a
              >
            </li>
          </ul>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

export default {
  components: {
    VueJsonPretty,
  },
  name: "Pod",
  props: {
    resourceType: String,
    namespace: String,
  },
  data: function () {
    return {
      loading: false,
      dialog: false,
      logDialog: false,
      containerDialog: false,
      item: {},
      pods: [],
      containers: [],
      logs: "",
      allHeaders: {
        pod: [
          { text: "Namespace", value: "metadata.namespace" },
          { text: "Name", value: "metadata.name" },
          { text: "Status", value: "status.phase" },
          { text: "Start time", value: "status.start_time" },
          { text: "Details & Logs", value: "actions", sortable: false },
        ],
        event: [
          { text: "Type", value: "type" },
          { text: "Namespace", value: "metadata.namespace" },
          { text: "Name", value: "metadata.name" },
          { text: "last_timestamp", value: "last_timestamp" },
          { text: "message", value: "message" },
          { text: "Details", value: "actions", sortable: false },
        ],
        default: [
          { text: "Namespace", value: "metadata.namespace" },
          { text: "Name", value: "metadata.name" },
          { text: "creation_timestamp", value: "metadata.creation_timestamp" },
          { text: "Details", value: "actions", sortable: false },
        ]
      },
      headers: [],
      search: "",
    };
  },
  methods: {
    backToList: function () {
      this.$emit("backToList");
    },
    displayJson: function (item) {
      this.item = item;
      this.dialog = true;
    },
    closeDialog: function () {
      this.dialog = false;
      this.item = {};
    },
    closeLogDialog: function () {
      this.logDialog = false;
      this.item = "";
    },
    showContainers: function (item) {
      this.item = item;
      this.containers = item.spec.containers;
      this.containerDialog = true;
    },
    showLogs: function (container) {
      this.logDialog = false;
      this.containerDialog = false;
      axios
        .get("http://127.0.0.1:5000/api/", {
          params: {
            "resource-type": "log",
            name: this.item.metadata.name,
            namespace: this.item.metadata.namespace,
            container: container.name,
          },
        })
        .then((response) => (this.logs = response.data))
        .catch((error) => console.log(error))
        .finally(() => (this.logDialog = true));
    },
    refresh: function () {
      this.pods = [];
      this.loading = true;
      axios
        .get("http://127.0.0.1:5000/api/", {
          params: {
            "resource-type": this.resourceType,
            "namespace": this.namespace,
          },
        })
        .then((response) => (this.pods = response.data))
        .catch((error) => console.log(error))
        .finally(() => (this.loading = false));
    },
  },
  mounted() {
    if (this.resourceType !== "pod" && this.resourceType !== "event"){
      this.headers = this.allHeaders["default"];
    }
    else {
      this.headers = this.allHeaders[this.resourceType];
    }
    
    this.refresh();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.resource-list {
  padding: 32px;
}
.container-item {
  margin-left: 8px;
  text-transform: uppercase;
}
a:hover {
  text-decoration: underline;
}
</style>
