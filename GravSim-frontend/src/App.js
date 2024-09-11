import { useState , useEffect} from 'react';
import axios from 'axios';
import io from 'socket.io-client'
import './App.css';
import './Grid.css';
import './Button.css';

const colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A6", "#A633FF"]; 

const Grid = ( {points} ) => {

  return (
    <div className='grid'>
      {points.map((point, index) => (
      <div key={index} className="point" style={{ left: `${point[0] * 0.1}%`, top: `${point[1] * 0.1}%`, position: "absolute", backgroundColor: colors[index % colors.length], }}></div>
    ))}
    </div>
    )
}

const Button = ({ top, left, label, onClick}) => {
  const buttonStyle = {
    position: 'absolute',
    top: top,    // Dynamically set top position
    left: left,  // Dynamically set left position
  };

  return <button style={buttonStyle} className='button-36' onClick={onClick}>{label}</button>
}

function App() {

  const [data, setData] = useState([]);
  const [socket, setSocket] = useState(null);
  const [eliminatedPlanets, setEliminated] = useState([]);

  useEffect(() => {
    // Connect to Flask WebSocket server
    const socket = io('http://localhost:5000', {
      transports: ['websocket']  // Use only WebSocket transport
    });

    // Listen for messages from the server
    socket.on('planet_positions', (message) => {
      console.log('Received message:', message);
      setData(message); 
      // Set data from the server
    });

    socket.on('planet_eliminated', (message) => {
      console.log('Received message:', message);
      setEliminated(message);
      console.log(eliminatedPlanets);
    })

    socket.emit('message', 'hello from react');

    // Set socket in state
    setSocket(socket)

  }, []);

  const emitMessage = (message) => {
    console.log(message)
    socket.emit(message)
  };


  return (
    <div className='App'>
      <Grid points={data}/>
      <Button top="10%" left="65%" label="start" onClick={() => emitMessage('start')}/>
      <Button top="18%" left="65%" label="stop" onClick={() => emitMessage('stop')}/>
      <Button top="26%" left="65%" label="reset" onClick={() => emitMessage('reset')}/>
      {eliminatedPlanets.map((planetIndex, index) => (
      <div key={index} className='point' style={{ left: `75%`, top: `${index * 1.5 + 10}%`, position: "absolute", backgroundColor: colors[planetIndex % colors.length],}}></div>
      ))}
    </div>
  );
}

export default App;