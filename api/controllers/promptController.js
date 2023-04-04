const {
  getPrompts,
  createPrompt,
  getPromptById,
  updatePrompt,
  deletePrompt,
} = require("../repositories/promptRepositories");

const {
  getList,
  createList,
  deleteList,
} = require("../repositories/listRepositories");

module.exports = {
  list: async (req, res) => {
    try {
      const lists = await getList();

      res.send(lists);
    } catch (error) {
      res.status(400).send(error);
    }
  },
  create: async (req, res) => {
    try {
      const newPrompt = await createPrompt(req.body);
      await createList({ key: newPrompt.id });

      res.status(201).send(newPrompt);
    } catch (error) {
      res.status(400).send(error);
    }
  },
  detail: async (req, res) => {
    try {
      const prompt = await getPromptById(req.params.id);

      if (!prompt) return res.status(404).send({ message: "prompt not found" });

      res.send(prompt);
    } catch (error) {
      res.status(400).send(error);
    }
  },
  update: async (req, res) => {
    try {
      const { id } = req.params;

      const prompt = await getPromptById(id);

      if (!prompt) return res.status(404).send({ message: "prompt not found" });

      const updatedPrompt = await updatePrompt(id, req.body);

      res.send(updatedPrompt);
    } catch (error) {
      res.status(400).send(error);
    }
  },
  delete: async (req, res) => {
    try {
      const prompt = await getPromptById(req.params.id);

      if (!prompt) return res.status(404).send({ message: "prompt not found" });

      await deletePrompt(req.params.id);
      await deleteList(req.params.id);

      res.send({ message: "Deleted successfully" });
    } catch (error) {
      res.status(400).send(error);
    }
  },
};
