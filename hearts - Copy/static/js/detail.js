const image = document.getElementById('img');
const intro = document.getElementById('intro');
const large = document.getElementById('large');



if(image.naturalWidth > image.naturalHeight){
    image.classList.add('hide');
    intro.classList.add('hide');
    large.classList.add('show');
}