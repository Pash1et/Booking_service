import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import Header from './components/header/Header';
import MainPage from './components/main_page/MainPage';
import Bookings from './components/bookings/Bookings';
import Login from './components/login/Login';

export default function App() {
  return (
    <BrowserRouter>
      <div className='app-wrapper'>
        <Header />
        <Routes>
          <Route path="/main" element={<MainPage />} />
          <Route path="/bookings" element={<Bookings />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
