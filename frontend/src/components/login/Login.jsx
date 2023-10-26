import { useState } from "react";
import axios from 'axios';
import s from "./Login.module.css";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        axios.post('http://api.solved-task.ru/auth/login',
            { email, password }, { withCredentials: true }
            )
            .then((response) => {
                console.log(response.status)
            })
            .catch((err) => {
                console.error("Error: ", err)
            })
    }

    return (
        <div className={s.login_page}>
            <div className={s.form_login_wrapper}>
                <div className={s.title}>
                    Сервис бронирований
                </div>
                <form className={s.login_form} onSubmit={handleSubmit}>
                    <label for="email">
                        Email
                        <input type="email" value={email} onChange={handleEmailChange} />
                    </label>
                    <label for="password">
                        Password
                        <input type="password" value={password} onChange={handlePasswordChange} />
                    </label>
                    <button type="submit">
                        Войти
                    </button>
                </form>
            </div>
        </div>
    );
}