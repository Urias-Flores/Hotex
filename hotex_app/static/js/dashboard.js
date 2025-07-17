document.addEventListener('DOMContentLoaded', function(){
    const roomInput = document.querySelector('#room')

    roomInput.addEventListener('change', () => {
        const dateValue = roomInput.value;
        updateQueryParam('room', dateValue);
    })
})