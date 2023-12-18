function toggleSortingOptions() {
    var selectionInput = document.getElementById('selectionInput');
    var sortingOptions = document.getElementById('ebay')
    if (selectionInput.value === "1") {
        sortingOptions.style.display = 'block';
    } else {
        sortingOptions.style.display = 'none';
    }
}

function updateSliderInput(val) {
    var h= document.getElementById('displaySlider');
    h.innerText = "Filter seller reviews under: " + document.getElementById('reviewSlider').value + "%";
}

function resetTerm(val) {
    var i = document.getElementById('termInput');
    i.innerText = "";
}