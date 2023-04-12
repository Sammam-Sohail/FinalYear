const {MongoClient} = require('mongodb');
const express = require("express");
const jwt = require('jsonwebtoken');
const app = express();
const cors = require("cors");
const e = require('express');


const PORT = process.env.PORT || 8080;
app.listen(PORT, console.log(`Server started on port ${PORT}`));
app.use(express.urlencoded({ extended: false }))
app.use(express.json())
app.use(cors())

secretKey = 'key';

const uri = "mongodb+srv://admin:BSfzY7TU5FjPkvO7@cluster0.hqyhi3g.mongodb.net/test"
global.client = new MongoClient(uri);

app.get("/calls/:name", async (req, res) => {

    var all_calls
    var name = req.params.name
    // var name = req.params.name.split('-')
    // name = name[0] + " " + name[1]
    // console.log(name)
    var query = { Name: name };

    try{
         all_calls = await client.db("test").collection("coin").find(query).toArray();
        }
    catch(e){
        console.log(e)
    }

    console.log(all_calls)
    res.send(all_calls)
})

app.post('/addcall', async (req, res) => {
  try {
      existingUser = await client.db("test").collection("calls").insertOne(req.body);
      res.status(201).json({ message: 'Call added.' });
} catch (error) {
console.error(error);
res.status(500).json({ error: 'Internal server error' });
}
});

app.post('/login', async (req, res) => {
    try {
      const { username, password } = req.body;
  
      // Validate user input
      if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required' });
      }
  
      // Check if user exists
        var query = { username: username, password:password};

      try{
        result = await client.db("test").collection("users").find(query).toArray();

        if (result[0].username == username && result[0].password == password)
        {
            const token = jwt.sign({ userId: result[0]._id }, secretKey, { expiresIn: '1h' });

            res.json(token)
        }
        else
        {
            return res.status(400).json({ error: 'Username and password are incorrect' });
        }
       }
        catch(e){
        console.log(e)
        }
  
      // Compare passwords
    //   const isPasswordValid = await bcrypt.compare(password, user.password);
    //   if (!isPasswordValid) {
        // return res.status(401).json({ error: 'Invalid username or password' });
    //   }
  
      // Generate JWT token
    //   const token = jwt.sign({ userId: result[0]._id },secretKey, { expiresIn: '1h' });
  
    //   res.json({ token });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  app.post('/signup', async (req, res) => {
        try {

            const query = {username: req.body.username}

            existingUser = await client.db("test").collection("users").findOne(query);
        
            if(existingUser)
            {
                return res.status(400).json({ error: 'Username already taken' });
            }

            else
            {
                await client.db("test").collection("users").insertOne(req.body);
                res.status(201).json({ message: 'User registered successfully' });
            }
      
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });