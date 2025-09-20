const express = require('express');
const app = express();
app.use(express.json());

let sensorData = [];

app.post('/sensor/push', (req, res) => {
  sensorData.push(req.body);
  res.send({status: "received"});
});

app.get('/sensor/status', (req, res) => {
  res.send(sensorData.slice(-10));
});

app.listen(4000, () => console.log("Sensor server running on 4000."));
