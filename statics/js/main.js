
const notificationClosers = document.getElementsByClassName('notification-closer');


const notificationClosersArray = Array.from(notificationClosers);

notificationClosersArray.forEach(closer => {
 
    closer.addEventListener('click', () => {
        closer.parentElement.style.display = "none"
    });
});