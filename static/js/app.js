setTimeout(() => {
    document.querySelectorAll(".message").forEach(el => {
        el.style.transition = "opacity .4s";
        el.style.opacity = "0";
        setTimeout(() => el.remove(), 500);
    });
}, 3500);
