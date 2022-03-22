import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import Highscores from './hs';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <p>Routes</p>
      <div className="content">
      <Router>
        <Routes>
        <Route path='/highscores/:world' element={<Highscores/>} />
        </Routes>
      </Router>
      </div>
    </div>
  );
}

export default App;
