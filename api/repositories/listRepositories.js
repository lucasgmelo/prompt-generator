const List = require("../models/List");

module.exports = {
  getList: async () => {
    const list = await List.find();

    return list;
  },
  createList: async (ListInfo) => {
    const newList = await List.create(ListInfo);

    return newList;
  },
  deleteList: async (key) => {
    return await List.findOneAndDelete({ key: key });
  },
};
