/**
 * Animations JavaScript - Animation triggers and handlers
 */

document.addEventListener('DOMContentLoaded', function() {
    initScrollAnimations();
    initHoverAnimations();
    initParallaxEffects();
});

/**
 * Initialize scroll-based animations
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animationType = element.dataset.animate || 'fade-in';
                const delay = element.dataset.delay || 0;
                
                setTimeout(() => {
                    element.classList.add('animated');
                    element.classList.add(animationType);
                }, delay);
                
                observer.unobserve(element);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });
    
    animatedElements.forEach(el => observer.observe(el));
}

/**
 * Initialize hover animations
 */
function initHoverAnimations() {
    // Card hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-hover');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-hover');
        });
    });
    
    // Button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.classList.add('btn-hover');
        });
        btn.addEventListener('mouseleave', function() {
            this.classList.remove('btn-hover');
        });
    });
}

/**
 * Initialize parallax effects
 */
function initParallaxEffects() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    window.addEventListener('scroll', TCD.throttle(() => {
        const scrollY = window.pageYOffset;
        
        parallaxElements.forEach(el => {
            const speed = parseFloat(el.dataset.parallax) || 0.5;
            const offset = scrollY * speed;
            el.style.transform = `translateY(${offset}px)`;
        });
    }, 16));
}

/**
 * Add animation class to element
 */
function animateElement(element, animationClass, duration = 600) {
    element.classList.add(animationClass);
    
    setTimeout(() => {
        element.classList.remove(animationClass);
    }, duration);
}

/**
 * Stagger animation for list items
 */
function staggerAnimate(elements, animationClass, delay = 100) {
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add(animationClass);
        }, index * delay);
    });
}

/**
 * Counter animation for numbers
 */
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = TCD.formatNumber(Math.round(target));
            clearInterval(timer);
        } else {
            element.textContent = TCD.formatNumber(Math.round(current));
        }
    }, 16);
}

/**
 * Progress bar animation
 */
function animateProgressBar(element, targetWidth, duration = 1000) {
    element.style.width = '0%';
    element.style.transition = `width ${duration}ms ease-out`;
    
    setTimeout(() => {
        element.style.width = targetWidth + '%';
    }, 100);
}

/**
 * Typing animation
 */
function typeText(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

/**
 * Fade in element
 */
function fadeIn(element, duration = 300) {
    element.style.opacity = '0';
    element.style.transition = `opacity ${duration}ms ease`;
    
    setTimeout(() => {
        element.style.opacity = '1';
    }, 10);
}

/**
 * Fade out element
 */
function fadeOut(element, duration = 300) {
    element.style.transition = `opacity ${duration}ms ease`;
    element.style.opacity = '1';
    
    setTimeout(() => {
        element.style.opacity = '0';
    }, 10);
    
    setTimeout(() => {
        element.style.display = 'none';
    }, duration);
}

/**
 * Slide up animation
 */
function slideUp(element, duration = 300) {
    element.style.transform = 'translateY(20px)';
    element.style.opacity = '0';
    element.style.transition = `transform ${duration}ms ease, opacity ${duration}ms ease`;
    
    setTimeout(() => {
        element.style.transform = 'translateY(0)';
        element.style.opacity = '1';
    }, 10);
}

/**
 * Slide down animation
 */
function slideDown(element, duration = 300) {
    element.style.transform = 'translateY(-20px)';
    element.style.opacity = '0';
    element.style.transition = `transform ${duration}ms ease, opacity ${duration}ms ease`;
    
    setTimeout(() => {
        element.style.transform = 'translateY(0)';
        element.style.opacity = '1';
    }, 10);
}

/**
 * Scale animation
 */
function scaleIn(element, duration = 300) {
    element.style.transform = 'scale(0.8)';
    element.style.opacity = '0';
    element.style.transition = `transform ${duration}ms ease, opacity ${duration}ms ease`;
    
    setTimeout(() => {
        element.style.transform = 'scale(1)';
        element.style.opacity = '1';
    }, 10);
}

/**
 * Shake animation (for errors)
 */
function shakeElement(element) {
    element.classList.add('shake');
    setTimeout(() => {
        element.classList.remove('shake');
    }, 500);
}

/**
 * Pulse animation
 */
function pulseElement(element, duration = 2000) {
    element.classList.add('pulse');
    setTimeout(() => {
        element.classList.remove('pulse');
    }, duration);
}

// Export animation functions
window.TCDAnimations = {
    animateElement,
    staggerAnimate,
    animateCounter,
    animateProgressBar,
    typeText,
    fadeIn,
    fadeOut,
    slideUp,
    slideDown,
    scaleIn,
    shakeElement,
    pulseElement
};
