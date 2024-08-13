// Bootstrap Alert Auto Close
$("#success-alert").fadeTo(500, 100).slideUp(100, function () {
  $("#success-alert").slideUp(100);
  window.location.href = '/';
});


(function ($) {
  "use strict";
  $("#sidebarToggle, #sidebarToggleTop").on('click', function (e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function () {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };

    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function (e) {
    if ($(window).width() > 768) {
      let e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function () {
    let scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function (e) {
    let $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict

//carousel autoplay
document.addEventListener('DOMContentLoaded', function () {
  var myCarousel = document.querySelector('#heroBanner')
  var carousel = new bootstrap.Carousel(myCarousel, {
    interval: 5000,  // Change slide every 5 seconds
    wrap: true
  })
})

document.addEventListener('DOMContentLoaded', function () {
  // Initialize all dropdowns
  var dropdowns = document.querySelectorAll('.dropdown-toggle');
  dropdowns.forEach(function (dropdown) {
    dropdown.addEventListener('click', function (event) {
      event.preventDefault();
      var dropdownList = this.nextElementSibling;
      dropdownList.classList.toggle('show');
    });
  });

  // Close dropdowns when clicking outside
  window.addEventListener('click', function (event) {
    if (!event.target.matches('.dropdown-toggle')) {
      var dropdowns = document.getElementsByClassName("dropdown-menu");
      for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  });
});

function handleLogout(event) {
  event.preventDefault();
  document.getElementById('logout-form').submit();
}

// Add this to your DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', function () {
  // ... existing code ...

  // Add event listener for logout
  const logoutLink = document.querySelector('a[href="#"][onclick^="document.getElementById(\'logout-form\')"]');
  if (logoutLink) {
    logoutLink.addEventListener('click', handleLogout);
  }
});