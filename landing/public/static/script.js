const timeLine = gsap.timeline({defaults: {duration: 0.8}})

// preloader
timeLine.to('.pre-loader > .overlay', {top: '75%'})
timeLine.to('.pre-loader > .overlay', {top: '50%', delay: 0.5})
timeLine.to('.pre-loader > .overlay', {top: '25%', delay: 0.5})
timeLine.to('.pre-loader > .overlay', {top: '0', delay: 0.5})
timeLine.to('.pre-loader', {width: '85vw', left:0, top: '42%'})
timeLine.set('.pre-loader', {'z-index': -20})

// nav
timeLine.fromTo('nav', {y:-100}, {y:0, opacity:1})

//round text
document.getElementById('roundText').style.paddingLeft = 0;

// animation transition
timeLine.fromTo('.first-row .bold-text', {y:100}, {y:0, opacity:1}, "<")
timeLine.fromTo('.second-row .bold-text', {y:100}, {y:0, opacity:1, delay:0.5})
timeLine.fromTo('.round-text', {y:100}, {y:0, opacity:1, delay:0.5})

// circle menu
// document.getElementById('circleMenu').style.position = 'absolute'
// timeLine.to('#circleMenu', {right:10, bottom: 10})
// timeLine.fromTo('#circleMenu', {y:100}, {y:0, opacity:1})

//mobile media
const isMobile = !(window.matchMedia('(min-width: 768px)').matches)

if (isMobile) {
    timeLine.fromTo('.mobile-row .copy', {y:100}, {y:0, opacity:1, delay:0.5})
    timeLine.fromTo('.mobile-row .cta', {y:100}, {y:0, opacity:1, delay:0.5})
} else {
    timeLine.fromTo('.first-row .copy', {y:100}, {y:0, opacity:1, delay:0.5})
    timeLine.set('.round-text', {opacity:1, delay:0.5})
}