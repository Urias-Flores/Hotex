document.addEventListener('DOMContentLoaded', function(){
    const searchInput = document.querySelector('#search')
    const dateInput = document.querySelector('#date')
    const roomInput = document.querySelector('#room')

    roomInput.addEventListener('change', () => {
        const roomValue = roomInput.value;
        updateQueryParam('room', roomValue);
    })

    dateInput.addEventListener('change', () => {
        const dateValue = dateInput.value;
        updateQueryParam('date', dateValue);
    })

    searchInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const searchValue = searchInput.value.trim();
            const encodedSearch = encodeURIComponent(searchValue);
            updateQueryParam('search', encodedSearch);
        }
    })
})