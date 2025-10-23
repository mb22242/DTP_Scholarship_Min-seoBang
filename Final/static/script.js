console.log("JS loaded");

document.addEventListener("DOMContentLoaded", function () {

    // Sidebar toggle
    const sidebar = document.querySelector('.side-menu');
    const menu = document.querySelector('#menu');
    if (menu && sidebar) {
        menu.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            menu.classList.toggle('change');
        });
    }

    // Login form toggle
    const login_button = document.getElementById('login_button');
    const login_form = document.getElementById('login_form');
    const login_form_exit_button = document.getElementById('exit');

    const toggleLoginForm = () => {
        if (!login_form) return;
        login_form.classList.toggle('show');
        document.body.style.overflow = login_form.classList.contains('show') ? 'hidden' : 'auto';
    };
    if (login_button) login_button.addEventListener('click', toggleLoginForm);
    if (login_form_exit_button) login_form_exit_button.addEventListener('click', toggleLoginForm);

    // Logout button
    const logout_button = document.getElementById('logout_button');
    if (logout_button) {
        logout_button.addEventListener('click', () => {
            window.location.href = "/logout";
        });
    }

    // Utility: handles form submission for both Claim and Report
    const handleFormSubmit = (form, type = "Claim") => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = {};
            form.querySelectorAll("input, textarea").forEach(input => {
                formData[input.name] = input.value.trim();
            });

            if (!formData.name || !formData.email) {
                alert("Please fill out all required fields.");
                return;
            }

            const itemName = form.dataset.itemName || formData.item_name || "Unknown Item";

            const params = {
                ...formData,
                item_name: itemName,
                type: type
            };

            emailjs.send("service_lirsgks", "template_kxb4e5d", params)
                .then(() => {
                    alert(`Your ${type.toLowerCase()} for "${itemName}" has been sent successfully.`);
                    form.reset();
                })
                .catch((error) => {
                    console.error(`${type} send failed:`, error);
                    alert(`An error occurred while sending your ${type.toLowerCase()}. Please try again later.`);
                });
        });
    };

    // Initialize forms
    const claimForm = document.getElementById('claim_form');
    const reportForm = document.getElementById('report_form');

    if (claimForm) handleFormSubmit(claimForm, "Claim");
    if (reportForm) handleFormSubmit(reportForm, "Report");

});
