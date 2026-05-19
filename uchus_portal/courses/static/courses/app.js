// ========== СЛАЙДЕР ==========
document.querySelectorAll('[data-slider]').forEach((slider) => {
    const track = slider.querySelector('.slides');
    if (!track) return; // Проверка наличия слайдера
    
    const slides = Array.from(track.children);
    if (slides.length === 0) return; // Если нет слайдов - выходим
    
    const prev = slider.querySelector('[data-prev]');
    const next = slider.querySelector('[data-next]');
    let index = 0;
    let autoInterval;

    function showSlide(nextIndex) {
        index = (nextIndex + slides.length) % slides.length;
        track.style.transform = `translateX(-${index * 100}%)`;
        track.style.transition = 'transform 0.5s ease';
    }

    function nextSlide() {
        showSlide(index + 1);
    }

    function prevSlide() {
        showSlide(index - 1);
    }

    function startAutoSlide() {
        if (autoInterval) clearInterval(autoInterval);
        autoInterval = setInterval(nextSlide, 4000);
    }

    function stopAutoSlide() {
        if (autoInterval) clearInterval(autoInterval);
    }

    // Добавляем обработчики кнопок
    if (prev && next) {
        prev.addEventListener('click', () => {
            prevSlide();
            stopAutoSlide();
            startAutoSlide();
        });
        
        next.addEventListener('click', () => {
            nextSlide();
            stopAutoSlide();
            startAutoSlide();
        });
        
        // Пауза при наведении
        slider.addEventListener('mouseenter', stopAutoSlide);
        slider.addEventListener('mouseleave', startAutoSlide);
    }

    // Запускаем автослайд
    startAutoSlide();
});

// ========== УВЕДОМЛЕНИЯ ==========
document.querySelectorAll('.alert').forEach((notice) => {
    setTimeout(() => {
        notice.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        notice.style.opacity = '0';
        notice.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            if (notice.remove) notice.remove();
        }, 300);
    }, 3600);
});

// ========== МАСКА ТЕЛЕФОНА ==========
document.querySelectorAll('[data-phone-mask]').forEach((input) => {
    const formatPhone = (value) => {
        let digits = value.replace(/\D/g, '');
        if (digits.startsWith('7')) {
            digits = `8${digits.slice(1)}`;
        }
        if (!digits.startsWith('8') && digits.length > 0) {
            digits = `8${digits}`;
        }
        digits = digits.slice(0, 11);

        const code = digits.slice(1, 4);
        const first = digits.slice(4, 7);
        const second = digits.slice(7, 9);
        const third = digits.slice(9, 11);

        let result = '';
        if (digits.length === 0) return result;
        
        result = '8';
        if (code) {
            result += `(${code}`;
            if (code.length === 3) result += ')';
        }
        if (first) result += first;
        if (second) result += `-${second}`;
        if (third) result += `-${third}`;
        return result;
    };

    input.addEventListener('input', (e) => {
        const cursorPos = input.selectionStart;
        const oldValue = input.value;
        const newValue = formatPhone(input.value);
        input.value = newValue;
        
        if (oldValue !== newValue && cursorPos) {
            const diff = newValue.length - oldValue.length;
            input.setSelectionRange(cursorPos + diff, cursorPos + diff);
        }
    });

    input.addEventListener('focus', () => {
        if (!input.value) input.value = '8';
    });
    
    input.addEventListener('blur', () => {
        if (input.value === '8' || input.value === '8(') {
            input.value = '';
        }
    });
});

// ========== МАСКА ДАТЫ ==========
document.querySelectorAll('[data-date-mask]').forEach((input) => {
    const formatDate = (value) => {
        const digits = value.replace(/\D/g, '').slice(0, 8);
        const day = digits.slice(0, 2);
        const month = digits.slice(2, 4);
        const year = digits.slice(4, 8);

        let result = '';
        if (day) result += day;
        if (month) result += `.${month}`;
        if (year) result += `.${year}`;
        return result;
    };

    input.addEventListener('input', (e) => {
        const oldValue = input.value;
        const newValue = formatDate(input.value);
        input.value = newValue;
        
        // Ограничение на день (01-31)
        if (newValue.length >= 2) {
            let day = parseInt(newValue.slice(0, 2));
            if (day > 31) input.value = '31' + newValue.slice(2);
            if (day < 1) input.value = '01' + newValue.slice(2);
        }
        
        // Ограничение на месяц (01-12)
        if (newValue.length >= 5) {
            let month = parseInt(newValue.slice(3, 5));
            if (month > 12) input.value = newValue.slice(0, 3) + '12' + newValue.slice(5);
            if (month < 1) input.value = newValue.slice(0, 3) + '01' + newValue.slice(5);
        }
    });
});

// ========== АВТОСАБМИТ ФОРМ ==========
document.querySelectorAll('[data-autosubmit]').forEach((field) => {
    field.addEventListener('change', () => {
        const form = field.closest('form');
        if (form) form.submit();
    });
});

// ========== ДОБАВЛЯЕМ ПОДДЕРЖКУ ПЛЕЙСХОЛДЕРОВ ДЛЯ СЕЛЕКТОВ ==========
document.querySelectorAll('select').forEach((select) => {
    if (select.querySelector('option[value=""]') && !select.value) {
        select.style.color = '#6c757d';
        select.addEventListener('change', function() {
            this.style.color = '#212529';
        });
    }
});

// ========== АНИМАЦИЯ ПРИ ЗАГРУЗКЕ ==========
document.addEventListener('DOMContentLoaded', () => {
    // Анимация для карточек
    const cards = document.querySelectorAll('.card, .application-card');
    cards.forEach((card, i) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, i * 100);
    });
});