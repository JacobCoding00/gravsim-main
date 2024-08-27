import { useState , useEffect} from 'react';
import axios from 'axios';
import './App.css';
import './Grid.css';


const Grid = ( {points} ) => {

    return (
      <div className='grid'>
        <div className='point' style= {{ left: points.x, top: points.y}} />
      </div>
    )
}

function App() {

  const [data, setData] = useState([200,0]);
  const [points, setPoints] = useState({x: 0, y: 0})

  useEffect(() => {

    console.log('fetching data');
    axios.get('http://127.0.0.1:5000/api/data')
      .then(response => {
        setData(response.data.message);
        console.log({data})
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
    {/*
    console.log("starting stream")

    const eventSource = new EventSource('http://localhost:5000/stream'); // Adjust the URL as needed
    eventSource.onmessage = (event) => {
      setData(event.data);
      console.log("data received");
    };

    eventSource.onerror = (err) => {
      console.error('EventSource failed:', err);
      eventSource.close();
    };
    */}
  }, []);


  useEffect(() => {
    const x = data[0]
    const y = data[1];
    setPoints({ x, y });
  }, [data]);

  return (
    <div className="App">
      <Grid points={points}/>
    </div>
  );
}

export default App;