console.log("JS loaded");

document.addEventListener("DOMContentLoaded", function () {

    let sidebar = document.querySelector('.side-menu');
    let menu = document.querySelector('#menu');
    let login_button = document.getElementById('login_button');
    let login_form = document.getElementById('login_form');
    let logout_button = document.getElementById('logout_button');
    let login_form_exit_button = document.getElementById('exit');



    if (menu && sidebar) {
        menu.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            menu.classList.toggle("change");
        });
    }

    if (login_form_exit_button) {
        login_form_exit_button.onclick = function () {
        login_form.classList.toggle("show");
        if (login_form.classList.contains("show")) {
            document.body.style.overflow = "hidden"; // disable scrolling
        } else {
            document.body.style.overflow = "auto"; // enable scrolling
        }
        }
    }

    if (logout_button) {
        logout_button.addEventListener('click', () => {
            window.location.href = "/logout";
        });
    }

    if (login_button) {
        login_button.onclick = function () {
            login_form.classList.toggle("show");
            if (login_form.classList.contains("show")) {
                document.body.style.overflow = "hidden"; // disable scrolling
            } else {
                document.body.style.overflow = "auto"; // enable scrolling
            }
        };
    }

});
