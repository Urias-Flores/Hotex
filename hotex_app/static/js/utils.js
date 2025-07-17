function updateQueryParam(paramName, paramValue) {
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);
    params.set(paramName, paramValue);
    window.location.href = `${url.pathname}?${params.toString()}`;
}