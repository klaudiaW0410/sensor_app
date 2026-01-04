import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { Line } from "react-chartjs-2";
import mockData from "../../mockData.json";
import "./SensorDetail.css";

export const SensorDetail = () => {
  const { id } = useParams(); 
  const sensorId = Number(id);

  const sensor = mockData.sensors.find(s => s.id === sensorId);

  const readings = mockData.readings.filter(r => r.sensor_id === sensorId);

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const filteredReadings = readings.filter(r => {
    const readingDate = r.timestamp.slice(0, 10); // YYYY-MM-DD
    return (!startDate || readingDate >= startDate) && (!endDate || readingDate <= endDate);
  });

  const data = {
    labels: filteredReadings.map(r => new Date(r.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: "Temperature (°C)",
        data: filteredReadings.map(r => r.temperature),
        borderColor: "red",
      },
      {
        label: "Humidity (%)",
        data: filteredReadings.map(r => r.humidity),
        borderColor: "blue",
      },
    ],
  };

  return (
    <div className="page">
      <h1>{sensor?.name} Details</h1>

      <div className="date-filter">
        <label>Start date:</label>
        <input
          type="date"
          value={startDate}
          onChange={e => setStartDate(e.target.value)}
        />

        <label>End date:</label>
        <input
          type="date"
          value={endDate}
          onChange={e => setEndDate(e.target.value)}
        />
      </div>

      <div className="chart-container">
        <Line data={data} />
      </div>
    </div>
  );
};
