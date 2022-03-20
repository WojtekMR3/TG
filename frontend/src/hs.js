import React, { Component, useState, useEffect } from 'react';
import { useParams, useNavigate } from "react-router-dom";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

function Highscores() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [worlds, setWorlds] = useState([]);
  const { world } = useParams();
  const navigate = useNavigate();

  const [worldName, setWorldName] = React.useState('');

  const handleChange = (event) => {
    let wrld = event.target.value;
    setWorldName(wrld);
    navigate('/highscores/' + wrld);
    fetchHs(wrld)
  };

  function fetchHs(world) {
    fetch("http://127.0.0.1:8000/get_highscores/" + world)
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setItems(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }

  function fetchWorlds() {
    fetch("http://127.0.0.1:8000/get_worlds")
      .then(res => res.json())
      .then(
        (result) => {
          setWorlds(result);
        },
        (error) => {
          setError(error);
        }
      )
  }

  // Note: the empty deps array [] means  
  // this useEffect will run once
  // similar to componentDidMount()
  useEffect(() => {
    fetchWorlds()
    setWorldName(world);
    fetchHs(world)  
  }, [])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (
      <Box sx={{ minWidth: 120 }}>
        <FormControl fullWidth>
          <InputLabel id="demo-simple-select-label">World Name</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={worldName}
            label="Age"
            onChange={handleChange}
          >
            {worlds.map(world => (
              <MenuItem value={world.name}>{world.name}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <ul>
          {items.map(item => (
            <li key={item.id}>
              {item.nick} {item.level}
            </li>
          ))}
        </ul>
      </Box>
    );
  }
}

export default Highscores;