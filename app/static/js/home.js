// Home Page JavaScript - GSAP and Swiper Animations

document.addEventListener('DOMContentLoaded', function() {
    // Register GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);
    
    // Hero Slideshow
    const heroSlides = document.querySelectorAll('.hero-slide');
    const heroDots = document.querySelectorAll('.hero-dot');
    let currentSlide = 0;
    const slideInterval = 5000; // 5 seconds per slide
    
    function showSlide(index) {
        heroSlides.forEach((slide, i) => {
            slide.classList.remove('active');
            heroDots[i].classList.remove('active');
        });
        heroSlides[index].classList.add('active');
        heroDots[index].classList.add('active');
    }
    
    function nextSlide() {
        currentSlide = (currentSlide + 1) % heroSlides.length;
        showSlide(currentSlide);
    }
    
    // Auto-advance slides
    let slideTimer = setInterval(nextSlide, slideInterval);
    
    // Dot navigation
    heroDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            clearInterval(slideTimer);
            currentSlide = index;
            showSlide(currentSlide);
            slideTimer = setInterval(nextSlide, slideInterval);
        });
    });
    
    // Hero animations on load
    gsap.from('.hero-title', {
        opacity: 0,
        y: 50,
        duration: 1.2,
        ease: 'power3.out',
        delay: 0.3
    });
    
    gsap.from('.hero-quote', {
        opacity: 0,
        y: 30,
        duration: 1,
        ease: 'power3.out',
        delay: 0.6
    });
    
    gsap.from('.hero-subtitle', {
        opacity: 0,
        y: 30,
        duration: 1,
        ease: 'power3.out',
        delay: 0.9
    });
    
    gsap.from('.hero-buttons', {
        opacity: 0,
        y: 30,
        duration: 1,
        ease: 'power3.out',
        delay: 1.2
    });
    
    gsap.from('.hero-stats-card', {
        opacity: 0,
        x: 50,
        duration: 1,
        ease: 'power3.out',
        delay: 1.5
    });
    
    // Stats Strip Count-up Animation
    const statNumbers = document.querySelectorAll('.stat-strip-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-count'));
        
        ScrollTrigger.create({
            trigger: stat,
            start: 'top 80%',
            onEnter: () => {
                gsap.to(stat, {
                    innerText: target,
                    duration: 2,
                    ease: 'power2.out',
                    snap: { innerText: 1 },
                    onUpdate: function() {
                        stat.innerText = Math.round(this.targets()[0].innerText) + '+';
                    }
                });
            },
            once: true
        });
    });
    
    // About Section Animations
    gsap.from('.about-left', {
        scrollTrigger: {
            trigger: '.about-section',
            start: 'top 70%',
        },
        opacity: 0,
        x: -50,
        duration: 1,
        ease: 'power3.out'
    });
    
    gsap.from('.about-right', {
        scrollTrigger: {
            trigger: '.about-section',
            start: 'top 70%',
        },
        opacity: 0,
        x: 50,
        duration: 1,
        ease: 'power3.out',
        delay: 0.2
    });
    
    // Premium Services Section - Enhanced Directional Mouse Transition
    const serviceCards = document.querySelectorAll('.service-card');
    
    // Check if GSAP is available
    const hasGSAP = typeof gsap !== 'undefined';
    
    if (!hasGSAP) {
        console.warn('GSAP not loaded - using CSS-only hover effects');
    }
    
    let lastHoveredCard = null;
    let lastMousePosition = { x: 0, y: 0 };
    let mouseVelocity = { x: 0, y: 0 };
    
    // Track mouse position globally for momentum
    document.addEventListener('mousemove', (e) => {
        mouseVelocity.x = e.clientX - lastMousePosition.x;
        mouseVelocity.y = e.clientY - lastMousePosition.y;
        lastMousePosition.x = e.clientX;
        lastMousePosition.y = e.clientY;
    });
    
    serviceCards.forEach((card, index) => {
        const details = card.querySelector('.service-card-details');
        const listItems = card.querySelectorAll('.service-card-list li');
        const cta = card.querySelector('.service-card-cta');
        const bg = card.querySelector('.service-card-bg');
        
        // Mouse enter with 8-direction animation (GSAP enhanced, CSS fallback)
        card.addEventListener('mouseenter', (e) => {
            if (!hasGSAP) return; // Let CSS handle the animation
            
            const direction = getDirection8(e, card);
            const { x, y } = getDirectionValues8(direction);
            
            // Apply momentum to animation
            const momentumX = Math.sign(mouseVelocity.x) * Math.min(Math.abs(mouseVelocity.x), 20);
            const momentumY = Math.sign(mouseVelocity.y) * Math.min(Math.abs(mouseVelocity.y), 20);
            
            // Reset and animate details based on direction with momentum
            gsap.set(details, {
                opacity: 0,
                x: x * 40 + momentumX,
                y: y * 40 + momentumY
            });
            
            gsap.to(details, {
                opacity: 1,
                x: 0,
                y: 0,
                duration: 0.7,
                ease: 'power3.out'
            });
            
            // Stagger list items with spring-like feel
            gsap.fromTo(listItems, 
                { opacity: 0, x: x * 25 + momentumX, y: y * 25 + momentumY },
                { 
                    opacity: 1, 
                    x: 0, 
                    y: 0, 
                    duration: 0.5, 
                    stagger: 0.06,
                    ease: 'back.out(1.2)',
                    delay: 0.15
                }
            );
            
            // Fade in CTA last with slight delay
            gsap.fromTo(cta,
                { opacity: 0, y: 15 },
                { 
                    opacity: 1, 
                    y: 0, 
                    duration: 0.5, 
                    ease: 'power3.out',
                    delay: 0.4
                }
            );
            
            lastHoveredCard = card;
            
            // Apply parallax to non-hovered cards
            serviceCards.forEach(otherCard => {
                if (otherCard !== card) {
                    const otherBg = otherCard.querySelector('.service-card-bg');
                    const rect = card.getBoundingClientRect();
                    const otherRect = otherCard.getBoundingClientRect();
                    
                    // Calculate relative position
                    const relX = (otherRect.left + otherRect.width / 2 - rect.left - rect.width / 2) / 500;
                    const relY = (otherRect.top + otherRect.height / 2 - rect.top - rect.height / 2) / 500;
                    
                    gsap.to(otherBg, {
                        x: relX * 8,
                        y: relY * 8,
                        duration: 0.8,
                        ease: 'power2.out'
                    });
                }
            });
        });
        
        // Mouse leave with reverse animation (GSAP enhanced, CSS fallback)
        card.addEventListener('mouseleave', () => {
            if (!hasGSAP) return; // Let CSS handle the animation
            
            const direction = getDirection8(lastMousePosition, card);
            const { x, y } = getDirectionValues8(direction);
            
            gsap.to(details, {
                opacity: 0,
                x: x * 30,
                y: y * 30,
                duration: 0.4,
                ease: 'power2.in'
            });
            
            gsap.to(cta, {
                opacity: 0,
                duration: 0.3,
                ease: 'power2.in'
            });
            
            // Reset parallax on all cards
            serviceCards.forEach(otherCard => {
                const otherBg = otherCard.querySelector('.service-card-bg');
                gsap.to(otherBg, {
                    x: 0,
                    y: 0,
                    duration: 0.6,
                    ease: 'power2.out'
                });
            });
        });
        
        // Enhanced parallax on mouse move with spring physics (GSAP only)
        card.addEventListener('mousemove', (e) => {
            if (!hasGSAP) return;
            
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            
            gsap.to(bg, {
                x: x * 12,
                y: y * 12,
                duration: 0.6,
                ease: 'power2.out'
            });
        });
    });
    
    // Helper function to determine 8-direction mouse movement
    function getDirection8(e, element) {
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const deltaX = x - centerX;
        const deltaY = y - centerY;
        
        const angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI);
        
        // 8-direction detection
        if (angle >= -22.5 && angle < 22.5) return 'right';
        if (angle >= 22.5 && angle < 67.5) return 'bottom-right';
        if (angle >= 67.5 && angle < 112.5) return 'bottom';
        if (angle >= 112.5 && angle < 157.5) return 'bottom-left';
        if (angle >= 157.5 || angle < -157.5) return 'left';
        if (angle >= -157.5 && angle < -112.5) return 'top-left';
        if (angle >= -112.5 && angle < -67.5) return 'top';
        return 'top-right';
    }
    
    // Helper function to get animation values based on 8-direction
    function getDirectionValues8(direction) {
        switch(direction) {
            case 'left': return { x: -1, y: 0 };
            case 'right': return { x: 1, y: 0 };
            case 'top': return { x: 0, y: -1 };
            case 'bottom': return { x: 0, y: 1 };
            case 'top-left': return { x: -0.7, y: -0.7 };
            case 'top-right': return { x: 0.7, y: -0.7 };
            case 'bottom-left': return { x: -0.7, y: 0.7 };
            case 'bottom-right': return { x: 0.7, y: 0.7 };
            default: return { x: 0, y: 0 };
        }
    }
    
    // Services Section Scroll Animation (Old)
    gsap.from('.service-card', {
        scrollTrigger: {
            trigger: '.services-section',
            start: 'top 70%',
        },
        opacity: 0,
        y: 50,
        duration: 0.8,
        ease: 'power3.out',
        stagger: 0.1
    });
    
    // Clean Services Section Scroll Animation - IntersectionObserver based (reliable)
    const serviceItemsClean = document.querySelectorAll('.service-item-clean');

    if (serviceItemsClean.length > 0) {
        // Add hidden class now that JS is running
        serviceItemsClean.forEach(item => {
            item.classList.add('js-animate-hidden');
        });

        const servicesObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const items = document.querySelectorAll('.service-item-clean.js-animate-hidden');
                    items.forEach((item, i) => {
                        const delay = i * 80; // 80ms stagger between items
                        setTimeout(() => {
                            item.classList.remove('js-animate-hidden');
                            item.classList.add('js-animate-visible');
                        }, delay);
                    });
                    servicesObserver.disconnect(); // Only animate once
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        const servicesSectionClean = document.querySelector('.services-section-clean');
        if (servicesSectionClean) {
            servicesObserver.observe(servicesSectionClean);
        }
    }
    
    // Projects Swiper
    const projectSwiper = new Swiper('.project-swiper', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        navigation: {
            nextEl: '.project-swiper-next',
            prevEl: '.project-swiper-prev',
        },
        pagination: {
            el: '.project-swiper-pagination',
            clickable: true,
        },
        breakpoints: {
            640: {
                slidesPerView: 1,
            },
            768: {
                slidesPerView: 2,
            },
            1024: {
                slidesPerView: 3,
            },
        },
    });
    
    // Projects Section Animation
    gsap.from('.project-swiper', {
        scrollTrigger: {
            trigger: '.projects-section',
            start: 'top 70%',
        },
        opacity: 0,
        y: 50,
        duration: 1,
        ease: 'power3.out'
    });
    
    // Testimonials Swiper
    const testimonialSwiper = new Swiper('.testimonial-swiper', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        autoplay: {
            delay: 6000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.testimonial-swiper-pagination',
            clickable: true,
        },
        effect: 'fade',
        fadeEffect: {
            crossFade: true,
        },
    });
    
    // Testimonials Section Animation
    gsap.from('.testimonial-swiper', {
        scrollTrigger: {
            trigger: '.testimonials-section',
            start: 'top 70%',
        },
        opacity: 0,
        y: 50,
        duration: 1,
        ease: 'power3.out'
    });
    
    // News Section Animations
    gsap.from('.news-main', {
        scrollTrigger: {
            trigger: '.news-section',
            start: 'top 70%',
        },
        opacity: 0,
        x: -50,
        duration: 1,
        ease: 'power3.out'
    });
    
    gsap.from('.news-side', {
        scrollTrigger: {
            trigger: '.news-section',
            start: 'top 70%',
        },
        opacity: 0,
        x: 50,
        duration: 1,
        ease: 'power3.out',
        delay: 0.2
    });
    
    // CTA Section Animation
    gsap.from('.cta-content', {
        scrollTrigger: {
            trigger: '.cta-section',
            start: 'top 70%',
        },
        opacity: 0,
        y: 50,
        duration: 1,
        ease: 'power3.out'
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
