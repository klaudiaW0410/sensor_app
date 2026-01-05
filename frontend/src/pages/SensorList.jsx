import  { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import "./Sensors.css";

export const SensorList = () => {
  const[sensors, setSensors] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);       
  const [filter, setFilter] = useState("");  
  const itemsPerPage = 2; 

useEffect(() => {
    const token = localStorage.getItem("token");

    fetch("http://localhost:8000/api/sensors/", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Unauthorized");
        return res.json();
      })
      .then((data) => setSensors(data))
      .catch(() => alert("Please login again"));
  }, []);


  const filteredSensors = sensors.filter(sensor =>
    sensor.name.toLowerCase().includes(filter.toLowerCase())
  );

  
  const start = (currentPage - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  const paginatedSensors = filteredSensors.slice(start, end);


  const totalPages = Math.ceil(filteredSensors.length / itemsPerPage);

  return (
    <div className="container">
      <div className="page">
        <h1>Sensor List</h1>

        <input
          type="text"
          placeholder="Filter by name..."
          value={filter}
          onChange={(e) => {
            setFilter(e.target.value);
            setCurrentPage(1); 
          }}
          className="sensor-filter"
        />

        <ul className="sensor-list">
          {paginatedSensors.map(sensor => (
            <li key={sensor.id}>
              <strong>{sensor.name}</strong> ({sensor.model}){" "}
              <Link to={`/sensors/${sensor.id}`}>Details</Link>
            </li>
          ))}
        </ul>

        <div className="pagination">
          <button
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
          >
            Previous
          </button>

          <span>
            Page {currentPage} of {totalPages}
          </span>

          <button
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};
