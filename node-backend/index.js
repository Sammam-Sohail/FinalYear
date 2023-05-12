const { MongoClient } = require("mongodb");
const { ObjectId } = require("mongodb");
const express = require("express");
const jwt = require("jsonwebtoken");
const app = express();
const cors = require("cors");
const _ = require("lodash")

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
    const calls = await db.collection("Telegram").find({ $and : [{"Call.Status" : "A"}, { "Timestamp":  { "$lte": Date.now() - (15 * 24 * 60 * 60) }}] }).toArray()
    res.send(calls)
  }
  catch(e){
    res.send(e)
  }

})

/** Gets active calls
 * filters based on duration > 15 days and non evaluated calls
 */
app.post("/updateCall", async (req, res) => {

  try{

    let call = req.body;

    const evaluation_time = Math.round(Date.now() / 1000);
    const time_elapsed = Math.round(Date.now() / 1000) - call.Timestamp;

    const output = algorithm()

    const evaluation = {evaluation_time,time_elapsed,score : output.number, result : output.status}

    var o_id = new ObjectId(call._id);
  

    const result1 = await db.collection("Telegram_clone").updateOne({'_id': o_id},{$set: {'Call.Status' :'P', evaluation}})

    res.send(result1)
  }
  catch(e){
    res.send(e)
  }

})


const algorithm = () => {
  const number = Math.floor(Math.random() * (100+1))
  const status = Math.floor(Math.random() * (2)) === 0 ? 'N' : 'P'
  return {status,number}
}


app.get("/calculate", async (req,res) => {

  try{
    const influencerNames = await db.collection("Influencer").find().project( {"_id": 0, "name": 1}).toArray()

 influencerNames.forEach(async obj => {

      let name = obj.name
      //const sum_p = await db.collection("Telegram_clone").countDocuments({$and: [{Name: name, "evaluation.result": "P" }]})
      //const sum_n = await db.collection("Telegram_clone").countDocuments({$and: [{Name: name, "evaluation.result": "N" }]})

      let sum_p = await db.collection("Telegram_clone").aggregate([{ $match:  {$and: [{ Name: name },   {"evaluation.result": "P" }]}},
        { $group: { _id: null, sum_p: {$sum: 1}}}]).toArray();

      let sum_n = await db.collection("Telegram_clone").aggregate([{ $match:  {$and: [{ Name: name },   {"evaluation.result": "N" }]}},
      { $group: { _id: null, sum_n: {$sum: 1}}}]).toArray();

      let score_avg = await db.collection("Telegram_clone").aggregate([{ $match: { Name: name } },
      { $group: { _id: "$Name", score_avg: {$avg: "$evaluation.score"}}}]).toArray();
      
      
      const data = [...score_avg, ...sum_p, ...sum_n]
      console.log(score_avg, sum_p, sum_n)
      
   });
    res.status(200).send(influencerNames)
  }
  catch(e){
    res.status(404).send("Request failed")
  }
})

app.get('/getDetails/:name' , async(req, res) => {
  
  let objects = await client
  .db("Twigram")
  .collection("Telegram_clone")
  .find({
    $and: [
      { Name: req.params.name },
      { 'Call.Status': 'P' }
    ]
  })
  .toArray()
  
  let score = _.map(objects , (o) => {
    return _.get(o , 'evaluation.score')
  })

  let time_elapsed = _.map(objects , (o) => {
    return _.get(o , 'evaluation.time_elapsed')
  })

  
  res.status(200).send({
    score ,
    time_elapsed
  })
  
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