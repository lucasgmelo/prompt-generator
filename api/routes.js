const { Router } = require("express");

const promptController = require("./controllers/promptController.js");

const router = Router();

router.route("/routine").get(promptController.dayRoutine);
router
  .route("/prompt")
  .get(promptController.list)
  .post(promptController.create);
router
  .route("/prompt/:id")
  .get(promptController.detail)
  .patch(promptController.update)
  .delete(promptController.delete);

module.exports = router;
