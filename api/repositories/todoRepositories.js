const Prompt = require("../models/Prompt");

module.exports = {
  getPrompts: async () => {
    const prompts = await Prompt.find();

    return prompts;
  },
  getPromptById: async (id) => {
    const prompt = await Prompt.findById(id);

    return prompt;
  },
  createPrompt: async (PromptInfo) => {
    const newPrompt = await Prompt.create(PromptInfo);

    return newPrompt;
  },
  createPrompts: async (PromptsInfo) => {
    const newPrompt = await Prompt.insertMany(PromptsInfo);

    return newPrompt;
  },
  updatePrompt: async (id, body) => {
    const updatedPrompt = await Prompt.findByIdAndUpdate(id, body, {
      new: true,
    });

    return updatedPrompt;
  },
  deletePrompt: async (id) => {
    return await Prompt.findByIdAndDelete(id);
  },
};
