import { useState , useEffect} from 'react';
import axios from 'axios';
import io from 'socket.io-client'
import './App.css';
import './Grid.css';

const Grid = ( {points} ) => {

    return (
      <div className='grid'>
        {points.map((point, index) => (
        <div key={index} className="point" style={{ left: `${point[0]}px`, top: `${point[1]}px`, position: "absolute" }}></div>
      ))}
      </div>
    )
}

function App() {

  const [data, setData] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Connect to Flask WebSocket server
    const socket = io('http://localhost:5000', {
      transports: ['websocket']  // Use only WebSocket transport
    });

    // Listen for messages from the server
    socket.on('planet_positions', (message) => {
      console.log('Received message:', message);
      setData(message); 
      console.log(message) // Set data from the server
    })

    socket.emit('message', 'hello from react');
    socket.emit('start') // start the simulation

    // Set socket in state
    setSocket(socket);

  }, []);


  return (
    <div className="App">
      <Grid points={data}/>
    </div>
  );
}

export default App;