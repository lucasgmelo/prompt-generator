const { Schema, model } = require("mongoose");

const ListSchema = new Schema(
  {
    key: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

module.exports = model("List", ListSchema);
