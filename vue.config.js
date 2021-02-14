module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      builderOptions: {
        // options placed here will be merged with default configuration and passed to electron-builder
        files: [
          "**/*"
        ],
        extraFiles: [
          {
            "from": "./dist/app",
            "to": "./dist/app",
            "filter": ["**/*"]
          },
          {
            "from": "./dist/data.json",
            "to": "./dist/data.json",
            "filter": ["**/*"]
          }
        ]
      }
    }
  }
}