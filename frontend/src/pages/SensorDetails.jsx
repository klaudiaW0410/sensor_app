import { useState , useEffect} from "react";
import { useParams } from "react-router-dom";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from "react-chartjs-2";
import "./SensorDetail.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);
export const SensorDetail = () => {
  const { id } = useParams();
  const sensorId = Number(id);

  const [sensor, setSensor] = useState(null);
  const [readings, setReadings] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() =>{
    fetch(`http://localhost:8000/api/sensors/${sensorId}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(response => response.json())
      .then(data => setSensor(data))
      .catch(err => console.error("Error fetching sensor:", err));
  }, [sensorId, token]);

  useEffect(() => {
    fetch(`http://localhost:8000/api/sensors/${sensorId}/readings/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => res.json())
      .then(data => setReadings(data))
      .catch(err => console.error("Error fetching readings:", err));
  }, [sensorId, token]);

const filteredReadings = readings.filter(r => {
  const readingDate = new Date(r.timestamp);

  const start =
    startDate
      ? new Date(`${startDate}T${startTime || "00:00"}`)
      : null;

  const end =
    endDate
      ? new Date(`${endDate}T${endTime || "23:59"}`)
      : null;

  if (start && readingDate < start) return false;
  if (end && readingDate > end) return false;

  return true;
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
const options = {
  responsive: true,
  plugins: {
    legend: {
      labels: {
        font: { size: 14 },
      },
    },
    title: {
      display: true,
      text: 'Sensor Readings',
      font: { size: 24 },
    },
  },
  scales: {
    x: {
      ticks: {
        font: {
          size: 12, // godziny
        },
      },
    },
    y: {
      ticks: {
        font: {
          size: 14, // wartości temperatury / wilgotności
        },
      },
    },
  },
};


  return (
    <div className="details-container">
      <h1>{sensor?.name} Details</h1>

      <div className="date-filter">
        <label>Start date:</label>
        <input
          type="date"
          value={startDate}
          onChange={e => setStartDate(e.target.value)}
        />

        <label>Start time:</label>
        <input
          type="time"
          value={startTime}
          onChange={e => setStartTime(e.target.value)}
        />

        <label>End date:</label>
          <input
            type="date"
            value={endDate}
            onChange={e => setEndDate(e.target.value)}
          />

        <label>End time:</label>
          <input
            type="time"
            value={endTime}
            onChange={e => setEndTime(e.target.value)}
          />
      </div>

    <div className="chart-container">
        <Line data={data} options={options} />
      </div>
    </div>
  );
};
