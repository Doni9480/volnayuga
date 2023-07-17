$(document).ready(() => {
    $('.whatsapp-question-handler').on('click', () => {
        const current_url = window.location.href;
        const message = `Здравствуйте! \nМы нашли ваше объявление на ${current_url}`;
        const link_to_whatsapp = `https://wa.me/+996706305623?text=${message}`;
        window.open(link_to_whatsapp, "_blank");
    })}
)