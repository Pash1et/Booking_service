import { NavLink } from 'react-router-dom';
import s from './Header.module.css';

export default function Header() {
    return (
        <div className={s.header}>
            <div className={s.header_nav}>
                <ul>
                    <li>
                        Сервис бронирований
                    </li>
                </ul>
                <ul>
                    <li>
                        <NavLink to="/main">Главная</NavLink>
                    </li>
                    <li>
                        <NavLink to="/bookings">Бронирования</NavLink>
                    </li>
                    <li>
                    <NavLink to="/login">Войти</NavLink>
                    </li>
                </ul>
            </div>
        </div>
    );
}
