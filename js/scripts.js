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
    labels: ['Marc Conrad Welschbilliger (Welschbillig)', 'Weyand\'s Viez (Biewer)', 'Joachim Meyer Holzäpelchi (Waldrach)', 'Klimmes (Ralingen)', 'Wolfgang Schmitt Sorte Barbe (Merzig)', 'Römerviez (Welschbillig)', 'Merziger Alter Särkower (Merzig)', 'Franco Viez Juppis Viez (Welschbillig)', 'Rudi Müller (Pluwig)', 'Wiltinger Glühviez (Wiltingen)'],
    datasets: [{
      label: 'A',
      yAxesID: 'A',
      data: [4, 3, 7, 4, 9,2,6,5,4,6],
      borderColor: "#307a44",
      backgroundColor: "rgba(48, 122, 68,0.2)"
    }, {
      label: 'B',
      yAxesID: 'B',
      data: [3, 4, 9, 7, 10,1,7,6,9,10],
      borderColor: "#f46239",
      backgroundColor: "rgba(244, 98, 57,0.2)"
    },
    {
        label: 'C',
        yAxesID: 'C',
        data: [5,4, 7, 9, 2, 0,8,6,8,10],
        borderColor: "#503ade",
        backgroundColor: "rgba(80, 58, 222,0.2)"
      },
      {
        label: 'D',
        yAxesID: 'D',
        data: [2, 1, 9, 4, 10,0,1,5,7,8],
        borderColor: "#f04232",
        backgroundColor: "rgba(201, 122, 56,0.2)"
      },
      {
        label: 'E',
        yAxesID: 'E',
        data: [2, 5, 7, 8, 10,4,9,5,6,10],
        borderColor: "#10ff08",
        backgroundColor: "rgba(16, 255, 8,0.2)"
      },
      {
        label: 'F',
        yAxesID: 'F',
        data: [5, 4, 3, 6, 9,0,5,2,2,10],
        borderColor: "#f5d836",
        backgroundColor: "rgba(245, 216, 54,0.2)"
      },
      {
        label: 'G',
        yAxesID: 'G',
        data: [3, 6, 7, 8, 10,2,9,5,6,10],
        borderColor: "#5cd6f7",
        backgroundColor: "rgba(92, 214, 247,0.2)"
      },
      {
        label: 'H',
        yAxesID: 'H',
        data: [3, 5, 6, 4, 8,1,5,4,6,9],
        borderColor: "#ff08d6",
        backgroundColor: "rgba(255, 8, 214,0.2)"
      },
      {
        label: 'I',
        yAxesID: 'I',
        data: [4, 5,8, 5,10,2,4,6,7,2],
        borderColor: "#321e54",
        backgroundColor: "rgba(50, 30, 84,0.2)"
      },{
        label: 'J',
        yAxesID: 'J',
        data: [5, 4,7, 6,8,3,5,4,3,9],
        borderColor: "#b0bf0a",
        backgroundColor: "rgba(176, 191, 10,0.2)"
      },
      {
        label: 'K',
        yAxesID: 'K',
        data: [0,2, 6,6, 9,3,3,5,1,7],
        borderColor: "#117d5b",
        backgroundColor: "rgba(17, 125, 91,0.2)"
      },
      ]
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
      },
      {
        id: 'D',
        position: {display:false},
      },
      {
        id: 'E',
        position: {display:false},
      },
      {
        id: 'F',
        position: {display:false},
      },
      {
        id: 'G',
        position: {display:false},
      },
      {
        id: 'H',
        position: {display:false},
      },
      {
        id: 'I',
        position: {display:false},
      },{
        id: 'J',
        position: {display:false},
      },
      {
        id: 'K',
        position: {display:false},
      }]
    }
  }
});


new Chart(document.getElementById("bar-chart-2"), {
    type: 'bar',
    data: {
      labels: ['Marc Conrad Welschbilliger (Welschbillig)', 'Weyand\'s Viez (Biewer)', 'Joachim Meyer Holzäpelchi (Waldrach)', 'Klimmes (Ralingen)', 'Wolfgang Schmitt Sorte Barbe (Merzig)', 'Römerviez (Welschbillig)', 'Merziger Alter Särkower (Merzig)', 'Franco Viez Juppis Viez (Welschbillig)', 'Rudi Müller (Pluwig)', 'Wiltinger Glühviez (Wiltingen)'],
      datasets: [
        {
          label: "Mild (10) - Sauer (0)",
          backgroundColor: ["#fbb373", "#f46239","#a73616","#e8c3b9","#c45850","#fbb373", "#f46239","#a73616","#e8c3b9","#c45850"],
          data: [3.1,3.9,7,6.2,8.8,1.5,5.7,4.9,5.6,8.3]
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
