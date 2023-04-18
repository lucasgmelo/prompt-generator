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

const { createUsed } = require("../repositories/usedRepositories");

module.exports = {
  list: async (req, res) => {
    try {
      const prompts = await getPrompts();

      if(prompts.length < 1 ) return res.status(400).send('There are no prompts');

      return res.send(prompts[0]);
    } catch (error) {
      res.status(400).send(error);
    }
  },
  create: async (req, res) => {
    try {
      const newPrompt = await createPrompt(req.body);

      res.status(201).send(newPrompt);
    } catch (error) {
      res.status(400).send(error);
    }
  },
  dayRoutine: async (req, res) => {
    try {
      const prompts = await getPrompts();
      
      if(prompts.length > 1) {
        const newUsed = {
          prompt: prompts[0].prompt,
          image: prompts[0].image,
        }
        
        await createUsed(newUsed)
        await deletePrompt(prompts[0].id)
  
        res.status(201).send('Done!');
      }
    } catch (error) {
      console.log(error)
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
