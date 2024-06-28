import './App.css';
import BasicComponent from './BasicComponents/BasicComponent'
import Navbar from './BasicComponents/Navbar';
import About from './AboutComponents/About';
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <div className="App container">
        <Navbar />
        <Routes>
          <Route path="/"
            element={<BasicComponent />}
          />
          <Route path="/about"
            element={<About />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
