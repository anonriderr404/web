document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll('.container .card img');

    images.forEach(img => {
        const card = img.parentElement;

        img.onload = function() {
            if (img.naturalWidth > img.naturalHeight) {
                card.classList.add('high');
                img.classList.add('high-img');
                // Additional styling or actions can be added here
                // For example: card.style.border = '2px solid red';
            }
        };
    });
});
