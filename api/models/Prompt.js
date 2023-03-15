const { Schema, model } = require("mongoose");

const PromptSchema = new Schema(
  {
    prompt: {
      type: String,
      required: true,
    },
    image: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

module.exports = model("Prompt", PromptSchema);
