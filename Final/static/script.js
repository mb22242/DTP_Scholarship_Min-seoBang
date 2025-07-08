document.addEventListener("DOMContentLoaded", function () {

    let sidebar = document.querySelector('.side-menu');
    let menu = document.querySelector('#menu');
    let login_button = document.getElementById('login')
    let login_form = document.getElementById('login_form')
    let logout_button = document.getElementById('logout')

    menu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        menu.classList.toggle("change");
    });

    logout_button.addEventListener('click', () => {
        window.location.href = "/logout";
    });

    login_button.onclick = function () {
        login_popup()
    };

    function login_popup() {
        login_form.classList.toggle("show");
        if (login_form.classList.contains("show")) {
            document.body.style.overflow = "hidden"; // disable scrolling
        } else {
            document.body.style.overflow = "auto"; // enable scrolling
        }
    }

    

});