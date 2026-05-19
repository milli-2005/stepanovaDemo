document.querySelectorAll('[data-slider]').forEach((slider) => {
    const track = slider.querySelector('.slides');
    const slides = Array.from(track.children);
    const prev = slider.querySelector('[data-prev]');
    const next = slider.querySelector('[data-next]');
    let index = 0;

    function showSlide(nextIndex) {
        index = (nextIndex + slides.length) % slides.length;
        track.style.transform = `translateX(-${index * 100}%)`;
    }

    prev.addEventListener('click', () => showSlide(index - 1));
    next.addEventListener('click', () => showSlide(index + 1));
    setInterval(() => showSlide(index + 1), 3000);
});

document.querySelectorAll('.notice').forEach((notice) => {
    setTimeout(() => {
        notice.style.opacity = '0';
        notice.style.transform = 'translateY(-8px)';
    }, 3600);
});

document.querySelectorAll('[data-phone-mask]').forEach((input) => {
    const formatPhone = (value) => {
        let digits = value.replace(/\D/g, '');
        if (digits.startsWith('7')) {
            digits = `8${digits.slice(1)}`;
        }
        if (!digits.startsWith('8')) {
            digits = `8${digits}`;
        }
        digits = digits.slice(0, 11);

        const code = digits.slice(1, 4);
        const first = digits.slice(4, 7);
        const second = digits.slice(7, 9);
        const third = digits.slice(9, 11);

        let result = '8';
        if (code) result += `(${code}`;
        if (code.length === 3) result += ')';
        if (first) result += first;
        if (second) result += `-${second}`;
        if (third) result += `-${third}`;
        return result;
    };

    input.addEventListener('input', () => {
        input.value = formatPhone(input.value);
    });

    input.addEventListener('focus', () => {
        if (!input.value) input.value = '8';
    });
});

document.querySelectorAll('[data-date-mask]').forEach((input) => {
    const formatDate = (value) => {
        const digits = value.replace(/\D/g, '').slice(0, 8);
        const day = digits.slice(0, 2);
        const month = digits.slice(2, 4);
        const year = digits.slice(4, 8);

        let result = day;
        if (month) result += `.${month}`;
        if (year) result += `.${year}`;
        return result;
    };

    input.addEventListener('input', () => {
        input.value = formatDate(input.value);
    });
});

document.querySelectorAll('[data-autosubmit]').forEach((field) => {
    field.addEventListener('change', () => {
        field.closest('form').submit();
    });
});
