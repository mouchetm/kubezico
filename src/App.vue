<template>
  <div id="app" data-app>
    <v-app-bar>
      <v-toolbar-title class="home-logo" @click="view = 'Home'"
        >Kubezico</v-toolbar-title
      >
      <v-spacer></v-spacer>
      <v-btn class="settings-btn" @click="view = 'Settings'"> Settings </v-btn>
    </v-app-bar>
    <div v-if="view == 'Home'">
      <v-card class="homecard" :elevation="0">
        <v-toolbar tile>
          <v-toolbar-title>Select your resource</v-toolbar-title>
        </v-toolbar>
        <v-spacer></v-spacer>
        <div class="namespace-selector">
          <v-text-field
            outlined
            v-model="namespace"
            label="Namespace"
          ></v-text-field>
        </div>
        <v-spacer></v-spacer>
        <v-card
          v-for="category in categorys"
          :key="category.name"
          class="category-card"
        >
          <div class="category-title">
            <strong>{{ category.name }}</strong>
          </div>
          <div class="category">
            <v-card
              class="resource"
              v-for="resource in category.items"
              :key="resource.name"
            >
              <v-card-title>{{ resource.name }}</v-card-title>
              <v-card-text>{{ resource.description }}</v-card-text>
              <v-card-actions>
                <v-btn @click="switchToResourceView(resource.name)"
                  >Display</v-btn
                >
              </v-card-actions>
            </v-card>
          </div>
        </v-card>
      </v-card>
    </div>
    <pod
      v-if="view == 'Pod'"
      :resourceType="resourceType"
      :namespace="namespace"
      @backToList="backToList()"
    ></pod>
    <settings v-if="view == 'Settings'" @backToList="backToList()"></settings>
  </div>
</template>

<script>
import Pod from "./components/Pod.vue";
import Settings from "./components/Settings.vue";

export default {
  name: "app",
  components: {
    Pod,
    Settings,
  },
  data: function () {
    return {
      view: "Home",
      namespace: "",
      resourceType: "pod",
      categorys: [
        { name: "general", items: [{ name: "event", description: "event" }] },
        {
          name: "workloads",
          items: [
            { name: "pod", description: "pods" },
            { name: "deployment", description: "deployment" },
            { name: "job", description: "job" },
          ],
        },
        {
          name: "configuration",
          items: [
            { name: "config_map", description: "configmaps" },
            { name: "secret", description: "secret" },
            { name: "resource_quota", description: "resourcequota" },
          ],
        },
        {
          name: "network",
          items: [
            { name: "ingress", description: "ingress" },
            { name: "service", description: "service" },
          ],
        },
        {
          name: "storage",
          items: [
            {
              name: "persistent_volume_claim",
              description: "persistent_volume_claim",
            },
            { name: "persistent_volume", description: "persistent_volume" },
          ],
        },
      ],
    };
  },
  methods: {
    switchToResourceView(resourceType) {
      this.resourceType = resourceType;
      this.view = "Pod";
    },
    backToList() {
      this.view = "Home";
    },
  },
};
</script>

<style>
body,
html {
  @apply bg-white;
}
.home-logo {
  cursor: pointer;
}
.namespace-selector {
  margin: 32px;
  max-width: 400px;
}
.homecard {
  padding: 32px;
}
.category-card {
  margin-top: 16px;
}
.category-title {
  margin-top: 16px;
  margin-left: 16px;
}
.category {
  margin: 16px;
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 100%;
}
.resource {
  margin: 8px;
}

.settings-btn {
  margin-right: 8px;
}
</style>