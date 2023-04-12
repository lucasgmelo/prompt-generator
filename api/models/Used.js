const { Schema, model } = require("mongoose");

const UsedSchema = new Schema(
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

module.exports = model("Used", UsedSchema);
