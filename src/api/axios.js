import axios from 'axios';

// Tworzenie instancji Axios
const apiClient = axios.create({
    baseURL: 'http://localhost:8080',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor requestu – dokleja token, jeśli jest w localStorage
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {

        return Promise.reject(error);
    }
);

// Interceptor odpowiedzi – globalna obsługa błędów
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            // Jeśli serwer zwrócił status 401 (wygasły token / brak autoryzacji)
            if (error.response.status === 401) {
                // Usuwamy token z localStorage
                localStorage.removeItem('token');
                // Przekierowujemy użytkownika na /login z informacją o wygaśnięciu sesji
                window.location.href = '/login?sessionExpired=true';
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;
