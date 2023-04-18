const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const cool = require('cool-ascii-faces')
const path = require('path')

dotenv.config();

const routes = require("../routes");
const dbConnection = require("./dbConnection");

dbConnection();

const app = express();

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb" }));
app.use(cors());
app.use(express.json());
app.use(routes);
app.use(express.static(path.join(__dirname, 'public')))
  .set('views', path.join(__dirname, 'views'))
  .set('view engine', 'ejs')
  .get('/', (req, res) => res.render('pages/index'))
  .get('/cool', (req, res) => res.send(cool()))

module.exports = app;
