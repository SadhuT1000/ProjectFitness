document.addEventListener("DOMContentLoaded", () => {

    // // ===== Кнопки Записаться =====
    // const enrollButtons = document.querySelectorAll(".enroll-btn");
    // enrollButtons.forEach(btn => {
    //     btn.addEventListener("click", (e) => {
    //         const courseId = e.target.dataset.course;
    //         alert(`Вы выбрали курс с ID ${courseId}.\nРеализуйте здесь форму записи!`);
    //     });
    // });

    // ===== Анимация при скролле =====
    const fadeElems = document.querySelectorAll(".fade-in");

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    }, { threshold: 0.1 });

    fadeElems.forEach(elem => observer.observe(elem));

    // ===== Плавный скролл по якорям =====
    const anchors = document.querySelectorAll('a[href^="#"]');
    for (let anchor of anchors) {
        anchor.addEventListener("click", function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute("href"));
            if (target) target.scrollIntoView({behavior: "smooth"});
        });
    }

});
