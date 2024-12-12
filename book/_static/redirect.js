// const basePath = window.location.pathname.split('/').slice(0, -1).join('/');
// window.location.href = `${basePath}/../_static/password-protected.html`;

// Check if the user has already authenticated
if (!localStorage.getItem("authenticated")) {
    // Redirect to the password-protected page
    if (window.location.pathname === "/" || window.location.pathname.endsWith("index.html")) {
        window.location.href = "../_static/password-protected.html";
    }
}