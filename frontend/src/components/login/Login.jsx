import s from "./Login.module.css";

export default function Login() {
    return (
        <div className={s.login_page}>
            <div className={s.form_login_wrapper}>
                <div className={s.title}>
                    Сервис бронирований
                </div>
                <div className={s.login_form}>
                    <label for="email">Email</label>
                    <input type="email" />
                    <label for="password">Password</label>
                    <input type="password" />
                    <button>
                        Войти
                    </button>
                </div>
            </div>
        </div>
    );
}