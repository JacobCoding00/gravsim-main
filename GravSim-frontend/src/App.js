import { useState , useEffect} from 'react';
import io from 'socket.io-client'
import './App.css';
import './Grid.css';
import './Button.css';

const colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A6", "#A633FF"]; 

const Grid = ( {points, onClick} ) => {

  return (
    <div className='grid' onClick={onClick}>
      {points.map((point, index) => ( // map the points to corect postions on grid
      <div key={index} className="point" style={{ height: `${Math.sqrt(point[4]) / 2.5}%`, width: `${Math.sqrt(point[4]) / 2.5}%`, left: `${point[0] * 0.1}%`, top: `${point[1] * 0.1}%`, position: "absolute", backgroundColor: colors[index % colors.length], }}></div>))}

      {points.map((point, index) => ( // map velocity arrows to grid in same position as corresponding points
      <div key={index} className="arrow" style={{ left: `${point[0] * 0.1}%`, top: `${point[1] * 0.1}%`, height:`${point[3] * 50}px`,position: "absolute", transform: `rotate(${point[2] + 3.141 / 2}rad) translate(-1.5px, -${point[3] * 50}px)`, }}></div>))}
    </div>
    )
}

const Button = ({ top, left, label, onClick}) => {
  const buttonStyle = {
    position: 'absolute',
    top: top,
    left: left,
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

  const emitMessage = (message) => { // not needed, remove before finished
    console.log(message)
    socket.emit(message)
  };

  const [newPlanet, setNewPlanet] = useState([]);

  const addPlanet = (e) => {
    const gridRect = e.target.getBoundingClientRect();

    const x = e.clientX - gridRect.left;
    const y = e.clientY - gridRect.top;

    const xAdjusted = (x / gridRect.width) * 1000 // backend considers grid 1000 x 1000
    const yAdjusted = (y / gridRect.height) * 1000
    
    setNewPlanet((prevPlanet) => [...prevPlanet, xAdjusted, yAdjusted]);
    console.log(newPlanet.length);

    if (newPlanet.length >= 4) {
      console.log(newPlanet.length);
      socket.emit('add_planet', newPlanet);
      setNewPlanet([]);
    }
  }


  return (
    <div className='App'>
      <Grid points={data} onClick={(e) => addPlanet(e)}/>
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