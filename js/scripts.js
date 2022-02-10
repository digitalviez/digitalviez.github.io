/*!
* Start Bootstrap - Creative v7.0.5 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
//
// Scripts
// 



window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
            document.getElementById("logo").src = "./assets/img/icons/logo-white-Variante2.png"
        } 
        else {
            navbarCollapsible.classList.add('navbar-shrink')
            document.getElementById("logo").src = "./assets/img/icons/logo-black-Variante2.png"
        }

    };


    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    //verhindet direktes Einklappen des Dropdown auf mobilen Geräten
    $('body').on('touchstart.dropdown', '.dropdown-menu', function (e) { e.stopPropagation(); });

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

  
    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Activate SimpleLightbox plugin for portfolio items
    new SimpleLightbox({
        elements: '#portfolio a.portfolio-box'
    });
        
});


//Get the button
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
scrollFunction();
};

function scrollFunction() {
if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
) {
    mybutton.style.display = "block";
} else {
    mybutton.style.display = "none";
}
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
document.body.scrollTop = 0;
document.documentElement.scrollTop = 0;
}

var canvas = document.getElementById('bar-chart');
new Chart(canvas, {
  type: 'line',
  data: {
    labels: ['Römerviez', 'FrancoViez', 'WiltingerViez', 'WeyandsViez', 'Weingut Gehlen'],
    datasets: [{
      label: 'A',
      yAxesID: 'A',
      data: [6, 2, 9, 4, 5],
      borderColor: "#307a44",
      backgroundColor: "rgba(48, 122, 68,0.2)"
    }, {
      label: 'B',
      yAxesID: 'B',
      data: [3, 4, 5, 6, 2],
      borderColor: "#f46239",
      backgroundColor: "rgba(244, 98, 57,0.2)"
    },
    {
        label: 'C',
        yAxesID: 'C',
        data: [7, 8, 9, 10, 10],
        borderColor: "#503ade",
        backgroundColor: "rgba(80, 58, 222,0.2)"
      },
      {
        label: 'D',
        yAxesID: 'D',
        data: [1, 2, 6, 2, 8],
        borderColor: "#f04232",
        backgroundColor: "rgba(201, 122, 56,0.2)"
      },
      {
        label: 'E',
        yAxesID: 'E',
        data: [4, 1, 0, 9, 5],
        borderColor: "#10ff08",
        backgroundColor: "rgba(16, 255, 8,0.2)"
      },
      {
        label: 'F',
        yAxesID: 'F',
        data: [1, 1, 4, 5, 3],
        borderColor: "#f5d836",
        backgroundColor: "rgba(245, 216, 54,0.2)"
      },
      {
        label: 'G',
        yAxesID: 'G',
        data: [7, 2, 1, 6, 7],
        borderColor: "#5cd6f7",
        backgroundColor: "rgba(92, 214, 247,0.2)"
      },
      {
        label: 'H',
        yAxesID: 'H',
        data: [3, 4, 5, 6, 2],
        borderColor: "#ff08d6",
        backgroundColor: "rgba(255, 8, 214,0.2)"
      },
      {
        label: 'I',
        yAxesID: 'I',
        data: [1, 8,4, 4, 9],
        borderColor: "#321e54",
        backgroundColor: "rgba(50, 30, 84,0.2)"
      }]
  },
  options: {
    scales: {
      yAxes: [{
        id: 'A',
        position: 'left',
        ticks: {
            max: 10,
            min: 0
          },
      }, {
        id: 'B',
        position: {display:false},
      },
      {
        id: 'C',
        position: {display:false},
      }]
    }
  }
});


new Chart(document.getElementById("bar-chart-2"), {
    type: 'bar',
    data: {
      labels: ['RömerViez', 'FrancoViez', 'WiltingerViez', 'WeyandsViez', 'Weingut Gehlen'],
      datasets: [
        {
          label: "Süß (10) - Sauer (0)",
          backgroundColor: ["#fbb373", "#f46239","#a73616","#e8c3b9","#c45850"],
          data: [1,5,7,2,4]
        }
      ]
    },
    options: {
      legend: { display: false },
      scales: {
          yAxes: [{
            ticks:{
                max:10,
                min:0
            }
          }]
        }
    }
});
