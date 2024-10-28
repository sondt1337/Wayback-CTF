// JavaScript to display the current year
document.getElementById('year').textContent = new Date().getFullYear();

// JavaScript to add hover effect on footer
const footer = document.querySelector('.footer');
footer.addEventListener('mouseenter', () => {
    footer.style.backgroundColor = '#4ca1af';
});
footer.addEventListener('mouseleave', () => {
    footer.style.backgroundColor = '#1c2833';
});

// // Welcome message in home page
// if (window.location.pathname === '/') { // Kiểm tra nếu đang ở trang chủ
//     const welcomeMessage = document.createElement('div');
//     welcomeMessage.className = 'alert alert-info text-center animate__animated animate__fadeIn centered-welcome';
//     welcomeMessage.innerHTML = "Welcome to the CTF Scoreboard Archive!";
//     document.body.appendChild(welcomeMessage); // Thêm vào body để định vị giữa màn hình

//     // Remove message after 3 seconds
//     setTimeout(() => {
//         welcomeMessage.classList.add('animate__fadeOut');
//         welcomeMessage.addEventListener('animationend', () => welcomeMessage.remove());
//     }, 3000);
// }


document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});


window.addEventListener('scroll', function () {
    document.querySelectorAll('.card').forEach(card => {
        const rect = card.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom >= 0) {
            card.classList.add('animate__fadeInUp');
        }
    });
});


// noti successfully created gif
const gifStatusMessage = document.querySelector('.text-center p');
if (gifStatusMessage && gifStatusMessage.textContent.includes("GIF is ready!")) {
    gifStatusMessage.classList.add('alert', 'alert-success', 'animate__animated', 'animate__pulse');
    gifStatusMessage.innerHTML = "<strong>Success!</strong> Your GIF has been created!";
}

document.getElementById('searchInput').addEventListener('keyup', function () {
    let filter = this.value.toUpperCase();
    let items = document.querySelectorAll('#scoreboardList .list-group-item');
    
    items.forEach(item => {
        if (item.textContent.toUpperCase().includes(filter)) {
            item.classList.remove('fade-out');
            item.classList.add('fade-in');
            item.style.display = '';  // Hiển thị mục nếu khớp
        } else {
            item.classList.remove('fade-in');
            item.classList.add('fade-out');
            setTimeout(() => { item.style.display = 'none'; }, 500);  // Đặt độ trễ để hoàn thành hiệu ứng mờ dần
        }
    });
});
