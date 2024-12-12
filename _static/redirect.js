const basePath = window.location.pathname.split('/').slice(0, -1).join('/');
window.location.href = `${basePath}/_static/password-protected.html`;