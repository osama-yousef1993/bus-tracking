import aaulogo from './aaulogo.png';
import './App.css';
import Login from './components/login';
import Register from './components/Register';
import HomePage from './components/HomePage'; 
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';


function App() {
  return (
    <div className="App">
      <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/bus-schedule" element={<HomePage />} /> 
        <Route path="/" element={<Login />} />
      </Routes>
    </Router>
    </div>
  );
}

export default App;
