const Used = require("../models/Used");

module.exports = {
  createUsed: async (UsedInfo) => {
    const newUsed = await Used.create(UsedInfo);

    return newUsed;
  },
};
