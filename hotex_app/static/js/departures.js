document.addEventListener( 'DOMContentLoaded', () => {
    const searchInput = document.querySelector('#search')

    searchInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const searchValue = searchInput.value.trim();
            const encodedSearch = encodeURIComponent(searchValue);
            updateQueryParam('search', encodedSearch);
        }
    })
})