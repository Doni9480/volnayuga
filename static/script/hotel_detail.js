$(document).ready(() => {
    $('.whatsapp-question-handler').on('click', () => {
        const current_url = window.location.href;
        const message = `Здравствуйте! \nМы нашли ваше объявление на ${current_url}`;
        const phone = $('.whatsapp-question-handler').data('phone');
        console.log(phone);
        const link_to_whatsapp = `https://wa.me/${phone}?text=${message}`;
        window.open(link_to_whatsapp, "_blank");
    })}
)