const { MongoClient } = require("mongodb");
const express = require("express");
const jwt = require("jsonwebtoken");
const app = express();
const cors = require("cors");
const PORT = process.env.PORT || 8080;
app.listen(PORT, console.log(`Server started on port ${PORT}`));
app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use(
  cors({ origin: ["http://localhost:19006", "exp://192.168.0.210:19000"] })
);

secretKey = "key";

const uri =
  "mongodb+srv://admin:BSfzY7TU5FjPkvO7@cluster0.hqyhi3g.mongodb.net/test";
global.client = new MongoClient(uri);

const db = client.db("Twigram");

/** Gets active calls
 * filters based on duration > 15 days and non evaluated calls
 */
app.get("/activeCalls", async (req, res) =>{

  try{
    const today = new Date();
  const year = today.getFullYear();
  const month = (today.getMonth() + 1).toString().padStart(2, '0');
  const day = (parseInt(today.getDate().toString().padStart(2, '0'))+15).toString();
  const formattedDate = `${year}-${month}-${day}`;

    const r = await db.collection("Telegram").find({ $and : [{"Call.Status" : "A"}, { "Date":  {$lte: new Date(new Date() - 15 * 60 * 60 * 24 * 1000)} }] }).toArray()
    res.send(r)
  }
  catch(e){
    res.send(e)
  }

})



app.get("/calls/:name", async (req, res) => {
  var all_calls;
  var name = req.params.name;
  // var name = req.params.name.split('-')
  // name = name[0] + " " + name[1]
  // console.log(name)
  var query = { Name: name };

  try {
    all_calls = await client
      .db("test")
      .collection("coin")
      .find(query)
      .toArray();
  } catch (e) {
    console.log(e);
  }

  console.log(all_calls);
  res.send(all_calls);
});

app.post("/addcall", async (req, res) => {
  try {
    existingUser = await client
      .db("test")
      .collection("calls")
      .insertOne(req.body);
    res.status(201).json({ message: "Call added." });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/login", async (req, res) => {
  try {
    const { username, password } = req.body;
    // Validate user input
    if (username == undefined || password == undefined) {
      return res
        .status(400)
        .json({ error: "Username and password are required" });
    }

    // Check if user exists
    var query = { username: req.body.username, password: req.body.password };

    try {
      result = await client
        .db("test")
        .collection("users")
        .find(query)
        .toArray();
      if (result[0].username == username && result[0].password == password) {
        return res.send({ status: "Verified" });
      } else {
        return res
          .sendStatus(400)
          .json({ error: "Username and password are incorrect" });
      }
    } catch (e) {
      console.error(e);
    }
  } catch (error) {
    console.error(error);
  }
});

app.post("/signup", async (req, res) => {
  try {
    const query = { username: req.body.username, password: req.body.password };

    existingUser = await client.db("test").collection("users").findOne(query);

    if (existingUser) {
      return res.status(400).json({ error: "Username already taken" });
    } else {
      await client.db("test").collection("users").insertOne(req.body);
      res.status(201).json({ message: "User registered successfully" });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.get("/filtercoins", async (req, res) => {
  try {
    console.log(req);
    res.send("OK");
  } catch (e) {
    console.error(e);
  }
});

app.get("/influencer", async (req, res) => {
  // var query = { Name: name };

  try {
    all_calls = await client
      .db("Twigram")
      .collection("Influencer")
      .find({})
      .toArray();
  } catch (e) {
    console.log(e);
  }

  console.log(all_calls);
  res.send(all_calls);
});