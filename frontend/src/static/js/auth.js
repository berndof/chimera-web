export {AuthState}
    
function AuthState(apiBaseUrl) {
    return {
        user: '',
        error: '',
        
        async checkAuth() {
            if (!localStorage.getItem("token")) {
                window.location.href = "/login";
                return;
            }
    
            try {
                let response = await fetch(apiBaseUrl + 'me', {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("token")}`
                    }
                });
                if (!response.ok) throw new Error('Not Authenticated'); // verificar o erro que a response retorna, se é usuário ou se é senha
    
                let data = await response.json();
                this.user = data;
    
            } catch (error) {
                window.location.href = "/login";
            }
        },

        async login(username, password) {
            const data = new URLSearchParams();
            data.append("grant_type", "password");
            data.append("username", username);
            data.append("password", password);
            data.append("client_id", "string"); //TODO ou o valor que sua API espera
            data.append("client_secret", "string"); // idem
    
            try {
                let response = await fetch(apiBaseUrl + 'auth/token', {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: data
                });
    
                let result = await response.json();
                if (!response.ok) throw new Error(result.detail);
                localStorage.setItem("token", result.access_token);
                window.location.href = "/"
    
            } catch (error) {
                console.log(error)
                this.error = error;
            };
        },
        
        logout() {
            localStorage.removeItem("token");
            this.user = '';
            window.location.href = "/login"
        },
    };
}

