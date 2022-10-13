var filterButton = document.querySelector(".filter a")
var filterDropdown = document.querySelector(".filter-dropdown")

filterButton.addEventListener('click', function() {
    console.log("this")
    if (filterDropdown.className.includes("active")) {
        filterDropdown.classList.remove("active")
        filterButton.classList.remove("active")
    } else {
        filterDropdown.classList.add("active")
        filterButton.classList.add("active")
    }
})