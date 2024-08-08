
document.addEventListener('DOMContentLoaded', function() {
    var myCarousel = document.querySelector('#heroBanner')
    if (myCarousel) {
        var carousel = new bootstrap.Carousel(myCarousel, {
            interval: 5000,  // Change slide every 5 seconds
            wrap: true
        })
    }
})
